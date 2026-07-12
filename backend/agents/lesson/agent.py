import logging
from typing import Dict, Any
from backend.core.interfaces import BaseAgent
from backend.providers.llm_provider import OllamaProvider
from backend.prompts.lesson import LESSON_SYSTEM_PROMPT, generate_lesson_user_prompt

logger = logging.getLogger(__name__)

class LessonAgent(BaseAgent):
    """
    Agent responsible for generating educational content for a specific lesson.
    """
    def __init__(self):
        self.llm_provider = OllamaProvider()

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expects payload: {
            "lesson_id": "...", 
            "lesson_title": "...", 
            "description": "...", 
            "source_chunks": [...]
        }
        Returns: {"lesson_id": "...", "content": {...}}
        """
        lesson_id = payload.get("lesson_id")
        title = payload.get("lesson_title")
        description = payload.get("description")
        source_chunks = payload.get("source_chunks", [])
        
        if not title or not source_chunks:
            raise ValueError("LessonAgent requires 'lesson_title' and 'source_chunks' in payload.")
            
        logger.info(f"LessonAgent processing lesson: {title}")
        
        # Combine source chunks into a single text block
        source_text = "\n\n".join(source_chunks)
        user_prompt = generate_lesson_user_prompt(title, description, source_text)
        
        lesson_json = await self.llm_provider.generate_json(
            prompt=user_prompt,
            system_prompt=LESSON_SYSTEM_PROMPT
        )
        
        logger.info(f"Lesson content generated for: {title}")
        
        return {
            "status": "success",
            "lesson_id": lesson_id,
            "lesson_title": title,
            "content": lesson_json
        }
