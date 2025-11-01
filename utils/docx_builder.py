from docx import Document
from docx.shared import Inches
from pathlib import Path
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import copy

def _replace_text_in_paragraph(paragraph, replacements):
    """Replaces placeholder text in a paragraph's runs."""
    for key, value in replacements.items():
        if key in paragraph.text:
            for run in paragraph.runs:
                if key in run.text:
                    run.text = run.text.replace(key, value)

def add_image_to_docx(docx_path, image_path, template_path, step_desc="", test_case_id=""):
    """
    Adds a table and an image for a step to a .docx file.
    Ensures the final order is Table -> Image -> Page Break for each step.
    """
    print(f"DEBUG: Processing DOCX at: {docx_path}")
    docx_file = Path(docx_path)
    
    replacements = {
        "{{TEST_ID}}": test_case_id,
        "{{STEP_DESC}}": step_desc,
    }

    # 1. Open or create the document
    if docx_file.exists():
        document = Document(docx_path)
    else:
        # First step: create from template and replace placeholders everywhere
        document = Document(template_path)
        for paragraph in document.paragraphs:
            _replace_text_in_paragraph(paragraph, replacements)
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        _replace_text_in_paragraph(paragraph, replacements)

    # 2. For existing documents, add a new table for the new step
    if docx_file.exists():
        template_doc = Document(template_path)
        if template_doc.tables:
            # Copy the template table to the end of the document
            template_table = template_doc.tables[0]
            new_tbl_xml = copy.deepcopy(template_table._tbl)
            document.element.body.append(new_tbl_xml)
            new_table = document.tables[-1]

            # Replace placeholders in the new table
            for row in new_table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        _replace_text_in_paragraph(paragraph, replacements)
        else:
            # If template has no table, just add a heading
            document.add_heading(f"Paso: {step_desc}", level=2)

    # 3. Add the image for the current step
    try:
        document.add_picture(image_path, width=Inches(5.5))
        # The picture is in its own paragraph, get it to center it
        last_paragraph = document.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        document.add_paragraph(f"[Image not found: {Path(image_path).name}]")
    
    # 4. Add a page break
    document.add_page_break()

    # 5. Save
    document.save(docx_path)

