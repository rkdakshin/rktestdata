@echo off
echo ====================================
echo Invoice Generator - Setup Script
echo ====================================
echo.

echo Step 1: Setting up Backend (Python Flask)
echo ------------------------------------------
cd backend
echo Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate
echo Installing Python dependencies...
pip install -r requirements.txt
echo.
echo Backend setup complete!
echo.

echo Step 2: Setting up Frontend (React TypeScript)
echo -----------------------------------------------
cd ..\frontend
echo Installing Node dependencies...
call npm install
echo.
echo Frontend setup complete!
echo.

echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Create a PostgreSQL database named 'invoice_db'
echo 2. Copy backend\.env.example to backend\.env and configure
echo 3. Copy frontend\.env.example to frontend\.env
echo 4. Run 'start.bat' to start both servers
echo.
pause
