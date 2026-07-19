import asyncio
from typing import Dict, List, Callable
from backend.core.interfaces import BaseEventBus, BaseJobQueue, BaseEvent, Job

class InMemoryEventBus(BaseEventBus):
    """Simple in-memory event bus for local MVP. Maps event_type to list of callbacks."""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    async def publish(self, event: BaseEvent) -> None:
        event_type = event.event_type
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                # Handlers should be async functions
                asyncio.create_task(handler(event))

    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        if event_type in self._subscribers and handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)

class AsyncJobQueue(BaseJobQueue):
    """AsyncIO queue implementation for local job execution."""
    def __init__(self):
        self._queue = asyncio.Queue()

    async def enqueue(self, job: Job) -> None:
        await self._queue.put(job)

    async def dequeue(self) -> Job:
        job = await self._queue.get()
        return job
    
    def task_done(self) -> None:
        self._queue.task_done()
