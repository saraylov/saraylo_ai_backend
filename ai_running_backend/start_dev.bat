@echo off
echo Запуск разработческого окружения SARAYLO AI Workout System
echo ======================================================

echo Запуск бэкенда (Flask)...
start "Flask Backend" /D "%~dp0" python api/workout_api.py

echo Запуск фронтенда (Vite)...
cd gui
start "Vite Frontend" npm run dev

echo.
echo Разработческое окружение запущено!
echo Бэкенд:  http://localhost:5000
echo Фронтенд: http://localhost:3000
echo.
echo Для остановки серверов закройте окна терминалов.
pause