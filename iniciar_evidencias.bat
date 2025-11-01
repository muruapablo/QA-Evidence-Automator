@echo off
REM =====================================================
REM  Inicia el servidor local QA Evidence Automator
REM =====================================================

cd /d "C:\Proyectos\QA-Evidence-Automator"

echo Activando entorno virtual...
call .\venv\Scripts\activate

echo Iniciando servidor de evidencias QA...
echo Esperando a que el servidor este listo...
echo (Presiona CTRL + C para detenerlo)
echo -----------------------------------------------------

REM Iniciar el servidor en una nueva ventana
start "QA Evidence Server" uvicorn app:app --host 127.0.0.1 --port 8000 --reload

REM Esperar 3 segundos para que el servidor inicie
timeout /t 3 /nobreak >nul

REM Abrir Chrome en modo incognito (nueva ventana limpia sin cache)
echo Abriendo Chrome en nueva ventana...
start "" "C:\Users\Pedro Hernadez\AppData\Local\ms-playwright\chromium-1194\chrome-win\chrome.exe" --window-size=700,900 --window-position=1220,0 http://127.0.0.1:8000/set_context_form

echo.
echo =====================================================
echo  Servidor iniciando en una nueva ventana.
echo  Esta ventana se cerrara automaticamente.
echo =====================================================
echo.
