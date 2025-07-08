"""
Configuration

Application configuration and settings management.
"""

import os


class Config:
    """Application configuration"""
    
    def __init__(self):
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
    
    def validate_api_keys(self, provider: str) -> bool:
        """Validate API key for Mistral only"""
        return bool(self.mistral_api_key)
    
    def get_missing_api_key_message(self, provider: str) -> str:
        """Get error message for missing Mistral API key"""
        return "MISTRAL_API_KEY not found. Please add it to your environment variables." 