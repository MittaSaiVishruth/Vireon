VIREON AGENT CONTRACT SPECIFICATION (ACS)

Project: Vireon AI Learning Operating System (VAIOS)

Version: 1.0

Architecture: Multi-Agent AI System

Deployment: Local (Phase 1)

Initial LLM: Ollama + Llama 3

1. Purpose

The ACS defines the behavior, interfaces, communication rules, responsibilities, and quality standards for every AI agent within Vireon.

Each agent must:

Have a single responsibility.
Never directly invoke another agent.
Communicate only through the AI Orchestrator.
Produce structured JSON output.
Validate its own output before returning.
Be independently testable.
2. Agent Communication Principles

Agents never call each other directly.

User
 │
 ▼
Planner Agent
 │
 ▼
AI Orchestrator
 │
 ├── Document Agent
 ├── Curriculum Agent
 ├── Lesson Agent
 ├── Assessment Agent
 ├── Learning Experience Agent
 ├── Storyboard Agent
 ├── Media Producer
 ├── QA Agent
 └── Course Publisher

The Orchestrator owns the workflow.

3. Standard Agent Contract

Every agent must expose the same interface.

{
  "agent_id": "lesson_agent",
  "version": "1.0",
  "job_id": "UUID",
  "status": "success",
  "execution_time": 1.52,
  "input": {},
  "output": {},
  "warnings": [],
  "errors": []
}

This makes swapping agents easy.

4. Standard Lifecycle

Every agent follows exactly the same lifecycle.

Receive Job

↓

Validate Input

↓

Prepare Prompt

↓

Run LLM

↓

Parse Output

↓

Validate Output

↓

Return JSON
5. Planner Agent
Role

Learning Strategist

Purpose

Convert uploaded content into a learning strategy.

Responsibilities

Identify

document type
difficulty
subject
learner level
estimated duration

Decide

number of modules
lesson length
interaction types
required AI agents
Input
{
 "document":"..."
}
Output
{
 "course_type":"Programming",

 "difficulty":"Intermediate",

 "modules":8,

 "lesson_duration":"90 seconds",

 "required_agents":[
   "Curriculum",
   "Lesson",
   "Assessment",
   "LearningExperience",
   "MediaProducer"
 ]
}
Success Criteria

95% correct subject detection.

6. Document Agent
Role

Content Engineer

Purpose

Convert uploaded documents into clean structured text.

Responsibilities

OCR
Remove headers
Remove page numbers
Remove duplicates
Detect headings
Preserve formatting

Input

PDF

Output

{
 "chapters":[],
 "text":"..."
}

Validation

No empty chapters.

Failure

Unreadable document

↓

Retry OCR

7. Curriculum Agent
Role

Knowledge Architect

Purpose

Create educational structure.

Responsibilities

Generate

course
modules
lessons
learning objectives
prerequisites

Output

{
 "course":{

   "modules":[

   ]

 }
}

Validation

Every lesson belongs to one module.

8. Lesson Agent
Role

Learning Designer

Purpose

Explain concepts.

Generates

explanation
analogy
examples
summary
key takeaways

Target

90–120 second lesson.

Validation

Reading level matches learner.

9. Assessment Agent
Role

Assessment Designer

Purpose

Measure understanding.

Generates

MCQ
True/False
Fill blank
Flashcards
Reflection questions

Future

Drag & Drop

Scenario

Puzzle

Validation

Correct answer verified.

10. Learning Experience Agent
Role

Interaction Designer

Purpose

Choose best learning interaction.

Example

Programming

↓

Code Sandbox

Math

↓

Equation Builder

Finance

↓

Budget Simulator

Biology

↓

Label Diagram

History

↓

Timeline

Cybersecurity

↓

Attack Simulation

Output

{
 "interaction":"drag_drop",

 "instructions":"..."
}

Validation

Interaction matches concept.

11. Storyboard Agent
Role

Media Designer

Purpose

Convert lesson into scenes.

Output

{
 "scene":1,

 "voice":"",

 "subtitle":"",

 "visual":"",

 "animation":"",

 "duration":8
}

Validation

Scene duration under 10 seconds.

12. Media Producer
Role

Video Producer

Purpose

Generate final lesson media.

Produces

narration
subtitles
slides
MP4

Future

Animation

3D

Avatar

Validation

Audio and captions synchronized.

13. Quality Assurance Agent
Role

Reviewer

Purpose

Review every AI output.

Checks

hallucinations
duplicate lessons
factual errors
quiz correctness
ordering
missing concepts

Output

{
 "passed":true,

 "confidence":0.94,

 "issues":[]
}

Failure

↓

Regenerate.

14. Course Publisher

Purpose

Merge all outputs.

Creates

Course

↓

Modules

↓

Lessons

↓

Activities

↓

Videos

↓

Assessments

↓

Metadata
15. Agent Events

Agents listen only to events.

Example

PDF_UPLOADED

↓

DOCUMENT_PARSED

↓

CURRICULUM_READY

↓

LESSONS_READY

↓

MEDIA_READY

↓

COURSE_PUBLISHED
16. Retry Policy

Level 1

Prompt retry

Level 2

Different temperature

Level 3

Different model

Level 4

Human review

17. Performance Targets

Planner

<3 sec

Document

<10 sec

Curriculum

<20 sec

Lesson

<30 sec

Assessment

<15 sec

Storyboard

<15 sec

Media

<60 sec

18. Prompt Management

Every agent owns its prompts.

prompts/

planner.md

curriculum.md

lesson.md

assessment.md

interaction.md

storyboard.md

qa.md

Version-controlled independently.

19. Model Management

Current

Ollama

↓

Llama 3

Future

Qwen

DeepSeek

Gemma

Mistral

The agent never knows which model is being used.

Only the LLM Provider Layer handles model selection.

20. Acceptance Criteria

An agent is complete only when:

It passes unit tests.
It validates malformed input.
It returns valid JSON.
It logs execution metrics.
It supports retries.
It follows the standard contract.
It has documented prompts.
It can be replaced without affecting other agents.