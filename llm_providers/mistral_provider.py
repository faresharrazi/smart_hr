"""
Mistral LLM Provider

Implementation for Mistral AI models using direct HTTP API calls.
"""

import os
import sys
import json
import urllib.request
from typing import Dict, Any, Optional

from .base_provider import BaseLLMProvider

class MistralProvider(BaseLLMProvider):
    """Mistral AI provider implementation using direct HTTP API calls"""
    
    def __init__(self, model_name: str, temperature: float = 0.3, max_tokens: int = 2000):
        super().__init__(model_name, temperature, max_tokens)
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
    
    def initialize(self) -> bool:
        """Initialize the Mistral LLM model"""
        try:
            if not self.api_key:
                return False
            return True
        except Exception as e:
            return False
    
    def analyze_compatibility(self, job_description: str, cv_text: str, selected_metrics: list) -> Optional[Dict[str, Any]]:
        """Analyze compatibility using Mistral via direct HTTP API"""
        try:
            if not self.initialize():
                return None
            
            prompt = self.create_prompt(job_description, cv_text, selected_metrics)
            
            # Prepare the request
            data = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            # Make HTTP request to Mistral API
            json_data = json.dumps(data).encode('utf-8')
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            req = urllib.request.Request(self.api_url, data=json_data, headers=headers, method='POST')
            
            with urllib.request.urlopen(req) as response:
                response_data = response.read()
                api_response = json.loads(response_data.decode('utf-8'))
            
            # Extract the response content
            if 'choices' in api_response and len(api_response['choices']) > 0:
                response_content = api_response['choices'][0]['message']['content']
                self.last_raw_response = response_content
                return self.parse_response(response_content)
            else:
                return None
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                raise Exception("⚠️ Mistral API quota exceeded. Please check your plan and billing details.")
            elif "503" in error_msg or "overloaded" in error_msg.lower():
                raise Exception("⚠️ Mistral API is currently overloaded. Please try again in a few minutes.")
            elif "timeout" in error_msg.lower():
                raise Exception("⚠️ Request timed out. The API is taking too long to respond. Please try again.")
            elif "401" in error_msg or "unauthorized" in error_msg.lower():
                raise Exception("⚠️ Mistral API key is invalid or missing. Please check your API key configuration.")
            else:
                raise Exception(f"Error analyzing compatibility: {error_msg}")
    
    @staticmethod
    def get_available_models() -> list:
        """Get list of available Mistral models"""
        return ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"]
    
    @staticmethod
    def get_default_model() -> str:
        """Get the default Mistral model"""
        return "mistral-small-latest" 