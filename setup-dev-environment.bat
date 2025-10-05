@echo off
echo 🛠️ Campus Connect - Development Environment Setup
echo ================================================
echo.

echo ✅ Step 1: Setting up Python Backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        echo Make sure Python 3.10+ is installed
        pause
        exit /b 1
    )
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📥 Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo 🗄️ Setting up database...
python manage.py makemigrations
python manage.py migrate

echo 👤 Creating superuser (optional - you can skip this)...
echo Enter admin credentials or press Ctrl+C to skip:
python manage.py createsuperuser

cd ..

echo.
echo ✅ Step 2: Setting up React Frontend...
cd frontend

echo 📥 Installing Node.js dependencies...
npm install
if errorlevel 1 (
    echo ❌ Failed to install Node.js dependencies
    echo Make sure Node.js 16+ and npm are installed
    pause
    exit /b 1
)

cd ..

echo.
echo 🎉 Setup Complete!
echo ================
echo.
echo 🚀 To start development servers, run: start-dev-servers.bat
echo.
echo 📁 Project Structure:
echo   backend/  - Django REST API
echo   frontend/ - React Application
echo.
echo 🌐 Development URLs:
echo   Frontend: http://localhost:3000
echo   Backend:  http://127.0.0.1:8999
echo   Admin:    http://127.0.0.1:8999/admin/
echo   API Docs: http://127.0.0.1:8999/swagger/
echo.
pause