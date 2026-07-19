#  Vireon

<div align="center">

### AI-Powered Educational Content Generation Platform

Transform PDFs, documents, and educational resources into professionally designed interactive courses, videos, quizzes, flashcards, and learning experiences using AI.

**Current Version:** Phase 5 – Educational Rendering Engine (ERE)

</div>

---

#  Overview

Vireon is an AI-native educational platform that converts educational content into structured and interactive learning experiences.

Instead of manually creating courses, users simply upload a document and Vireon automatically:

-  Understands the document
-  Builds a curriculum
-  Generates lessons
-  Creates storyboards
-  Produces educational visuals
-  Generates lesson videos
-  Creates quizzes and flashcards
-  Packages everything into a complete course

---

#  Current Features

- User Authentication
- Project Dashboard
- Course Management
- PDF Upload
- AI Course Generation Pipeline
- Storyboard Generation
- Educational Rendering Engine
- Interactive Course Viewer
- Lesson Notes
- Flashcards
- Quizzes
- Download Center
- AI Generation Journey
- Responsive User Interface

---

#  Tech Stack

## Frontend

- React
- TypeScript
- Tailwind CSS
- Vite
- React Router
- Framer Motion
- Lucide Icons

---

## Backend

- FastAPI
- Python 3.11+
- Pydantic
- SQLAlchemy
- SQLite (Development)

---

## AI

- Ollama
- Llama 3
- Local AI Inference

---

## Educational Rendering

- HTML/CSS Templates
- Tailwind CSS
- Playwright
- Mermaid
- Graphviz
- Plotly
- Shiki
- KaTeX
- Manim
- FFmpeg

---

# Prerequisites

Install the following software before running the project.

---

## 1. Git

Download:

https://git-scm.com/

Verify

```bash
git --version
```

---

## 2. Python 3.11+

Download:

https://python.org

Verify

```bash
python --version
```

---

## 3. Node.js (LTS)

Download:

https://nodejs.org/

Verify

```bash
node -v

npm -v
```

---

## 4. FFmpeg

Required for video generation.

Download

https://ffmpeg.org/

Verify

```bash
ffmpeg -version
```

---

## 5. Ollama

Download

https://ollama.com

Verify

```bash
ollama --version
```

Pull the required model

```bash
ollama pull llama3
```

Run

```bash
ollama serve
```

---

## 6. Playwright

Install browser

```bash
playwright install
```

---

## 7. Visual Studio Code

Recommended Extensions

- Python
- Pylance
- ESLint
- Tailwind CSS IntelliSense
- Prettier
- GitLens

---

# ⚙ Backend Setup

Navigate

```bash
cd backend
```

Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Copy Environment File

```bash
cp .env.example .env
```

Configure

```text
DATABASE_URL=

OLLAMA_BASE_URL=

MODEL_NAME=llama3

SECRET_KEY=

LOG_LEVEL=
```

Run

```bash
uvicorn app.main:app --reload
```

Backend

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

---

#  Frontend Setup

Navigate

```bash
cd frontend
```

Install packages

```bash
npm install
```

Create

```
.env
```

Example

```text
VITE_API_URL=http://localhost:8000
```

Run

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

---

# 🗄 Database

Development

SQLite

Migration

```bash
alembic upgrade head
```

---

# Running the Project

## Terminal 1

Backend

```bash
cd backend

uvicorn app.main:app --reload
```

---

## Terminal 2

Frontend

```bash
cd frontend

npm run dev
```

---

## Terminal 3

Ollama

```bash
ollama serve
```

---

Open

```
http://localhost:5173
```

---

# Workflow

```
Login

↓

Upload PDF

↓

AI Generation Journey

↓

Curriculum Generation

↓

Storyboard Generation

↓

Educational Rendering

↓

Video Composition

↓

Interactive Course

↓

Download
```

---

# AI Pipeline

```
Upload

↓

Document Parser

↓

Curriculum Agent

↓

Lesson Agent

↓

Storyboard Agent

↓

Scene Planner

↓

Educational Rendering Engine

↓

Video Composer

↓

Quality Review

↓

Course Package
```

---

# Build

Frontend

```bash
npm run build
```

Backend

```bash
python -m build
```

---

# Testing

Frontend

```bash
npm test
```

Backend

```bash
pytest
```

---

# Development Guidelines

- Use meaningful commit messages.
- Follow PEP8 for Python.
- Use ESLint + Prettier.
- Keep components modular.
- Prefer reusable UI components.
- Add documentation for new modules.

---

# Roadmap

## Phase 5

- Educational Rendering Engine
- AI Course Generation
- Interactive Course Viewer
- Storyboard Engine
- Download Center

##  Phase 6

- Premium UI/UX
- AI Mission Control
- Redesigned Dashboard
- Course Workspace
- Storyboard Viewer
- Advanced Navigation
- Responsive Design
- Animations
- Design System

##  Future

- AI Learning Companion
- Adaptive Learning
- Creator Studio
- Marketplace
- Enterprise Platform
- Plugin SDK

---

# 📄 License

This project is released under the MIT License.

---

#  Built With

- FastAPI
- React
- Tailwind CSS
- Ollama
- Playwright
- FFmpeg
- Manim

---

<div align="center">

### Vireon

**Transforming static documents into intelligent learning experiences.**

</div>
