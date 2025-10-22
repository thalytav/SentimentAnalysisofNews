<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\SentimentAnalysisController;

// Endpoint untuk analisis sentimen dan readability
// Support: text input atau file upload (.txt, .pdf, .docx)
Route::post('/analyze', [SentimentAnalysisController::class, 'analyze'])
    ->middleware(['log.requests', 'validate.text']);
