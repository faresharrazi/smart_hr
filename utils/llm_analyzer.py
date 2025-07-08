"""
LLM Analyzer Utility

Handles prompt construction, LLM call, and robust JSON parsing for candidate analysis.
"""
import json
import re
from langchain_mistralai import ChatMistralAI
from langchain.schema import HumanMessage

def analyze_candidate(job_description: str, structured_cv: str) -> dict:
    """Analyze candidate using Mistral (small) and return parsed JSON result."""
    prompt = f"""
You are an expert HR analyst with 15+ years of experience in talent acquisition and recruitment. Your task is to provide an accurate, unbiased assessment of candidate-job fit.

ANALYSIS GUIDELINES:
1. Be objective and fair - don't artificially inflate or deflate scores
2. Consider both direct matches and transferable skills
3. Weight experience more heavily than education for senior roles
4. Consider industry context and role requirements
5. Acknowledge potential for growth and learning

SCORING CRITERIA:
- Overall Score: Weighted average considering role seniority and requirements
- Skills Match (0-100): Direct technical/functional skill alignment
- Relevant Experience (0-100): Industry/role-specific experience duration and quality
- Education (0-100): Degree relevance, certifications, continuous learning
- Soft Skills (0-100): Communication, leadership, adaptability, cultural fit

SCORING GUIDELINES:
- 90-100: Exceptional fit, exceeds requirements
- 80-89: Strong fit, meets all key requirements
- 70-79: Good fit, meets most requirements with minor gaps
- 60-69: Moderate fit, meets some requirements, needs development
- 50-59: Limited fit, significant gaps but potential
- Below 50: Poor fit, major misalignment

Job Description:
{job_description}

Candidate CV (Structured):
{structured_cv}

Return ONLY a valid JSON object with these exact fields:
{{
    "overall_score": <integer 0-100>,
    "metrics": {{
        "skills_match": <integer 0-100>,
        "relevant_experience": <integer 0-100>,
        "education": <integer 0-100>,
        "soft_skills": <integer 0-100>
    }},
    "candidate_summary": "<2-3 sentence summary of candidate background>",
    "analysis": "<detailed paragraph explaining the overall score, key strengths, areas of concern, and specific reasoning for each metric score>"
}}

IMPORTANT: Respond ONLY with the JSON object. No extra text, no markdown, no code blocks.
"""
    llm = ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.2,
        max_tokens=1500
    )
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    raw = response.content
    # Try to parse JSON
    try:
        result = json.loads(raw)
    except Exception:
        match = re.search(r'\{[\s\S]*\}', raw)
        if match:
            try:
                result = json.loads(match.group(0))
            except Exception:
                raise ValueError(f"❌ Could not parse LLM response as JSON. Raw output:\n{raw}")
        else:
            raise ValueError(f"❌ Could not parse LLM response as JSON. Raw output:\n{raw}")
    return result 