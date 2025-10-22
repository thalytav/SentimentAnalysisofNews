<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class ValidateNonEmptyText
{
    public function handle(Request $request, Closure $next)
    {
        $text = $request->input('text');

        if (!$text && !$request->hasFile('file')) {
            return response()->json([
                'error' => 'Text or file is required.',
            ], 400);
        }

        if ($text !== null && trim($text) === '') {
            return response()->json([
                'error' => 'Text cannot be empty.',
            ], 400);
        }

        return $next($request);
    }
}
