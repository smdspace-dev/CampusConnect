@echo off
echo Starting Campus Connect...
echo.

echo Starting Django Backend Server...
cd /d "C:\Users\thous\OneDrive\Desktop\Workspace\----------------------------------01\deplyment apps\default_25_09_22_15_14_18\backend"
start "Django Backend" cmd /k "python manage.py runserver 127.0.0.1:8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting React Frontend Server...
cd /d "C:\Users\thous\OneDrive\Desktop\Workspace\----------------------------------01\deplyment apps\default_25_09_22_15_14_18\frontend"
start "React Frontend" cmd /k "npm start"

echo.
echo Servers are starting...
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Opening browser in 10 seconds...
timeout /t 10 /nobreak > nul

echo Opening College Management System in browser...
start "" "http://localhost:3000"

echo.
echo College Management System is now running!
echo Press any key to continue...
pause > nul