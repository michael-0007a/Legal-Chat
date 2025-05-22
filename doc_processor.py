import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
import os
import tempfile

def is_scanned_pdf(pdf_path):
    """Check if the PDF is scanned or contains selectable text."""
    doc = fitz.open(pdf_path)
    text_length = 0
    for page in doc:
        text_length += len(page.get_text().strip())
    doc.close()
    # If there's very little text, assume it's scanned
    return text_length < 100

def extract_text_from_scanned_pdf(pdf_path):
    """Extract text from scanned PDF using OCR."""
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang="eng") + "\n"
    return text

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF with selectable text."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()
    return text

def process_pdf(file_path):
    """Process PDF and return extracted text."""
    try:
        if is_scanned_pdf(file_path):
            text = extract_text_from_scanned_pdf(file_path)
        else:
            text = extract_text_from_pdf(file_path)
        return text.strip()
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

def save_uploaded_file(file):
    """Save uploaded file temporarily and return the path."""
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)
    
    with open(temp_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    return temp_path

def cleanup_temp_file(file_path):
    """Clean up temporary file."""
    try:
        os.remove(file_path)
    except:
        pass 