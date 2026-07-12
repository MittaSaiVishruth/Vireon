from typing import Any, Dict
from backend.core.interfaces import BaseEvent

class PdfUploadedEvent(BaseEvent):
    """Fired when a user uploads a PDF."""
    pass

class DocumentProcessedEvent(BaseEvent):
    """Fired when the Document Agent successfully processes the PDF into chunks."""
    pass

class AgentFailedEvent(BaseEvent):
    """Fired when an agent fails to complete its processing."""
    pass

class DocumentProcessedEvent(BaseEvent):
    """Fired when a document is processed into chunks."""
    pass

class CurriculumGeneratedEvent(BaseEvent):
    """Fired when the syllabus JSON is generated."""
    pass

class LessonGeneratedEvent(BaseEvent):
    """Fired when the Lesson Agent generates a lesson JSON."""
    pass

class AssessmentGeneratedEvent(BaseEvent):
    """Fired when the Assessment Agent generates quizzes and flashcards."""
    pass

class StoryboardGeneratedEvent(BaseEvent):
    """Fired when the Storyboard Agent generates the scene JSON."""
    pass

class VideoGeneratedEvent(BaseEvent):
    """Fired when the Video Agent completes rendering the MP4."""
    pass
