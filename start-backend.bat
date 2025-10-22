@echo off
echo ========================================
echo Starting Backend Server (PHP)
echo ========================================
echo.
echo Backend will run at: http://localhost:8000
echo API Endpoint: http://localhost:8000/api.php
echo.
echo Press Ctrl+C to stop the server
echo.

cd Sentiment-ReadAbility-Analysis-of-News-Website-main\backend\public
php -S localhost:8000

pause
