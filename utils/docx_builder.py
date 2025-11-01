from docx import Document
from docx.shared import Inches
from pathlib import Path

def add_image_to_docx(docx_path, image_path, template_path, step_desc=""):
    print(f"DEBUG: Processing DOCX at: {docx_path}") # DEBUG PRINT
    docx_file = Path(docx_path)
    if docx_file.exists():
        document = Document(docx_path)
    else:
        document = Document(template_path)

    document.add_paragraph(f"Paso: {step_desc}")
    document.add_picture(image_path, width=Inches(5.5))
    document.add_paragraph("------------------------------------------------------------------------------------------------------")
    document.save(docx_path)