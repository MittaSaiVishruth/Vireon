import json
import logging
from typing import Dict, Any
import ollama
from backend.core.interfaces import BaseLLMProvider
from backend.core.config import settings

logger = logging.getLogger(__name__)

class OllamaProvider(BaseLLMProvider):
    """Implementation of the LLM Provider using local Ollama."""
    
    def __init__(self, model_name: str = None):
        self.model = model_name or settings.DEFAULT_LLM_MODEL
        # Ollama python client automatically uses localhost:11434 by default

    async def generate_json(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        """
        Calls the Ollama model and enforces JSON formatting.
        """
        logger.info(f"Calling Ollama model: {self.model}")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        messages.append({"role": "user", "content": prompt})

        try:
            # We use the sync client wrapped in a thread or we can use AsyncClient from ollama
            # For simplicity, we use AsyncClient
            client = ollama.AsyncClient(host=settings.OLLAMA_BASE_URL)
            response = await client.chat(
                model=self.model,
                messages=messages,
                format='json'  # Force JSON output
            )
            
            content = response['message']['content']
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Ollama output as JSON: {e}")
            logger.debug(f"Raw output: {content}")
            raise ValueError("LLM did not return valid JSON.") from e
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise
