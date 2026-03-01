import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from typing import Optional

from settings import get_settings

settings = get_settings()


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF, falling back to OCR when needed."""
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            if page_index >= settings.max_pdf_pages:
                break

            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"

    # If we didn't get meaningful text, try OCR as a fallback
    if not text.strip():
        text = extract_text_with_ocr(pdf_path, max_pages=settings.max_pdf_pages)

    # Debugging: Print extracted text to terminal
    print("Extracted PDF Text:\n", text)

    return text


def extract_text_with_ocr(pdf_path: str, max_pages: Optional[int] = None) -> str:
    text = ""
    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        if max_pages is not None and i >= max_pages:
            break
        extracted_text = pytesseract.image_to_string(image)
        text += extracted_text + "\n"

    # Debugging: Print OCR text
    print("OCR Extracted Text:\n", text)

    return text

