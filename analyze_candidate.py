import sys
import os
import json
from pdf_processing.pdf_extractor import PDFExtractor
from utils.cv_structurer import structure_cv_text
from utils.llm_analyzer import analyze_candidate


def main():
    if len(sys.argv) != 3:
        print("Usage: python analyze_candidate.py <job_description.txt> <cv.pdf>", file=sys.stderr)
        sys.exit(1)

    job_desc_path = sys.argv[1]
    pdf_path = sys.argv[2]

    # Read job description
    with open(job_desc_path, 'r', encoding='utf-8') as f:
        job_description = f.read()

    # Extract text from PDF CV
    with open(pdf_path, 'rb') as f:
        try:
            cv_text = PDFExtractor.extract_text_from_pdf(f)
        except Exception as e:
            print(f'Error extracting text: {e}', file=sys.stderr)
            sys.exit(1)
    if not cv_text:
        print('❌ Could not extract text from the PDF CV.', file=sys.stderr)
        sys.exit(1)

    # Structure the CV text
    structured_cv = structure_cv_text(cv_text)

    # Analyze with LLM
    try:
        result = analyze_candidate(job_description, structured_cv)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    # Print JSON result to stdout only
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main() 