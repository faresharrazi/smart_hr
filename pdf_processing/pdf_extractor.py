"""
PDF Extractor (Mistral OCR only)

Handles text extraction from PDFs using the Mistral OCR API via direct HTTP requests.
"""

import base64
import os
import sys
from typing import Optional

# Debug imports
print("Starting PDF extractor imports...")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path[:3]}...")  # Show first 3 paths

# Try to import requests with better error handling
try:
    import requests
    print("✓ requests imported successfully")
except ImportError as e:
    print(f"✗ Error importing requests: {e}")
    print(f"Available modules: {[m for m in sys.modules.keys() if 'request' in m.lower()]}")
    raise ImportError(f"requests module not found. Please ensure it's installed: pip install requests. Error: {e}")

print("✓ All imports successful")

class PDFExtractor:
    """Extract text from PDF files using Mistral OCR API via direct HTTP requests."""
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> Optional[str]:
        """Extract text from a PDF file using Mistral OCR API."""
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise RuntimeError("MISTRAL_API_KEY not set in environment.")
        
        # Read and encode PDF to base64
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        
        # Call Mistral OCR API directly via HTTP
        url = "https://api.mistral.ai/v1/ocr"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-ocr-latest",
            "document": {
                "type": "document_url",
                "document_url": f"data:application/pdf;base64,{base64_pdf}"
            },
            "include_image_base64": True
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # Parse response and extract text
        ocr_response = response.json()
        all_text = "\n\n".join(page["markdown"] for page in ocr_response["pages"])
        return all_text if all_text.strip() else None 