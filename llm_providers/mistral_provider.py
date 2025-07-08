"""
Mistral LLM Provider

Implementation for Mistral AI models.
"""

import os
import sys
from typing import Dict, Any, Optional

# Debug imports
print("Starting Mistral provider imports...")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path[:3]}...")

# Try to import langchain_mistralai with better error handling
try:
    from langchain_mistralai import ChatMistralAI
    print("✓ langchain_mistralai imported successfully")
except ImportError as e:
    print(f"✗ Error importing langchain_mistralai: {e}")
    print(f"Available modules: {[m for m in sys.modules.keys() if 'langchain' in m.lower() or 'mistral' in m.lower()]}")
    raise ImportError(f"langchain_mistralai module not found. Please ensure it's installed: pip install langchain-mistralai. Error: {e}")

# Try to import langchain schema
try:
    from langchain.schema import HumanMessage
    print("✓ langchain.schema imported successfully")
except ImportError as e:
    print(f"✗ Error importing langchain.schema: {e}")
    raise ImportError(f"langchain.schema module not found. Please ensure langchain is installed: pip install langchain. Error: {e}")

from .base_provider import BaseLLMProvider

print("✓ All Mistral provider imports successful")


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