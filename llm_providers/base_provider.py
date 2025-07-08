"""
Base LLM Provider

Defines the interface that all LLM providers must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union


class BaseLLMProvider(ABC):
    """Base class for all LLM providers"""
    
    def __init__(self, model_name: str, temperature: float = 0.3, max_tokens: int = 2000):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.llm = None
        self.last_raw_response = None  # For debugging raw LLM output
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the LLM model"""
        pass
    
    @abstractmethod
    def analyze_compatibility(self, job_description: str, cv_text: str, selected_metrics: list) -> Optional[Dict[str, Any]]:
        """Analyze compatibility between job description and CV"""
        pass
    
    def create_prompt(self, job_description: str, cv_text: str, selected_metrics: list) -> str:
        """Create the analysis prompt"""
        metrics_text = ", ".join(selected_metrics)
        
        prompt = f"""
You are an expert HR analyst. Analyze the compatibility between a job description and a candidate's CV.
Focus on these metrics: {metrics_text}
Respond ONLY with a valid JSON object, no markdown, no explanations, no extra text, no code block formatting.
Provide your analysis in the following JSON format:
{{
    \"overall_score\": <score_0_100>,
    \"reasoning\": \"<detailed_paragraph_explaining_the_score_and_reasoning>\",
    \"metrics\": {{
        \"skills_match\": <score_0_100>,
        \"experience_level\": <score_0_100>,
        \"overall_fit\": <score_0_100>
    }}
}}
Be objective and provide specific examples from both documents to support your analysis.

Job Description:
{job_description}

Candidate CV:
{cv_text}

Please analyze the compatibility focusing on: {metrics_text}
"""
        return prompt
    
    def parse_response(self, response_content: str) -> Union[dict, None]:
        """Parse the LLM response into structured format. Returns None if parsing fails."""
        import json
        import re
        self.last_raw_response = response_content  # Always store for debugging
        try:
            # Try direct JSON parse first
            return json.loads(response_content)
        except Exception:
            # Try to extract JSON block from the response
            match = re.search(r'\{[\s\S]*\}', response_content)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception:
                    pass
        # If parsing fails, return None
        return None 