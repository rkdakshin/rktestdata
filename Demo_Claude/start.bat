@echo off
echo ====================================
echo Starting Invoice Generator
echo ====================================
echo.

echo Starting Backend Server (Flask)...
start cmd /k "cd backend && venv\Scripts\activate && python app.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server (Vite)...
start cmd /k "cd frontend && npm run dev"

echo.
echo ====================================
echo Servers Started!
echo ====================================
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit...
pause > nul
