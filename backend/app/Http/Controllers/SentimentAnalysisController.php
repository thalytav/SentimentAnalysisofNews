<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class SentimentAnalysisController extends Controller
{
    // Fungsi utama API
    public function analyze(Request $request)
    {
        // Handle file upload atau text input
        if ($request->hasFile('file')) {
            $text = $this->extractTextFromFile($request->file('file'));
        } else {
            $text = $request->input('text');
        }

        if (!$text) {
            return response()->json([
                'error' => 'Text or file is required'
            ], 400);
        }

        // Analisis Sentimen (Gemini API)
        $sentimentResult = $this->analyzeSentiment($text);

        // Analisis Keterbacaan (Flesch Reading Ease)
        $readability = $this->analyzeReadability($text);

        return response()->json([
            'text' => $text,
            'sentiment' => $sentimentResult['sentiment'],
            'sentiment_score' => $sentimentResult['score'],
            'sentiment_details' => $sentimentResult['details'],
            'readability' => $readability,
            'readability_category' => $this->getReadabilityCategory($readability),
            'word_count' => str_word_count($text),
            'sentence_count' => count(preg_split('/[.!?]+/', $text, -1, PREG_SPLIT_NO_EMPTY))
        ]);
    }

    private function extractTextFromFile($file)
    {
        $extension = $file->getClientOriginalExtension();

        if ($extension === 'txt') {
            return file_get_contents($file->getRealPath());
        } elseif ($extension === 'pdf') {
            // TODO: Implement PDF text extraction (need smalot/pdfparser)
            return "PDF extraction not yet implemented. Please use .txt file.";
        } elseif (in_array($extension, ['doc', 'docx'])) {
            // TODO: Implement DOCX text extraction (need phpoffice/phpword)
            return "DOCX extraction not yet implemented. Please use .txt file.";
        }

        return null;
    }

    private function analyzeSentiment($text)
    {
        $apiKey = env('GEMINI_API_KEY');
        $apiUrl = env('GEMINI_API_URL');

        // Prompt untuk Gemini
        $prompt = "Analisis sentimen dari berita berikut: '{$text}'. " .
                  "Apakah sentimennya positif, negatif, atau netral? " .
                  "Berikan alasannya dan highlight kata-kata penyebabnya. " .
                  "Format jawaban: Sentimen: [Positif/Negatif/Netral], Skor: [0-1], Alasan: [penjelasan], Kata Kunci: [kata-kata penting]";

        try {
            $response = Http::timeout(30)->post("{$apiUrl}?key={$apiKey}", [
                'contents' => [
                    [
                        'parts' => [
                            ['text' => $prompt]
                        ]
                    ]
                ]
            ]);

            if ($response->successful()) {
                $result = $response->json();
                $geminiText = $result['candidates'][0]['content']['parts'][0]['text'] ?? '';

                // Parse response Gemini
                return $this->parseGeminiResponse($geminiText);
            } else {
                // Fallback ke analisis sederhana
                return $this->simpleSentimentAnalysis($text);
            }
        } catch (\Exception $e) {
            // Fallback jika Gemini error
            return $this->simpleSentimentAnalysis($text);
        }
    }

    private function parseGeminiResponse($geminiText)
    {
        // Ekstrak sentimen dari response Gemini
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

    private function simpleSentimentAnalysis($text)
    {
        // Fallback sederhana jika Gemini error
        $positiveWords = ['baik', 'bagus', 'hebat', 'senang', 'sukses', 'positif', 'maju', 'unggul', 'meningkat', 'berkembang'];
        $negativeWords = ['buruk', 'jelek', 'gagal', 'sedih', 'negatif', 'mundur', 'korupsi', 'menurun', 'rugi'];

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
            return ['sentiment' => 'Positive', 'score' => 0.7, 'details' => 'Analisis fallback: ditemukan kata positif'];
        } elseif ($negativeCount > $positiveCount) {
            return ['sentiment' => 'Negative', 'score' => 0.3, 'details' => 'Analisis fallback: ditemukan kata negatif'];
        } else {
            return ['sentiment' => 'Neutral', 'score' => 0.5, 'details' => 'Analisis fallback: netral'];
        }
    }

    private function analyzeReadability($text)
    {
        return $this->fleschReadingEase($text);
    }

    private function fleschReadingEase($text)
    {
        $words = str_word_count($text, 1);
        $sentences = preg_split('/[.!?]+/', $text, -1, PREG_SPLIT_NO_EMPTY);
        $wordCount = max(1, count($words));
        $sentenceCount = max(1, count($sentences));
        $syllableCount = 0;

        foreach ($words as $word) {
            $syllableCount += $this->countSyllables($word);
        }

        $score = 206.835
             - (1.015 * ($wordCount / $sentenceCount))
             - (84.6 * ($syllableCount / $wordCount));

        return round($score, 2);
    }

    private function getReadabilityCategory($score)
    {
        if ($score >= 90) return 'Sangat Mudah';
        if ($score >= 80) return 'Mudah';
        if ($score >= 70) return 'Cukup Mudah';
        if ($score >= 60) return 'Standar';
        if ($score >= 50) return 'Cukup Sulit';
        if ($score >= 30) return 'Sulit';
        return 'Sangat Sulit';
    }

    private function countSyllables($word)
    {
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
}
