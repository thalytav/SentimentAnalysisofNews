<?php
/**
 * Simple API Endpoint for Sentiment & Readability Analysis
 * No Laravel dependency - Pure PHP
 * Works with PHP 8.1+
 */

// Enable CORS for frontend
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed. Use POST.']);
    exit;
}

// Load environment variables
function loadEnv($file) {
    if (!file_exists($file)) {
        return;
    }
    $lines = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) continue;
        list($name, $value) = explode('=', $line, 2);
        $name = trim($name);
        $value = trim($value);
        putenv("$name=$value");
        $_ENV[$name] = $value;
        $_SERVER[$name] = $value;
    }
}

loadEnv(__DIR__ . '/../.env');

// Get Gemini API configuration
$geminiApiKey = getenv('GEMINI_API_KEY') ?: 'AIzaSyBIh8y9NibKTSKMvL2FpoxMPo2sWYCIOVk';
$geminiApiUrl = getenv('GEMINI_API_URL') ?: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent';

// Get input (text or file)
$text = '';

// Check for file upload
if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
    $filePath = $_FILES['file']['tmp_name'];
    $extension = pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION);

    if ($extension === 'txt') {
        $text = file_get_contents($filePath);
    } else {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'error' => 'File tidak didukung. Hanya file .txt yang bisa di-upload saat ini. PDF dan DOCX akan segera didukung.',
            'supported_formats' => ['.txt'],
            'coming_soon' => ['.pdf', '.docx']
        ]);
        exit;
    }
} elseif (isset($_POST['text'])) {
    $text = $_POST['text'];
} else {
    // Try JSON input
    $json = json_decode(file_get_contents('php://input'), true);
    if (isset($json['text'])) {
        $text = $json['text'];
    }
}

// Validate input
if (empty($text)) {
    http_response_code(400);
    echo json_encode(['error' => 'Text or file is required']);
    exit;
}

// ===== SENTIMENT ANALYSIS (Gemini API) =====
function analyzeSentiment($text, $apiKey, $apiUrl) {
    $prompt = "Analisis sentimen dari berita berikut: '{$text}'. " .
              "Apakah sentimennya positif, negatif, atau netral? " .
              "Berikan alasannya dan highlight kata-kata penyebabnya. " .
              "Format jawaban: Sentimen: [Positif/Negatif/Netral], Alasan: [penjelasan singkat]";

    $payload = [
        'contents' => [
            [
                'parts' => [
                    ['text' => $prompt]
                ]
            ]
        ]
    ];

    $ch = curl_init("{$apiUrl}?key={$apiKey}");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode !== 200 || !$response) {
        // Fallback to simple analysis
        return simpleSentimentAnalysis($text);
    }

    $result = json_decode($response, true);
    $geminiText = $result['candidates'][0]['content']['parts'][0]['text'] ?? '';

    return parseGeminiResponse($geminiText);
}

function parseGeminiResponse($geminiText) {
    if (stripos($geminiText, 'positif') !== false) {
        $sentiment = 'Positive';
        $score = 0.75;
    } elseif (stripos($geminiText, 'negatif') !== false) {
        $sentiment = 'Negative';
        $score = 0.25;
    } else {
        $sentiment = 'Neutral';
        $score = 0.5;
    }

    return [
        'sentiment' => $sentiment,
        'score' => $score,
        'details' => $geminiText
    ];
}

function simpleSentimentAnalysis($text) {
    $positiveWords = ['baik', 'bagus', 'hebat', 'senang', 'sukses', 'positif', 'maju', 'unggul', 'meningkat'];
    $negativeWords = ['buruk', 'jelek', 'gagal', 'sedih', 'negatif', 'mundur', 'korupsi', 'menurun'];

    $text = strtolower($text);
    $positiveCount = 0;
    $negativeCount = 0;

    foreach ($positiveWords as $word) {
        $positiveCount += substr_count($text, $word);
    }

    foreach ($negativeWords as $word) {
        $negativeCount += substr_count($text, $word);
    }

    if ($positiveCount > $negativeCount) {
        return ['sentiment' => 'Positive', 'score' => 0.7, 'details' => 'Fallback: Kata positif terdeteksi'];
    } elseif ($negativeCount > $positiveCount) {
        return ['sentiment' => 'Negative', 'score' => 0.3, 'details' => 'Fallback: Kata negatif terdeteksi'];
    } else {
        return ['sentiment' => 'Neutral', 'score' => 0.5, 'details' => 'Fallback: Sentimen netral'];
    }
}

// ===== READABILITY ANALYSIS (Flesch Reading Ease) =====
function analyzeReadability($text) {
    $words = str_word_count($text, 1);
    $sentences = preg_split('/[.!?]+/', $text, -1, PREG_SPLIT_NO_EMPTY);
    $wordCount = max(1, count($words));
    $sentenceCount = max(1, count($sentences));
    $syllableCount = 0;

    foreach ($words as $word) {
        $syllableCount += countSyllables($word);
    }

    $score = 206.835
         - (1.015 * ($wordCount / $sentenceCount))
         - (84.6 * ($syllableCount / $wordCount));

    return round($score, 2);
}

function countSyllables($word) {
    $vowels = ['a', 'e', 'i', 'o', 'u', 'y'];
    $syllables = 0;
    $previousCharIsVowel = false;

    for ($i = 0; $i < strlen($word); $i++) {
        $char = strtolower($word[$i]);
        if (in_array($char, $vowels)) {
            if (!$previousCharIsVowel) {
                $syllables++;
            }
            $previousCharIsVowel = true;
        } else {
            $previousCharIsVowel = false;
        }
    }

    return max(1, $syllables);
}

function getReadabilityCategory($score) {
    if ($score >= 90) return 'Sangat Mudah';
    if ($score >= 80) return 'Mudah';
    if ($score >= 70) return 'Cukup Mudah';
    if ($score >= 60) return 'Standar';
    if ($score >= 50) return 'Cukup Sulit';
    if ($score >= 30) return 'Sulit';
    return 'Sangat Sulit';
}

// ===== PROCESS REQUEST =====
try {
    $sentimentResult = analyzeSentiment($text, $geminiApiKey, $geminiApiUrl);
    $readability = analyzeReadability($text);

    $response = [
        'success' => true,
        'text' => substr($text, 0, 500) . (strlen($text) > 500 ? '...' : ''),
        'sentiment' => $sentimentResult['sentiment'],
        'sentiment_score' => $sentimentResult['score'],
        'sentiment_details' => $sentimentResult['details'],
        'readability' => $readability,
        'readability_category' => getReadabilityCategory($readability),
        'word_count' => str_word_count($text),
        'sentence_count' => count(preg_split('/[.!?]+/', $text, -1, PREG_SPLIT_NO_EMPTY))
    ];

    http_response_code(200);
    echo json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Internal server error: ' . $e->getMessage()
    ]);
}
