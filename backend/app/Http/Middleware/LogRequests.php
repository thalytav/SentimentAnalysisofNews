<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class LogRequests
{
    public function handle(Request $request, Closure $next)
    {
        $start = microtime(true);

        Log::info('➡️ Incoming Request', [
            'method' => $request->method(),
            'url' => $request->fullUrl(),
            'ip' => $request->ip(),
            'payload' => $request->except(['password', 'token']), // hindari log sensitif
        ]);

        $response = $next($request);

        $duration = round((microtime(true) - $start) * 1000, 2);

        Log::info('⬅️ Outgoing Response', [
            'status' => $response->getStatusCode(),
            'duration_ms' => $duration,
        ]);

        return $response;
    }
}
