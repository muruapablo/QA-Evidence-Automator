@echo off
REM =====================================================
REM  Inicia el servidor local QA Evidence Automator
REM =====================================================

cd /d "C:\Proyectos\QA-Evidence-Automator"

echo Activando entorno virtual...
call .\venv\Scripts\activate

echo Iniciando servidor de evidencias QA...
echo (Presiona CTRL + C para detenerlo)
echo -----------------------------------------------------
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
pause