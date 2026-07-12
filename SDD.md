VIREON SOFTWARE DESIGN DOCUMENT (SDD)

Project: Vireon – Quick Learn MVP

Version: 1.0

Architecture Style: Modular Multi-Agent AI Platform

Deployment: Local (Phase 1)

Target: Windows / Linux / macOS

1. Purpose

This document defines the technical architecture of the Vireon Quick Learn platform.

It explains:

Overall software architecture
Component interactions
AI orchestration
Backend architecture
Frontend architecture
Data flow
Storage
Security
Scalability
2. Design Principles

Every engineering decision follows these principles.

P1 Modular

Every component should be independently replaceable.

P2 Local First

Everything should run locally.

Internet is optional.

P3 AI First

Whenever repetitive work exists,

AI performs it.

P4 Event Driven

Instead of

Step1
↓

Step2
↓

Step3

The platform uses events.

Example

PDF Uploaded

↓

Generate Course Event

↓

Lesson Event

↓

Video Event

Every module reacts independently.

P5 Human Editable

AI never locks content.

Every output is editable.

3. High-Level Architecture
                    Flutter Application
                             │
                             ▼
                    FastAPI Backend
                             │
                             ▼
                     AI Orchestrator
                             │
     ┌──────────┬──────────┬──────────┬──────────┬──────────┐
     ▼          ▼          ▼          ▼          ▼
 Document   Curriculum   Lesson   Assessment  Storyboard
  Agent        Agent      Agent      Agent      Agent
     ▼          ▼          ▼          ▼          ▼
     └──────────┴──────────┴──────────┴──────────┘
                             ▼
                     Course Builder
                             ▼
                      SQLite Database
                             ▼
                    Local File Storage
4. Why an AI Orchestrator?

Without it:

PDF

↓

Python Script

↓

Everything

Difficult to extend.

With Orchestrator:

Upload PDF

↓

AI decides

↓

Which agents execute

↓

Results assembled

Very scalable.

5. AI Orchestrator

This is the brain.

Responsibilities

receive jobs
schedule jobs
call AI agents
monitor execution
retry failures
merge outputs

Pseudo workflow

Upload PDF

↓

Create Job

↓

Job Queue

↓

Run Document Agent

↓

Run Curriculum Agent

↓

Run Lesson Agent

↓

Run Quiz Agent

↓

Run Flashcard Agent

↓

Run Storyboard Agent

↓

Run Video Agent

↓

Assemble Course

↓

Notify Frontend
6. AI Agent Architecture

Every agent follows identical structure.

Input

↓

Analyze

↓

LLM

↓

Validate

↓

Output

Each agent contains

Controller

Service

Prompt

Validator

Output Formatter
7. Agent Specifications
Document Agent

Purpose

Convert uploaded file into structured text.

Input

PDF

Output

Clean Document

Tasks

OCR
Remove headers
Remove page numbers
Detect chapters
Detect headings

Libraries

PyMuPDF

Tesseract

Curriculum Agent

Purpose

Convert document into learning path.

Input

Document

Output

Course

↓

Modules

↓

Lessons

Example

Machine Learning

↓

Module

Regression

↓

Lessons

Linear Regression

Loss Function

Evaluation
Lesson Agent

Generates

explanation
summary
examples
analogy
key takeaways
Assessment Agent

Generates

MCQ

Flashcards

True False

Fill Blank

Drag Drop

Scenario

Reflection

Storyboard Agent

Creates

Scene 1

↓

Narration

↓

Visual Prompt

↓

Animation Prompt

↓

Subtitle

↓

Duration
Video Agent

Uses

MoviePy

FFmpeg

OpenCV

Creates

Lesson.mp4
Course Builder

Collects

Lessons

↓

Videos

↓

Quizzes

↓

Flashcards

↓

Progress

Creates final course.

8. Backend Architecture
API Layer

↓

Business Layer

↓

AI Layer

↓

Storage Layer
API Layer

FastAPI

Routes

Authentication

Upload

Courses

Lessons

Progress

Business Layer

Validation

Authorization

Workflow

AI Layer

All AI agents

Storage Layer

SQLite

Files

Videos

Assets

9. Frontend Architecture

Flutter

Pattern

MVVM

State

Riverpod

Navigation

GoRouter

Storage

Hive

Modules

Authentication

Dashboard

Course

Lesson

Quiz

Progress

Settings
10. Data Flow
Upload PDF

↓

Document Agent

↓

Curriculum Agent

↓

Lesson Agent

↓

Assessment Agent

↓

Storyboard Agent

↓

Video Agent

↓

Course Builder

↓

Database

↓

Flutter UI
11. Job Queue

Every task becomes

Job

Example

JOB

Generate Course

Status

Pending

Running

Completed

Failed

Future

Redis

RabbitMQ

Current

Python Async Queue

12. Storage

Local

uploads/

courses/

videos/

audio/

assets/

cache/

database/
13. AI Provider Layer

Never call Ollama directly.

Instead

Lesson Agent

↓

LLM Provider

↓

Ollama

Future

LLM Provider

↓

OpenAI

↓

Gemini

↓

Claude

↓

DeepSeek

Nothing changes.

14. Error Handling

Every agent returns

{
  "status":"success",

  "output":{}

}

or

{
 "status":"failed",

 "reason":"..."
}

Orchestrator retries.

15. Logging

Every execution

Start

Duration

Tokens

Errors

Model Used

Retry Count

Saved locally.

16. Security

Phase 1

Everything local.

No cloud.

No external APIs.

No data leaves machine.

17. Future Cloud Architecture

Later

Flutter

↓

Azure API

↓

Azure Functions

↓

AI Agents

↓

Azure PostgreSQL

↓

Blob Storage

No frontend changes.

18. Folder Structure
vireon/

├── frontend/
│
├── backend/
│   ├── api/
│   ├── orchestrator/
│   ├── providers/
│   ├── jobs/
│   ├── agents/
│   │   ├── document/
│   │   ├── curriculum/
│   │   ├── lesson/
│   │   ├── assessment/
│   │   ├── storyboard/
│   │   ├── video/
│   │   └── course_builder/
│   ├── models/
│   ├── prompts/
│   ├── services/
│   ├── storage/
│   └── database/
│
├── ai/
│
├── docs/
│
├── tests/
│
└── scripts/