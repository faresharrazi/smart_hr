# Smart HR: CV vs Job Description Analyzer

A minimal web app to analyze the fit between a candidate's CV (PDF) and a job description using Mistral LLM.

## 🌐 Live Demo

**Production URL**: https://smart-hr-ai.streamlit.app/

## Features

- **PDF Text Extraction**: Uses Mistral OCR API for reliable text extraction from PDFs (including scanned documents)
- **AI-Powered Analysis**: Leverages Mistral LLM for intelligent candidate-job matching
- **Comprehensive Scoring**: Provides overall fit score with detailed sub-metrics
- **Clean UI**: Minimalist Streamlit interface with modern design
- **Production Ready**: Deployed on Streamlit Cloud with robust error handling

## Technical Stack

- **Frontend**: Streamlit
- **LLM**: Mistral AI (via LangChain)
- **OCR**: Mistral OCR API for PDF text extraction
- **Backend**: Python with modular architecture
- **Deployment**: Streamlit Cloud

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

## Run

```bash
streamlit run app.py
```

## Usage

1. Enter the job description in the left panel
2. Upload a candidate's CV (PDF) in the right panel
3. Click "Analyze" to get the fit analysis
4. View the overall score and detailed metrics

## How It Works

1. **PDF Processing**: The app uses Mistral's OCR API to extract text from uploaded PDFs, ensuring compatibility with both text-based and scanned documents
2. **Analysis**: The extracted text is analyzed alongside the job description using Mistral LLM
3. **Scoring**: The system provides an overall fit score (0-100) with sub-metrics for skills match, experience, education, and soft skills
4. **Results**: Clean, color-coded results display with detailed analysis and recommendations
