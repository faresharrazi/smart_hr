"""
Mistral LLM Provider

Implementation for Mistral AI models.
"""

import os
from typing import Dict, Any, Optional
from langchain_mistralai import ChatMistralAI
from langchain.schema import HumanMessage
from .base_provider import BaseLLMProvider


class MistralProvider(BaseLLMProvider):
    """Mistral AI provider implementation"""
    
    def __init__(self, model_name: str, temperature: float = 0.3, max_tokens: int = 2000):
        super().__init__(model_name, temperature, max_tokens)
        self.api_key = os.getenv("MISTRAL_API_KEY")
    
    def initialize(self) -> bool:
        """Initialize the Mistral LLM model"""
        try:
            if not self.api_key:
                return False
            
            self.llm = ChatMistralAI(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return True
        except Exception as e:
            print(f"Error initializing Mistral model: {str(e)}")
            return False
    
    def analyze_compatibility(self, job_description: str, cv_text: str, selected_metrics: list) -> Optional[Dict[str, Any]]:
        """Analyze compatibility using Mistral"""
        try:
            if not self.initialize():
                return None
            
            prompt = self.create_prompt(job_description, cv_text, selected_metrics)
            messages = [HumanMessage(content=prompt)]
            
            response = self.llm.invoke(messages)
            self.last_raw_response = response.content  # Store raw response for debugging
            return self.parse_response(response.content)
            
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
        return "mistral-large-latest" 