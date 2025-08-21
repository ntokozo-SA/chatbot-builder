@echo off
REM AI Chatbot Builder Setup Script for Windows
REM This script helps set up the project with proper security practices

echo 🚀 AI Chatbot Builder Setup
echo ==========================

REM Check prerequisites
echo [INFO] Checking prerequisites...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 16+ and try again.
    pause
    exit /b 1
)

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed. Please install npm and try again.
    pause
    exit /b 1
)

echo [SUCCESS] Prerequisites check passed!

REM Generate secure secret key
echo [INFO] Generating secure secret key...
for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_urlsafe(32))"') do set SECRET_KEY=%%i

REM Backend setup
echo [INFO] Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating .env file from template...
    copy env.example .env
    
    REM Replace placeholder secret key
    powershell -Command "(Get-Content .env) -replace 'your-secret-key-here', '%SECRET_KEY%' | Set-Content .env"
    
    echo [WARNING] Please edit backend\.env with your actual API keys and configuration.
) else (
    echo [WARNING] backend\.env already exists. Please ensure it contains your actual API keys.
)

deactivate
cd ..

REM Frontend setup
echo [INFO] Setting up frontend...
cd frontend

REM Install dependencies
echo [INFO] Installing Node.js dependencies...
npm install

REM Create .env.local file if it doesn't exist
if not exist ".env.local" (
    echo [INFO] Creating .env.local file from template...
    copy env.example .env.local
    echo [WARNING] Please edit frontend\.env.local with your backend URL.
) else (
    echo [WARNING] frontend\.env.local already exists. Please ensure it contains your backend URL.
)

cd ..

REM Widget setup
echo [INFO] Setting up widget...
cd widget

REM Install dependencies
echo [INFO] Installing widget dependencies...
npm install

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating widget .env file from template...
    copy env.example .env
    echo [WARNING] Please edit widget\.env with your backend URL.
) else (
    echo [WARNING] widget\.env already exists. Please ensure it contains your backend URL.
)

cd ..

echo [SUCCESS] Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Edit the environment files with your actual API keys:
echo    - backend\.env
echo    - frontend\.env.local
echo    - widget\.env
echo.
echo 2. Set up your database:
echo    - Go to your Supabase dashboard
echo    - Run the migration files in backend\migrations\
echo.
echo 3. Start the application:
echo    - Backend: cd backend ^&^& venv\Scripts\activate ^&^& python -m uvicorn app.main:app --reload
echo    - Frontend: cd frontend ^&^& npm run dev
echo    - Widget: cd widget ^&^& npm run dev
echo.
echo 🔒 Security reminder:
echo - Never commit .env files (they're already in .gitignore)
echo - Rotate your API keys regularly
echo - Use HTTPS in production
echo - Enable Row Level Security in Supabase
echo.
echo 📚 For more information, see:
echo - README.md for detailed setup instructions
echo - SECURITY.md for security best practices
echo.
pause 