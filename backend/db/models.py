from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.database import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String, default="processing")
    
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")

class Module(Base):
    __tablename__ = "modules"
    id = Column(String, primary_key=True, index=True)
    course_id = Column(String, ForeignKey("courses.id"))
    title = Column(String)
    
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(String, primary_key=True, index=True)
    module_id = Column(String, ForeignKey("modules.id"))
    title = Column(String)
    description = Column(Text, nullable=True)
    
    # Store JSON strings for MVP simplicity
    content_json = Column(Text, nullable=True)
    assessment_json = Column(Text, nullable=True)
    storyboard_json = Column(Text, nullable=True)
    video_path = Column(String, nullable=True)
    
    module = relationship("Module", back_populates="lessons")
