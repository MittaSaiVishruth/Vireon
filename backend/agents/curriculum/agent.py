import logging
from typing import Dict, Any
from backend.core.interfaces import BaseAgent
from backend.providers.llm_provider import OllamaProvider
from backend.prompts.curriculum import CURRICULUM_SYSTEM_PROMPT, generate_curriculum_user_prompt

logger = logging.getLogger(__name__)

class CurriculumAgent(BaseAgent):
    """
    Agent responsible for generating a structured JSON syllabus from text chunks.
    """
    def __init__(self):
        self.llm_provider = OllamaProvider()

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expects payload: {"chunks": ["chunk1", ...], "file_path": "..."}
        Returns: {"curriculum": {...}}
        """
        chunks = payload.get("chunks")
        if not chunks or not isinstance(chunks, list):
            raise ValueError("CurriculumAgent requires a list of 'chunks' in the payload.")
            
        logger.info(f"CurriculumAgent received {len(chunks)} chunks for syllabus generation.")
        
        user_prompt = generate_curriculum_user_prompt(chunks)
        
        # Call LLM to generate JSON curriculum
        curriculum_json = await self.llm_provider.generate_json(
            prompt=user_prompt,
            system_prompt=CURRICULUM_SYSTEM_PROMPT
        )
        
        logger.info("Curriculum successfully generated.")
        
        return {
            "status": "success",
            "curriculum": curriculum_json,
            "source_file": payload.get("file_path")
        }
