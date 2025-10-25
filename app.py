from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from datetime import datetime
from utils.docx_builder import add_image_to_docx

contact_info = {
    "name": "Pablo Murua",
    "url": "https://EvidenceAutomator.net",
    "email": "muruapablo@gmail.com",
}

app = FastAPI(
    title="Automatizador de Evidencias QA",
    description="Una API para automatizar la generación de documentos de evidencia",
    version="1.0.0",
    contact=contact_info,
)

BASE_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = BASE_DIR / "evidences"
TEMPLATE_PATH = BASE_DIR / "templates" / "base_template.docx"

EVIDENCE_DIR.mkdir(exist_ok=True)

@app.post("/evidences")
async def upload_evidence(testId: str = Form(...), step: str = Form(""),
                          file: UploadFile = None):
    """Recibe una imagen y la agrega al documento del test."""
    test_folder = EVIDENCE_DIR / testId
    test_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = test_folder / f"{timestamp}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    docx_path = test_folder / f"{testId}_evidence.docx"
    add_image_to_docx(str(docx_path), str(file_path), TEMPLATE_PATH, step)

    return JSONResponse({
        "message": "Evidencia agregada correctamente",
        "file_saved": str(file_path),
        "docx_path": str(docx_path)
    })


@app.get("/evidences/{testId}/docx")
def get_docx(testId: str):
    """Devuelve el .docx generado para un test."""
    path = EVIDENCE_DIR / testId / f"{testId}_evidence.docx"
    if not path.exists():
        return JSONResponse({"error": "Documento no encontrado"}, status_code=404)
    return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        filename=f"{testId}_evidence.docx")