@echo off
echo ========================================
echo Starting Frontend Server (Vue.js)
echo ========================================
echo.
echo Installing dependencies (if needed)...
echo.

cd Sentiment-ReadAbility-Analysis-of-News-Website-main\frontend

if not exist "node_modules" (
    echo Node modules not found. Installing...
    call npm install
)

echo.
echo Starting development server...
echo Frontend will run at: http://localhost:5173
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause
