from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class BaseEvent(BaseModel):
    """Base class for all events in the system."""
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    
class JobStatus:
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Job(BaseModel):
    """Represents an asynchronous task."""
    job_id: str
    task_name: str
    payload: Dict[str, Any]
    status: str = JobStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class BaseEventBus(ABC):
    @abstractmethod
    async def publish(self, event: BaseEvent) -> None:
        pass

    @abstractmethod
    def subscribe(self, event_type: str, handler: callable) -> None:
        pass

class BaseJobQueue(ABC):
    @abstractmethod
    async def enqueue(self, job: Job) -> None:
        pass

    @abstractmethod
    async def dequeue(self) -> Job:
        pass

class BaseAgent(ABC):
    """
    Contract for all AI Agents in Vireon.
    Every agent must implement an asynchronous process method.
    """
    @abstractmethod
    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the given input payload and return a result dictionary.
        Must raise an exception on failure.
        """
        pass

class BaseLLMProvider(ABC):
    """
    Contract for Language Model Providers (Local or Cloud).
    """
    @abstractmethod
    async def generate_json(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        """
        Generates a JSON response from the LLM based on the prompt.
        Must return a parsed dictionary.
        """
        pass
