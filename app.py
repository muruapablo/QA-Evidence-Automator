from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette import status
from fastapi.staticfiles import StaticFiles
import urllib.parse
from pathlib import Path
from datetime import datetime
from utils.docx_builder import add_image_to_docx
import re
import logging
import asyncio
import queue
import json
from winotify import Notification, audio

# Configurar logging optimizado
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)

# Cola para almacenar logs en tiempo real
log_queue = queue.Queue(maxsize=100)

# Handler personalizado para capturar logs
class QueueHandler(logging.Handler):
    def emit(self, record):
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": self.format(record)
        }
        try:
            log_queue.put_nowait(log_entry)
        except queue.Full:
            try:
                log_queue.get_nowait()
                log_queue.put_nowait(log_entry)
            except:
                pass

# Agregar handler a logger
queue_handler = QueueHandler()
queue_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(queue_handler)

# Precompilar regex para mejor performance
TIMESTAMP_PATTERN = re.compile(r"_\d{8}_\d{6}_")

# Caracteres inválidos para nombres de archivo
INVALID_CHARS = str.maketrans({
    "\\": "_", "/": "_", ":": "_", "*": "_", 
    "?": "_", "\"": "_", "<": "_", ">": "_", 
    "|": "_", " ": "_"
})

def sanitize_filename(text: str) -> str:
    """Sanitiza texto para usar como nombre de archivo."""
    return text.translate(INVALID_CHARS)

contact_info = {
    "name": "Pablo Murua",
    "url": "https://EvidenceAutomator.net",
    "email": "muruapablo@gmail.com",
}

