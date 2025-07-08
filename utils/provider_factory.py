"""
Provider Factory

Factory class to create and manage the Mistral LLM provider.
"""

from typing import Dict, Type
from llm_providers.base_provider import BaseLLMProvider
from llm_providers.mistral_provider import MistralProvider

class ProviderFactory:
    """Factory for creating the Mistral LLM provider"""
    
    _providers: Dict[str, Type[BaseLLMProvider]] = {
        "Mistral": MistralProvider
    }
    
    @classmethod
    def get_provider(cls, provider_name: str, model_name: str, **kwargs) -> BaseLLMProvider:
        """Get a provider instance"""
        if provider_name not in cls._providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        
        provider_class = cls._providers[provider_name]
        return provider_class(model_name, **kwargs)
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Get list of available providers (only Mistral)"""
        return ["Mistral"]
    
    @classmethod
    def get_provider_models(cls, provider_name: str) -> list:
        """Get available models for Mistral"""
        return MistralProvider.get_available_models()
    
    @classmethod
    def get_default_model(cls, provider_name: str) -> str:
        """Get default model for Mistral"""
        return MistralProvider.get_default_model() 