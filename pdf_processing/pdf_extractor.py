"""
PDF Extractor

Handles text extraction from both text-based and image-based PDFs.
"""

import PyPDF2
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_bytes
from typing import Optional
import sys


class PDFExtractor:
    """Extract text from PDF files with fallback methods"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> Optional[str]:
        """Extract text from uploaded PDF file, fallback to PyMuPDF, then OCR if needed."""
        
        # Try PyPDF2 first
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            if text.strip():
                return text
            else:
                print("PyPDF2 could not extract text, trying PyMuPDF fallback...", file=sys.stderr)
        except Exception as e:
            print(f"PyPDF2 error: {str(e)}. Trying PyMuPDF fallback...", file=sys.stderr)
        
        # Fallback: PyMuPDF
        try:
            pdf_file.seek(0)
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            if text.strip():
                return text
            else:
                print("PyMuPDF could not extract text, trying OCR fallback...", file=sys.stderr)
        except Exception as e:
            print(f"PyMuPDF error: {str(e)}. Trying OCR fallback...", file=sys.stderr)
        
        # Fallback: OCR
        try:
            pdf_file.seek(0)
            images = convert_from_bytes(pdf_file.read())
            text = ""
            for i, image in enumerate(images):
                ocr_text = pytesseract.image_to_string(image)
                text += ocr_text
            if text.strip():
                print("Text extracted using OCR. Results may be less accurate for low-quality scans.", file=sys.stderr)
                return text
            else:
                print("OCR could not extract text. The PDF may be blank or corrupted.", file=sys.stderr)
                return None
        except Exception as e:
            print(f"OCR error: {str(e)}. Make sure Tesseract is installed on your system.", file=sys.stderr)
            return None 