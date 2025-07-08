# Smart HR: CV vs Job Description Analyzer

A minimal web app to analyze the fit between a candidate's CV (PDF) and a job description using Mistral LLM.

## Setup

- Clone the repo:
  ```bash
  git clone https://github.com/faresharrazi/smart_hr.git
  cd smart_hr
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Set your MISTRAL API key in a `.env` file:
  ```env
  MISTRAL_API_KEY=your-key-here
  ```
- (Optional) Install Tesseract OCR for scanned PDFs: [Instructions](https://github.com/tesseract-ocr/tesseract)

## Run

```bash
streamlit run app.py
```

## Usage

1. Enter the job description.
2. Upload a candidate's CV (PDF).
3. Click Analyze to view the fit score, metrics, and analysis.
