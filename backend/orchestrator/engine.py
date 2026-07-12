import asyncio
import uuid
import logging
from typing import Dict, Any, Type
from backend.core.interfaces import BaseEvent, Job, JobStatus, BaseAgent
from backend.orchestrator.events import AgentFailedEvent
from backend.orchestrator.queue import AsyncJobQueue, InMemoryEventBus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrchestratorEngine:
    def __init__(self):
        self.event_bus = InMemoryEventBus()
        self.job_queue = AsyncJobQueue()
        self._agents: Dict[str, Type[BaseAgent]] = {}
        self._worker_task = None
        
    def register_agent(self, task_name: str, agent_class: Type[BaseAgent]) -> None:
        """Register an agent class for a specific task type."""
        self._agents[task_name] = agent_class
        logger.info(f"Registered agent {agent_class.__name__} for task {task_name}")

    async def dispatch_job(self, task_name: str, payload: Dict[str, Any]) -> str:
        """Create and enqueue a new job."""
        job_id = str(uuid.uuid4())
        job = Job(
            job_id=job_id,
            task_name=task_name,
            payload=payload
        )
        await self.job_queue.enqueue(job)
        logger.info(f"Enqueued job {job_id} for task {task_name}")
        return job_id

    async def _worker_loop(self):
        """Continuously pulls jobs from the queue and executes them using the appropriate agent."""
        logger.info("Orchestrator worker loop started.")
        while True:
            job = await self.job_queue.dequeue()
            job.status = JobStatus.RUNNING
            logger.info(f"Starting job {job.job_id} ({job.task_name})")
            
            try:
                if job.task_name not in self._agents:
                    raise ValueError(f"No agent registered for task: {job.task_name}")
                
                # Instantiate the agent and process
                agent = self._agents[job.task_name]()
                result = await agent.process(job.payload)
                
                job.status = JobStatus.COMPLETED
                job.result = result
                
                # Publish completion event
                event_type_map = {
                    "process_document": "document_processed",
                    "generate_curriculum": "curriculum_generated",
                    "generate_lesson": "lesson_generated",
                    "generate_assessment": "assessment_generated",
                    "generate_storyboard": "storyboard_generated",
                    "generate_video": "video_generated"
                }
                if job.task_name in event_type_map:
                    merged_payload = {**job.payload, **result}
                    await self.event_bus.publish(BaseEvent(
                        event_id=str(uuid.uuid4()),
                        event_type=event_type_map[job.task_name],
                        payload=merged_payload
                    ))
                    
                logger.info(f"Job {job.job_id} completed successfully.")
                
            except Exception as e:
                job.status = JobStatus.FAILED
                job.error = str(e)
                logger.error(f"Job {job.job_id} failed: {e}")
                
                # Publish failure event
                await self.event_bus.publish(AgentFailedEvent(
                    event_id=str(uuid.uuid4()),
                    event_type="agent_failed",
                    payload={"job_id": job.job_id, "error": str(e), "task_name": job.task_name}
                ))
            finally:
                self.job_queue.task_done()

    def start(self):
        """Start the background worker."""
        if self._worker_task is None:
            self._worker_task = asyncio.create_task(self._worker_loop())
            
    async def stop(self):
        """Stop the background worker."""
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                logger.info("Orchestrator worker loop stopped.")
