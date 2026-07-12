VIREON DETAILED DESIGN DOCUMENT (DDD)
Volume 1 — Core System Design

Document Version: 1.0

Project: Vireon AI Learning Operating System (VAIOS)

Module: Core System

Status: Design Approved

Table of Contents
1. Introduction
2. System Philosophy
3. Overall Architecture
4. Core Components
5. Startup Lifecycle
6. Repository Structure
7. Configuration Management
8. Event Bus Architecture
9. AI Orchestrator
10. Shared Memory Layer
11. Learning Graph Engine
12. LLM Provider Layer
13. Job Management
14. Storage System
15. Logging Framework
16. Error Handling
17. Security Model
18. Performance Requirements
19. Coding Standards
20. Future Scalability
Chapter 1 — Introduction
Purpose

The Core System provides the foundation for every module within Vireon.

All future components—including Quick Learn, Adventure Mode, Practice Labs, AI Tutor, Personalization, Creator Studio, and Marketplace—must integrate through this layer.

No feature should bypass the Core System.

Goals

The system must be:

Modular
AI-native
Local-first
Event-driven
Extensible
Observable
Maintainable
Chapter 2 — System Philosophy

Vireon follows one principle:

Every educational document can become an interactive learning experience.

The system is therefore not designed around PDFs.

It is designed around knowledge transformation.

Input can eventually become:

PDF

PPT

DOCX

Markdown

Books

YouTube

Web Pages

Research Papers

Lecture Notes

Everything enters the same pipeline.

Chapter 3 — Overall Architecture
                     Flutter Desktop/Mobile
                              │
                              ▼
                     FastAPI Application
                              │
                     REST + WebSocket API
                              │
                              ▼
                    AI Orchestrator Engine
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
 Planner Engine       Event Bus Engine     Shared Memory
        │                     │                     │
        └─────────────┬───────┴─────────────┬───────┘
                      ▼                     ▼
              Learning Graph Engine   Job Manager
                      │
             Specialized AI Agents
                      │
              Course Publisher
                      │
            SQLite + Local Storage
Chapter 4 — Core Components

The system consists of twelve primary subsystems.

Component	Responsibility
Flutter UI	User interaction
FastAPI	API gateway
Planner Engine	Determines learning strategy
AI Orchestrator	Coordinates all agents
Event Bus	Internal communication
Shared Memory	Context management
Learning Graph	Knowledge relationships
Job Manager	Background execution
LLM Provider	Local model abstraction
Course Publisher	Assemble final course
SQLite	Structured data
Local Storage	Files and media

Each subsystem must remain independently replaceable.

Chapter 5 — Startup Lifecycle
Application Starts

↓

Load Configuration

↓

Verify Required Directories

↓

Initialize Logger

↓

Initialize SQLite

↓

Initialize Shared Memory

↓

Initialize Event Bus

↓

Initialize Job Manager

↓

Initialize LLM Provider

↓

Verify Ollama Connection

↓

Load Models

↓

Register AI Agents

↓

Start FastAPI

↓

System Ready
Chapter 6 — Repository Structure
vireon/

├── frontend/
│   ├── lib/
│   ├── assets/
│   ├── widgets/
│   ├── screens/
│   ├── providers/
│   └── themes/
│
├── backend/
│   ├── api/
│   ├── orchestrator/
│   ├── planner/
│   ├── events/
│   ├── memory/
│   ├── graph/
│   ├── jobs/
│   ├── providers/
│   ├── database/
│   ├── storage/
│   ├── config/
│   └── utils/
│
├── agents/
│   ├── document/
│   ├── curriculum/
│   ├── lesson/
│   ├── assessment/
│   ├── experience/
│   ├── storyboard/
│   ├── media/
│   ├── qa/
│   └── publisher/
│
├── prompts/
│
├── models/
│
├── tests/
│
├── docs/
│
└── scripts/
Chapter 7 — Configuration Management

All runtime configuration is centralized.

config/

system.yaml

models.yaml

prompts.yaml

storage.yaml

logging.yaml

Example:

app:
  name: Vireon

