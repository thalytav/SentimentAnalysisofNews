<?php

namespace App\Exceptions;

use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;
use Throwable;
use Illuminate\Validation\ValidationException;
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Symfony\Component\HttpKernel\Exception\HttpException;
use Illuminate\Support\Facades\Log;

class Handler extends ExceptionHandler
{
    /**
     * A list of exception types with their corresponding custom log levels.
     *
     * @var array<class-string<\Throwable>, \Psr\Log\LogLevel::*>
     */
    protected $levels = [
        //
    ];

    /**
     * A list of the exception types that are not reported.
     *
     * @var array<int, class-string<\Throwable>>
     */
    protected $dontReport = [
        //
    ];

    /**
     * A list of the inputs that are never flashed to the session on validation exceptions.
     *
     * @var array<int, string>
     */
    protected $dontFlash = [
        'current_password',
        'password',
        'password_confirmation',
    ];

    /**
     * Register the exception handling callbacks for the application.
     */
    public function register(): void
    {
        // 🔹 Tangani ValidationException (misalnya dari middleware atau form request)
        $this->renderable(function (ValidationException $e, $request) {
            if ($request->is('api/*') || $request->wantsJson()) {
                Log::warning('⚠️ Validation error', [
                    'errors' => $e->errors(),
                    'path' => $request->path(),
                ]);

                return response()->json([
                    'error' => 'Invalid request',
                    'details' => $e->errors(),
                ], 400);
            }
        });

        // 🔹 Tangani Model Not Found
        $this->renderable(function (ModelNotFoundException $e, $request) {
            if ($request->is('api/*') || $request->wantsJson()) {
                Log::warning('🔍 Model not found', [
                    'message' => $e->getMessage(),
                    'path' => $request->path(),
                ]);

                return response()->json([
                    'error' => 'Resource not found',
                ], 404);
            }
        });

        // 🔹 Tangani 404 untuk route yang tidak ada
        $this->renderable(function (NotFoundHttpException $e, $request) {
            if ($request->is('api/*') || $request->wantsJson()) {
                return response()->json([
                    'error' => 'Endpoint not found',
                ], 404);
            }
        });

        // 🔹 Tangani HTTP exception umum (403, 500, dll.)
        $this->renderable(function (HttpException $e, $request) {
            if ($request->is('api/*') || $request->wantsJson()) {
                $status = $e->getStatusCode();
                return response()->json([
                    'error' => $e->getMessage() ?: 'HTTP Error',
                ], $status);
            }
        });

        // 🔹 Fallback terakhir (error umum)
        $this->renderable(function (Throwable $e, $request) {
            if ($request->is('api/*') || $request->wantsJson()) {
                Log::error('💥 Unhandled Exception', [
                    'message' => $e->getMessage(),
                    'trace' => $e->getTraceAsString(),
                ]);

                return response()->json([
                    'error' => 'Internal Server Error',
                    'message' => config('app.debug') ? $e->getMessage() : null,
                ], 500);
            }
        });
    }
}
