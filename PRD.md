PRODUCT REQUIREMENTS DOCUMENT (PRD)

Project Name: Vireon Quick Learn

Version: 1.0 (Initial MVP)

Document Status: Draft

Author: Vireon Team

1. Executive Summary
Vision

Build an AI-powered learning platform that automatically converts educational documents into structured, interactive learning experiences.

The initial version, Quick Learn, focuses on allowing a learner to upload a PDF and automatically receive a complete AI-generated course consisting of:

Structured modules
Short lessons
AI-generated summaries
Flashcards
Interactive quizzes
Short narrated videos
Progress tracking
XP & badges

The entire system must run locally using free and open-source technologies, requiring no paid APIs or external services.

2. Problem Statement

Students today face several challenges:

Educational content is often long and difficult to consume.
Existing AI tools generate summaries but not complete learning experiences.
Creating structured learning material manually takes significant time.
Most AI-powered educational platforms rely on paid APIs.
Learners struggle to remain engaged with static documents.

Vireon addresses these problems by automatically transforming educational material into an interactive learning experience.

3. Product Goal

Enable any learner to upload a PDF and automatically generate a complete learning course in under five minutes.

4. Product Objectives

The system should:

Understand uploaded documents.
Identify chapters and concepts.
Organize concepts into lessons.
Generate concise educational scripts.
Produce short narrated videos.
Create summaries.
Generate flashcards.
Generate quizzes.
Track learner progress.
Award XP and badges.
Operate completely offline after initial setup.
5. Product Principles
Principle 1

Zero mandatory paid services.

The MVP must work without:

OpenAI API
Gemini API
Anthropic API
ElevenLabs
Principle 2

Local-first architecture.

All AI inference should initially use:

Ollama
Llama 3
Principle 3

Modular AI.

Every AI component must be replaceable.

Principle 4

Human editable.

Every AI-generated output can be edited before publishing.

Principle 5

Simple user experience.

A learner should generate a course in three clicks:

Upload → Generate → Learn

6. Target Users

Primary

University students
Self-learners
Competitive exam aspirants

Secondary

Teachers
Content creators
Training organizations
7. User Persona
Student

Needs

Quick understanding
Short lessons
Revision material

Pain Points

Long PDFs
Boring notes
Lack of engagement
Teacher

Needs

Convert notes into courses
Save preparation time
8. Core User Journey
Login

↓

Dashboard

↓

Upload PDF

↓

AI Analysis

↓

Course Generated

↓

Course Overview

↓

Lesson

↓

Video

↓

Interactive Quiz

↓

XP Earned

↓

Next Lesson
9. Functional Requirements
Authentication
Local account
Guest mode
Upload

Supported

PDF

Future

PPT
DOCX
URLs
AI Course Generation

Generate

Course title
Description
Modules
Lessons
Learning objectives
Lesson Generation

Each lesson contains:

Title
Summary
Video
Flashcards
Quiz
Key takeaways
Video Generation

Each lesson produces:

Narration
Slides
Captions
Final MP4
Flashcards

AI generates

Question

↓

Answer

Quiz

Generate

MCQ
True/False
Fill blank
Progress

Track

Completed lessons
XP
Badges
Time spent
10. Non-Functional Requirements

Performance

PDF under 100 pages

↓

Course generated within five minutes

Availability

Runs locally

No internet required after model installation

Scalability

Support future cloud deployment

Security

No uploaded files leave user's computer

11. MVP Scope

Included

✅ Upload PDF

✅ Generate course

✅ Generate lessons

✅ Generate summaries

✅ Generate quizzes

✅ Generate flashcards

✅ Generate short videos

✅ XP

✅ Badges

Not Included

❌ Multiplayer

❌ Adventure mode

❌ AI Tutor

❌ Cloud sync

❌ Marketplace

12. AI Workflow
Upload PDF

↓

Extract Text

↓

Clean Text

↓

Detect Chapters

↓

Generate Modules

↓

Generate Lessons

↓

Generate Summary

↓

Generate Quiz

↓

Generate Flashcards

↓

Generate Video Script

↓

Narration

↓

Video Rendering

↓

Course Ready
13. Success Metrics

The MVP is successful when it can:

Convert a PDF into a structured course.
Generate understandable lesson summaries.
Produce working quizzes and flashcards.
Create short lesson videos.
Operate entirely with local models.
Deliver a complete course within five minutes for a typical educational PDF.
14. Initial Technology Stack
Frontend
Flutter
Riverpod
Go Router
Hive
Backend
Python
FastAPI
AI
Ollama
Llama 3 (initial model)
Embeddings
Sentence Transformers
all-MiniLM-L6-v2
OCR
PyMuPDF
Tesseract
Video
MoviePy
FFmpeg
OpenCV
TTS
Piper TTS (preferred)
Edge TTS (development fallback)
Database (Initial)
SQLite

Future

PostgreSQL
Azure SQL / Cosmos DB
15. Future Vision

Quick Learn is the foundation of the Vireon ecosystem.

Future modules will include:

🎮 Adventure Mode
🧪 Interactive Practice Labs
🤖 AI Tutor
📈 Personalized Learning Paths
👩‍🏫 Teacher Workspace
🌐 Course Marketplace
🏢 Enterprise Training