llm:
  provider: ollama
  model: llama3

video:
  max_duration: 120

lesson:
  max_words: 250

No values should be hardcoded.

Chapter 8 — Event Bus Architecture

The system communicates only through events.

PDF_UPLOADED

↓

DOCUMENT_PARSED

↓

CURRICULUM_CREATED

↓

LESSONS_CREATED

↓

ASSESSMENTS_CREATED

↓

VIDEOS_CREATED

↓

COURSE_READY

↓

COURSE_PUBLISHED

Agents subscribe to events.

They never directly invoke one another.

Benefits:

loose coupling
easier debugging
future distributed execution
Chapter 9 — AI Orchestrator

The AI Orchestrator is responsible for workflow execution.

Responsibilities:

register agents
schedule tasks
manage retries
collect outputs
monitor execution
update job status

Pseudo workflow:

Receive Job

↓

Read Workflow

↓

Identify Required Agents

↓

Dispatch Events

↓

Collect Results

↓

Validate

↓

Publish Course

The Orchestrator never contains business logic.

Chapter 10 — Shared Memory Layer

Purpose:

Maintain context between agents.

Memory types:

Global Memory

Course Memory

Module Memory

Lesson Memory

User Memory (future)

Example:

Course Title

↓

Modules

↓

Definitions

↓

Terminology

↓

Teaching Style

All agents access memory through a common interface.

Chapter 11 — Learning Graph Engine

Every course is stored as a graph.

Probability

│

├── Random Variables

│      ├── PMF

│      └── PDF

├── Conditional Probability

├── Bayes

└── Applications

Each node stores:

concept
prerequisites
difficulty
learning objective
estimated duration

Benefits:

adaptive learning
revision planning
prerequisite validation
future recommendation engine
Chapter 12 — LLM Provider Layer

No module communicates directly with Ollama.

Lesson Agent

↓

LLM Provider

↓

Ollama

↓

Llama 3

Future providers:

Qwen
Gemma
DeepSeek
Mistral
Azure OpenAI

Changing providers should require zero changes to agents.

Chapter 13 — Job Management

Every workflow is represented as a Job.

Job

↓

Tasks

↓

Events

↓

Results

States:

Pending

Running

Paused

Completed

Failed

Cancelled

The Job Manager supports recovery after unexpected shutdowns.

Chapter 14 — Storage System
storage/

uploads/

courses/

videos/

audio/

images/

cache/

exports/

logs/

No generated content is stored inside the database.

SQLite stores only metadata.

Chapter 15 — Logging Framework

Every action generates structured logs.

Each log contains:

timestamp
agent
model
duration
tokens (if available)
status
errors
retry count

Logs are stored in JSON Lines format for future analytics.

Chapter 16 — Error Handling

Every component returns a standard response:

{
  "status": "success | warning | failed",
  "code": "VIR-XXXX",
  "message": "...",
  "data": {}
}

Recovery order:

Retry
Alternative prompt
Alternative model (future)
Human intervention
Chapter 17 — Security Model

Phase 1:

Local execution only
No telemetry
No mandatory internet
Local authentication
Local encrypted database (future)

User files never leave the device unless explicitly exported.

Chapter 18 — Performance Requirements

Target metrics for MVP:

Operation	Target
Startup	< 5 s
PDF parsing (100 pages)	< 20 s
Course generation	< 3 min
Lesson generation	< 10 s per lesson
Quiz generation	< 5 s
Flashcard generation	< 5 s
UI response	< 100 ms
Chapter 19 — Coding Standards

Backend:

Python 3.12+
Type hints required
Black formatting
Ruff linting
Async-first where appropriate

Frontend:

Flutter
Riverpod
Feature-based architecture
Stateless widgets by default

General:

One responsibility per class
Dependency injection
No circular dependencies
Configuration over hardcoding
Chapter 20 — Future Scalability

The architecture must support:

Distributed agent execution
Multiple local models
Cloud deployment
Multi-user mode
Collaborative course editing
AI Tutor
Adventure Mode
Practice Labs
Enterprise deployment

No core architectural changes should be required to add these capabilities.