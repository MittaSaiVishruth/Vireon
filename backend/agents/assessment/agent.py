import logging
import json
from typing import Dict, Any
from backend.core.interfaces import BaseAgent
from backend.providers.llm_provider import OllamaProvider
from backend.prompts.assessment import ASSESSMENT_SYSTEM_PROMPT, generate_assessment_user_prompt

logger = logging.getLogger(__name__)

class AssessmentAgent(BaseAgent):
    """
    Agent responsible for generating MCQs and Flashcards based on lesson content.
    """
    def __init__(self):
        self.llm_provider = OllamaProvider()

    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expects payload: {
            "lesson_id": "...", 
            "lesson_title": "...", 
            "lesson_content": {...} # From LessonAgent
        }
        Returns: {"lesson_id": "...", "assessment": {...}}
        """
        lesson_id = payload.get("lesson_id")
        title = payload.get("lesson_title")
        content = payload.get("lesson_content")
        
        if not content:
            raise ValueError("AssessmentAgent requires 'lesson_content' in payload.")
            
        logger.info(f"AssessmentAgent processing assessments for lesson: {title}")
        
        # Serialize the JSON content into a string for the prompt
        content_str = json.dumps(content, indent=2)
        user_prompt = generate_assessment_user_prompt(content_str)
        
        assessment_json = await self.llm_provider.generate_json(
            prompt=user_prompt,
            system_prompt=ASSESSMENT_SYSTEM_PROMPT
        )
        
        logger.info(f"Assessments generated for lesson: {title}")
        
        return {
            "status": "success",
            "lesson_id": lesson_id,
            "lesson_title": title,
            "assessment": assessment_json
        }