app = FastAPI(
    title="Automatizador de Evidencias QA",
    description="Una API para automatizar la generación de documentos de evidencia de pruebas de QA.",
    version="1.0.0",
    contact=contact_info,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = BASE_DIR / "evidences"
TEMPLATE_PATH = BASE_DIR / "templates" / "base_template.docx"
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Ruta al icono personalizado
ICON_PATH = str(BASE_DIR / "static" / "favicon.ico")

def send_windows_notification(title: str, message: str, duration: str = "short"):
    """Envía una notificación toast de Windows."""
    try:
        toast = Notification(
            app_id="QA Evidence Automator",
            title=title,
            msg=message,
            duration=duration,
            icon=ICON_PATH
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
        logger.info(f"🔔 {title}")
    except Exception as e:
        logger.error(f"❌ Error notificación: {e}")

# Variable global para almacenar el contexto de la prueba actual
current_test_context = {"testId": "default_test", "step": "default_step"}

EVIDENCE_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return RedirectResponse(url="/set_context_form")


@app.get("/set_context_form", response_class=HTMLResponse)
async def set_context_form(request: Request, notification_message: str = "", success: str = "false"):
    success_bool = success.lower() == "true"
    
    notification_html = ""
    if notification_message:
        css_class = 'success' if success_bool else 'error'
        notification_html = f'<div class="message {css_class}">{notification_message}</div>'
   
    testId = current_test_context["testId"]
    images_data = []
    test_folder = EVIDENCE_DIR / testId
 
    if test_folder.is_dir():
        for img_file in test_folder.glob("*.png"):
            filename = img_file.name
            step_from_filename = "Paso no especificado"
            original_filename_display = filename
 
            match = TIMESTAMP_PATTERN.search(filename)
            if match:
                timestamp_start_index = match.start(0)
                timestamp_end_index = match.end(0)
                sanitized_step_part = filename[:timestamp_start_index]
                step_from_filename = sanitized_step_part.replace("_", " ")
                original_filename_display = filename[timestamp_end_index:]
 
            images_data.append({
                "filename": filename, 
                "step": step_from_filename, 
                "original_filename": original_filename_display
            })
 
    return TEMPLATES.TemplateResponse(
        "set_context_form.html",
        {
            "request": request,
            "current_test_context": current_test_context,
            "notification_html": notification_html,
            "images_data": images_data
        },
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )


@app.post("/set_context")
async def set_context(testId: str = Form(...), step: str = Form(...)):
    global current_test_context
    current_test_context["testId"] = sanitize_filename(testId)
    current_test_context["step"] = step
    return RedirectResponse(url="/set_context_form", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/evidences")
async def upload_evidence(file: UploadFile = None):
    """Recibe una imagen y la agrega al documento del test usando el contexto actual."""
    testId = current_test_context["testId"]
    step = current_test_context["step"]
    
    if not testId or not step:
        error_message = "Error: testId o step no configurados."
        logger.error(error_message)
        return JSONResponse({"status": "error", "message": error_message}, status_code=400)

    test_folder = EVIDENCE_DIR / testId
    test_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_step = sanitize_filename(step)
    file_path = test_folder / f"{sanitized_step}_{timestamp}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    docx_path = test_folder / f"{testId}_evidence.docx"
    
    try:
        add_image_to_docx(str(docx_path), str(file_path), TEMPLATE_PATH, step, testId)
        success_message = "✅ Evidencia agregada correctamente"
        logger.info(f"✅ {file.filename} → {testId}")
        
        send_windows_notification(
            "Evidencia Agregada ✅",
            f"Paso: {step}\nArchivo: {file.filename}",
            duration="short"
        )
        
        return JSONResponse({
            "status": "success",
            "message": success_message,
            "file_path": str(file_path),
            "docx_path": str(docx_path),
            "web_url": f"/set_context_form?notification_message={urllib.parse.quote(success_message)}&success=true&t={int(datetime.now().timestamp() * 1000)}"
        }, status_code=200)
        
    except PermissionError:
        error_message = "❌ Error: Documento abierto. Cerrarlo para continuar."
        logger.error(f"❌ Documento bloqueado: {testId}")
        
        send_windows_notification(
            "Error - Documento Bloqueado ❌",
            f"El documento {testId}_evidence.docx está abierto.\nCiérralo para continuar.",
            duration="long"
        )
        
        return JSONResponse({
            "status": "error",
            "message": error_message,
            "web_url": f"/set_context_form?notification_message={urllib.parse.quote(error_message)}&success=false&t={int(datetime.now().timestamp() * 1000)}"
        }, status_code=423)
        
    except Exception as e:
        error_message = f"❌ Error inesperado: {str(e)}"
        logger.error(error_message)
        
        send_windows_notification(
            "Error Inesperado ❌",
            f"Error al procesar evidencia:\n{str(e)[:100]}",
            duration="long"
        )
        
        return JSONResponse({
            "status": "error",
            "message": error_message,
            "web_url": f"/set_context_form?notification_message={urllib.parse.quote(error_message)}&success=false&t={int(datetime.now().timestamp() * 1000)}"
        }, status_code=500)


@app.get("/evidences/{testId}/docx")
def get_docx(testId: str):
    """Devuelve el .docx generado para un test."""
    path = EVIDENCE_DIR / testId / f"{testId}_evidence.docx"
    if not path.exists():
        return JSONResponse({"error": "Documento no encontrado"}, status_code=404)
    return FileResponse(
        path, 
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"{testId}_evidence.docx"
    )


@app.get("/evidences/{testId}/images/{image_filename}")
async def get_image(testId: str, image_filename: str):
    image_path = EVIDENCE_DIR / testId / image_filename
    if not image_path.is_file():
        return JSONResponse({"error": "Imagen no encontrada"}, status_code=404)
    return FileResponse(image_path, media_type="image/png")


@app.get("/open_browser")
async def open_browser_with_message(message: str = "", success: str = "true"):
    """Endpoint para redirigir al navegador con un mensaje."""
    encoded_message = urllib.parse.quote(message) if message else ""
    timestamp = int(datetime.now().timestamp() * 1000)
    redirect_url = f"/set_context_form?notification_message={encoded_message}&success={success}&t={timestamp}"
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/monitor", response_class=HTMLResponse)
async def monitor(request: Request):
    """Página que se auto-actualiza para mostrar cambios."""
    return TEMPLATES.TemplateResponse("auto_refresh.html", {"request": request})


@app.get("/logs/stream")
async def stream_logs():
    """Stream de logs en tiempo real usando Server-Sent Events."""
    async def event_generator():
        while True:
            logs_batch = []
            try:
                for _ in range(5):
                    log_entry = log_queue.get_nowait()
                    logs_batch.append(log_entry)
            except queue.Empty:
                pass
            
            if logs_batch:
                data = json.dumps(logs_batch)
                yield f"data: {data}\n\n"
            
            await asyncio.sleep(1)
            yield f": keepalive\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/logs/recent")
async def get_recent_logs():
    """Obtiene los últimos logs almacenados."""
    logs = []
    temp_queue = queue.Queue()
    
    while not log_queue.empty():
        try:
            log = log_queue.get_nowait()
            logs.append(log)
            temp_queue.put(log)
        except queue.Empty:
            break
    
    while not temp_queue.empty():
        try:
            log_queue.put_nowait(temp_queue.get_nowait())
        except queue.Full:
            break
    
    return JSONResponse({"logs": logs[-50:]})
