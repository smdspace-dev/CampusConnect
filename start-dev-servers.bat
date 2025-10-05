@echo off
echo 🚀 Starting Campus Connect Development Servers...
echo.

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo ❌ Virtual environment not found!
    echo Please run: cd backend && python -m venv venv && .\venv\Scripts\Activate.ps1 && pip install -r requirements.txt
    pause
    exit /b 1
)

REM Start backend server in background
echo 📡 Starting Django Backend Server...
start "Campus Connect Backend" cmd /k "cd backend && .\venv\Scripts\activate && python manage.py runserver 127.0.0.1:8999"

REM Wait a moment for backend to start
timeout /t 3 >nul

REM Start frontend server
echo ⚛️ Starting React Frontend Server...
start "Campus Connect Frontend" cmd /k "cd frontend && npm start"

echo.
echo ✅ Both servers starting...
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend API: http://127.0.0.1:8999/api/
echo 📊 Health Check: http://127.0.0.1:8999/api/health/
echo 📖 API Docs: http://127.0.0.1:8999/swagger/
echo 👤 Admin Panel: http://127.0.0.1:8999/admin/
echo.
echo 🛑 To stop servers: Close the terminal windows or use Ctrl+C
echo.
pause