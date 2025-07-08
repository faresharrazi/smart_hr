"""
CV vs Job Description Analyzer - Modular Version

A Streamlit web application that uses AI to analyze the compatibility between job descriptions and candidate CVs.
Uses Mistral Small for analysis.
"""

import streamlit as st
import os
import json
import subprocess
import re
import plotly.graph_objects as go
from utils.json_io import load_json

def main():
    st.set_page_config(
        page_title="CV vs Job Description Analyzer",
        page_icon="📋",
        layout="wide"
    )
    
    st.title("CV vs Job Description Analyzer")
    st.markdown("Upload a CV (PDF) and enter a job description to analyze candidate fit.")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    result_data = None
    
    with col1:
        st.subheader("Job Description")
        job_description = st.text_area(
            "Enter the job description:",
            height=300,
            placeholder="Paste the job description here..."
        )
    
    with col2:
        st.subheader("CV Upload")
        uploaded_file = st.file_uploader(
            "Upload CV (PDF)",
            type=['pdf'],
            help="Upload a PDF file containing the candidate's CV"
        )
        
        # Right-align the Analyze button using custom CSS
        st.markdown("""
            <style>
            .analyze-btn-container { display: flex; justify-content: flex-end; }
            </style>
            <div class="analyze-btn-container">
        """, unsafe_allow_html=True)
        analyze_clicked = st.button("Analyze", key="analyze_btn", type="primary")
        st.markdown("</div>", unsafe_allow_html=True)
        if analyze_clicked:
            if not job_description.strip():
                st.error("Please enter a job description.")
            elif uploaded_file is None:
                st.error("Please upload a CV file.")
            else:
                # Save uploaded file temporarily
                temp_cv_path = "temp_cv.pdf"
                with open(temp_cv_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # Save job description to file
                temp_job_path = "temp_job.txt"
                with open(temp_job_path, "w") as f:
                    f.write(job_description)
                # Run the analysis and capture JSON result from stdout
                with st.spinner("Analyzing candidate..."):
                    try:
                        result = subprocess.run([
                            "python", "analyze_candidate.py",
                            temp_job_path,
                            temp_cv_path
                        ], capture_output=True, text=True, check=True)
                        try:
                            result_data = json.loads(result.stdout)
                        except Exception as parse_err:
                            st.error("Analysis failed: Could not parse JSON output.")
                            st.code(result.stdout)
                            result_data = None
                        if result_data:
                            st.session_state['result_data'] = result_data
                    except subprocess.CalledProcessError as e:
                        st.error(f"Analysis failed: {e.stderr}")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                    finally:
                        if os.path.exists(temp_cv_path):
                            os.remove(temp_cv_path)
                        if os.path.exists(temp_job_path):
                            os.remove(temp_job_path)
    # Display results in a visually distinct container below the form
    if 'result_data' in st.session_state:
        with st.container():
            display_results(st.session_state['result_data'])

def display_results(result):
    """Display analysis results in a visually appealing compact layout"""
    overall_score = result['overall_score']
    metrics = result.get('metrics', {})
    metric_names = {
        'skills_match': 'Skills Match',
        'relevant_experience': 'Relevant Experience',
        'education': 'Relevant Education',
        'soft_skills': 'Soft Skills'
    }
    # Score color logic
    def get_color(val):
        if val < 30:
            return "#FF4136"  # red
        elif val < 50:
            return "#FFDC00"  # yellow
        elif val < 80:
            return "#0074D9"  # blue
        else:
            return "#2ecc40"  # green
    score_color = get_color(overall_score)
    # Metrics chart data
    bar_labels = [metric_names.get(m, m.replace('_', ' ').title()) for m in metrics.keys()]
    bar_values = list(metrics.values())
    bar_colors = [get_color(v) for v in bar_values]
    # Two columns: left for score, right for metrics
    left, right = st.columns([1, 2], gap="small")
    with left:
        st.markdown("<h3 style='margin-bottom:0.5em;'>Overall Fit Score</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background:{score_color};color:white;border-radius:1.5em;width:120px;text-align:center;font-size:2.2em;font-weight:700;margin-bottom:1.2em;margin-top:0.2em;'>
                {overall_score}%
            </div>
        """, unsafe_allow_html=True)
    with right:
        # Custom minimal bar chart: each bar is a div with a light background and a colored overlay
        st.markdown("""
            <style>
            .metric-bar-track {background:#f2f2f2;border-radius:12px;height:28px;width:100%;margin-bottom:16px;position:relative;}
            .metric-bar-fill {height:28px;border-radius:12px;position:absolute;top:0;left:0;}
            .metric-bar-label {position:absolute;left:12px;top:4px;font-weight:600;color:#222;font-size:1.05em;z-index:2;}
            </style>
        """, unsafe_allow_html=True)
        for label, value, color in zip(bar_labels, bar_values, bar_colors):
            st.markdown(f"""
                <div class='metric-bar-track'>
                    <div class='metric-bar-label'>{label}</div>
                    <div class='metric-bar-fill' style='width:{value}%;background:{color};'></div>
                </div>
            """, unsafe_allow_html=True)
    # Candidate summary and analysis below
    st.markdown("<h4 style='margin-bottom:0.5em;'>Candidate Summary</h4>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom:1.5em;'>{result.get('candidate_summary', '')}</div>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-bottom:0.5em;'>Analysis</h4>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom:1.5em;'>{re.sub(r'\s+', ' ', result.get('analysis', '')).strip()}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 