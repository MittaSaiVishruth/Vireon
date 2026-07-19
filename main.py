import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from contextlib import asynccontextmanager

from backend.db.database import Base, engine, SessionLocal
from backend.db import crud
from backend.api import router

from backend.orchestrator.engine import OrchestratorEngine
from backend.agents.document.agent import DocumentAgent
from backend.agents.curriculum.agent import CurriculumAgent
from backend.agents.lesson.agent import LessonAgent
from backend.agents.assessment.agent import AssessmentAgent
from backend.agents.storyboard.agent import StoryboardAgent
from backend.agents.video.agent import VideoAgent

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize Orchestrator
orchestrator = OrchestratorEngine()
orchestrator.register_agent("process_document", DocumentAgent)
orchestrator.register_agent("generate_curriculum", CurriculumAgent)
orchestrator.register_agent("generate_lesson", LessonAgent)
orchestrator.register_agent("generate_assessment", AssessmentAgent)
orchestrator.register_agent("generate_storyboard", StoryboardAgent)
orchestrator.register_agent("generate_video", VideoAgent)

# Inject orchestrator into router
router.orchestrator = orchestrator

# A simple wrapper to update the DB asynchronously without blocking the event loop
async def _run_db_update(func, *args, **kwargs):
    db = SessionLocal()
    try:
        # Run the synchronous CRUD operation in a thread pool
        await asyncio.to_thread(func, db, *args, **kwargs)
    finally:
        db.close()

# Define Orchestration Event Hooks (These bridge the gap between agents and the DB/Next Jobs)
async def on_document_processed(event):
    payload = event.payload
    course_id = payload.get("course_id")
    chunks = payload.get("chunks")
    file_path = payload.get("file_path")
    # Dispatch next job
    await orchestrator.dispatch_job("generate_curriculum", {
        "course_id": course_id,
        "chunks": chunks,
        "file_path": file_path
    })

async def on_curriculum_generated(event):
    payload = event.payload
    course_id = payload.get("course_id")
    syllabus = payload.get("curriculum")
    chunks = payload.get("chunks")
    
    # Save Syllabus to DB
    await _run_db_update(crud.save_syllabus, course_id, syllabus)
    
    # Dispatch Lesson jobs for each lesson in the syllabus
    for module in syllabus.get("modules", []):
        for lesson in module.get("lessons", []):
            await orchestrator.dispatch_job("generate_lesson", {
                "course_id": course_id,
                "lesson_id": lesson.get("lesson_id"),
                "lesson_title": lesson.get("lesson_title"),
                "description": lesson.get("description"),
                "source_chunks": chunks # Passing all chunks to the lesson agent for context
            })

async def on_lesson_generated(event):
    payload = event.payload
    course_id = payload.get("course_id")
    lesson_id = payload.get("lesson_id")
    content = payload.get("content")
    
    # Update DB
    await _run_db_update(crud.update_lesson_content, lesson_id, content)
    
    # Dispatch Assessment and Storyboard jobs concurrently
    await orchestrator.dispatch_job("generate_assessment", {
        "course_id": course_id,
        "lesson_id": lesson_id,
        "lesson_title": payload.get("lesson_title"),
        "lesson_content": content
    })
    await orchestrator.dispatch_job("generate_storyboard", {
        "course_id": course_id,
        "lesson_id": lesson_id,
        "lesson_title": payload.get("lesson_title"),
        "lesson_content": content
    })

async def on_assessment_generated(event):
    payload = event.payload
    lesson_id = payload.get("lesson_id")
    assessment = payload.get("assessment")
    await _run_db_update(crud.update_lesson_assessment, lesson_id, assessment)

async def on_storyboard_generated(event):
    payload = event.payload
    lesson_id = payload.get("lesson_id")
    storyboard = payload.get("storyboard")
    await _run_db_update(crud.update_lesson_storyboard, lesson_id, storyboard)
    
    # Dispatch Video Job
    await orchestrator.dispatch_job("generate_video", {
        "course_id": payload.get("course_id"),
        "lesson_id": lesson_id,
        "lesson_title": payload.get("lesson_title"),
        "storyboard": storyboard
    })

async def on_video_generated(event):
    payload = event.payload
    lesson_id = payload.get("lesson_id")
    video_path = payload.get("video_path")
    course_id = payload.get("course_id")
    
    # The path saved should be relative so the API can serve it
    filename = os.path.basename(video_path)
    await _run_db_update(crud.update_lesson_video, lesson_id, filename)
    
    # For MVP, we can just mark the course as completed here 
    # (In reality, we'd check if all videos are done)
    await _run_db_update(crud.update_course_status, course_id, "completed")

# Subscribe to events
orchestrator.event_bus.subscribe("document_processed", on_document_processed)
orchestrator.event_bus.subscribe("curriculum_generated", on_curriculum_generated)
orchestrator.event_bus.subscribe("lesson_generated", on_lesson_generated)
orchestrator.event_bus.subscribe("assessment_generated", on_assessment_generated)
orchestrator.event_bus.subscribe("storyboard_generated", on_storyboard_generated)
orchestrator.event_bus.subscribe("video_generated", on_video_generated)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the background orchestrator loop
    orchestrator.start()
    print("Vireon Orchestrator Started.")
    yield
    # Shutdown: Stop the orchestrator
    print("Stopping Vireon Orchestrator...")
    await orchestrator.stop()

app = FastAPI(title="Vireon Learning OS API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For MVP, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
