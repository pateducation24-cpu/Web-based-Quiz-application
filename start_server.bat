
@echo off
title QuizApp Launcher
color 0A
echo ========================================
echo    QUIZAPP LAUNCHER
echo ========================================
echo.
echo Starting Django Server...
cd /d "%~dp0"
start http://127.0.0.1:8000
py manage.py runserver
pause