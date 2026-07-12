from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import uuid
import shutil

from backend.db.database import get_db
from backend.db import crud
from backend.core.config import settings
from backend.orchestrator.engine import OrchestratorEngine

api_router = APIRouter()

# We will inject the orchestrator instance here from main.py
orchestrator: OrchestratorEngine = None

@api_router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """
    Uploads a PDF, creates a Course record, and dispatches the document processing job.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    course_id = str(uuid.uuid4())
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, f"{course_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Create DB record
    crud.create_course(db=db, course_id=course_id, title=file.filename)
    
    # Dispatch to orchestrator
    if orchestrator:
        await orchestrator.dispatch_job("process_document", {
            "course_id": course_id,
            "file_path": file_path
        })
        
    return {"status": "processing", "course_id": course_id, "message": "Document uploaded and processing started."}

@api_router.get("/courses/{course_id}")
async def get_course(course_id: str, db: Session = Depends(get_db)):
    """
    Fetches the full course hierarchy and content from the database.
    """
    course = crud.get_full_course_dict(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@api_router.get("/videos/{filename}")
async def get_video(filename: str):
    """
    Serves the generated video file.
    """
    video_path = os.path.join(settings.UPLOAD_DIR, "videos", filename)
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_path, media_type="video/mp4")
