@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PYTHON=C:\Users\Azrar Link\anaconda3\python.exe"
if not exist "%PYTHON%" set "PYTHON=python"
echo Starting Skan AI...
"%PYTHON%" -m streamlit run app.py --server.headless false
pause
