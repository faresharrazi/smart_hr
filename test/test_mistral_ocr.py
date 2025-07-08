import base64
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def encode_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

pdf_path = "test/Fares resume 2025.pdf"
base64_pdf = encode_pdf(pdf_path)
if not base64_pdf:
    exit(1)

api_key = os.environ["MISTRAL_API_KEY"]

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
print(all_text)