from sqlalchemy.orm import Session
from typing import Dict, Any
import json
from . import models

def create_course(db: Session, course_id: str, title: str = "Generating Course..."):
    db_course = models.Course(id=course_id, title=title, status="processing")
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_course(db: Session, course_id: str):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def update_course_status(db: Session, course_id: str, status: str, title: str = None):
    course = get_course(db, course_id)
    if course:
        course.status = status
        if title:
            course.title = title
        db.commit()
        db.refresh(course)
    return course

def save_syllabus(db: Session, course_id: str, syllabus: Dict[str, Any]):
    """Creates Modules and Lessons from the generated Syllabus JSON."""
    course = get_course(db, course_id)
    if not course:
        return
        
    course.title = syllabus.get("course_title", course.title)
    
    for mod in syllabus.get("modules", []):
        db_module = models.Module(
            id=mod["module_id"], 
            course_id=course_id, 
            title=mod["module_title"]
        )
        db.add(db_module)
        
        for less in mod.get("lessons", []):
            db_lesson = models.Lesson(
                id=less["lesson_id"],
                module_id=mod["module_id"],
                title=less["lesson_title"],
                description=less["description"]
            )
            db.add(db_lesson)
            
    db.commit()

def update_lesson_content(db: Session, lesson_id: str, content: Dict[str, Any]):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if lesson:
        lesson.content_json = json.dumps(content)
        db.commit()

def update_lesson_assessment(db: Session, lesson_id: str, assessment: Dict[str, Any]):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if lesson:
        lesson.assessment_json = json.dumps(assessment)
        db.commit()

def update_lesson_storyboard(db: Session, lesson_id: str, storyboard: Dict[str, Any]):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if lesson:
        lesson.storyboard_json = json.dumps(storyboard)
        db.commit()

def update_lesson_video(db: Session, lesson_id: str, video_path: str):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if lesson:
        lesson.video_path = video_path
        db.commit()

def get_full_course_dict(db: Session, course_id: str) -> Dict[str, Any]:
    course = get_course(db, course_id)
    if not course:
        return None
        
    modules_list = []
    for m in course.modules:
        lessons_list = []
        for l in m.lessons:
            lessons_list.append({
                "lesson_id": l.id,
                "title": l.title,
                "description": l.description,
                "content": json.loads(l.content_json) if l.content_json else None,
                "assessment": json.loads(l.assessment_json) if l.assessment_json else None,
                "storyboard": json.loads(l.storyboard_json) if l.storyboard_json else None,
                "video_path": l.video_path
            })
        modules_list.append({
            "module_id": m.id,
            "title": m.title,
            "lessons": lessons_list
        })
        
    return {
        "course_id": course.id,
        "title": course.title,
        "status": course.status,
        "modules": modules_list
    }
