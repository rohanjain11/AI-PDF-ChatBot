import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

def extract_text_from_pdf(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"

    # Debugging: Print extracted text to terminal
    print("Extracted PDF Text:\n", text)

    return text


def extract_text_with_ocr(pdf_path):
    text = ""
    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        extracted_text = pytesseract.image_to_string(image)
        text += extracted_text + "\n"

    # Debugging: Print OCR text
    print("OCR Extracted Text:\n", text)

    return text

