Phase 5 – Educational Rendering Engine (ERE)

This phase replaces the traditional "video generation" pipeline with an AI-driven instructional design and rendering system. Instead of converting text directly into narrated slides, Vireon analyzes each lesson, determines the best instructional strategy, selects the most appropriate visual representation, generates educational assets, and renders them into a professional-quality learning experience. The objective is not to generate videos—it is to generate effective educational experiences.

Objective

Transform every AI-generated lesson into a visually rich, pedagogically effective learning experience comparable to high-quality educational content from platforms such as TED-Ed, Kurzgesagt, Brilliant, and 3Blue1Brown.

Design Philosophy

Instead of asking:

"How do we create a video?"

The system asks:

"What is the most effective way to teach this concept visually?"

The renderer should choose visuals based on the educational content rather than applying the same slide template to every lesson.

Architecture
Lesson
      │
      ▼
Instructional Design Agent
      │
      ▼
Visual Director Agent
      │
      ▼
Scene Graph Builder
      │
      ▼
Educational Rendering Engine
      │
      ▼
Professional Educational Video
Step 1 – Instructional Design Agent

The first stage focuses on teaching strategy, not visuals.

Responsibilities

The agent analyzes the lesson and determines:

learning objective
key concepts
prerequisite knowledge
difficult concepts
examples
misconceptions
reinforcement points
interaction checkpoints

Instead of producing plain text, it generates a structured teaching plan.

Example

Lesson:
  Leadership

Objectives:
  - Understand leadership
  - Identify leadership qualities

Teaching Strategy:
  - Hook
  - Explain
  - Visual Example
  - Real World Example
  - Summary
Step 2 – Visual Director Agent

The Visual Director decides how every concept should be visualized.

Instead of selecting random images, it chooses the best educational renderer.

Example

Concept	Renderer
Leadership	Character Illustration
Programming	Code Renderer
Finance	Animated Charts
Biology	Diagram Renderer
Physics	Manim
History	Timeline
AI	Network Diagram
Mathematics	Formula Animation

The output is a rendering plan for each scene.

Step 3 – Scene Graph Builder

Instead of creating a single long video, the lesson is divided into educational scenes.

Example

Scene 1
Hook

Scene 2
Concept Explanation

Scene 3
Visual Diagram

Scene 4
Real World Example

Scene 5
Knowledge Check

Scene 6
Summary

Each scene becomes an independent rendering unit.

Step 4 – Educational Rendering Engine

The Scene Graph is passed to the Educational Rendering Engine.

Instead of relying on a single rendering technique, the engine contains multiple specialized renderers.

Educational Rendering Engine

├── HTML Renderer
├── SVG Renderer
├── Animation Renderer
├── Manim Renderer
├── Chart Renderer
├── Timeline Renderer
├── Diagram Renderer
├── Code Renderer
├── Formula Renderer
└── Subtitle Renderer

The engine selects the appropriate renderer for every scene.

Step 5 – HTML Slide Renderer

General educational content is rendered using HTML templates.

Technology

HTML5
TailwindCSS
Playwright

The AI populates predefined templates with generated content.

Example

Title

Illustration

Explanation

Key Points

Example

Bottom Summary

Screenshots are generated using Playwright.

Step 6 – Diagram Renderer

Whenever relationships exist,

generate diagrams automatically.

Supported diagrams

Flowcharts
Mind Maps
Process Diagrams
Network Graphs
Comparison Tables
Organizational Charts

Technologies

Mermaid
Graphviz
SVG
Step 7 – Chart Renderer

If numerical information exists,

generate animated charts.

Supported

Line Chart
Bar Chart
Pie Chart
Scatter Plot
Timeline

Technology

Plotly
Step 8 – Formula & Mathematics Renderer

Mathematical concepts should never appear as static text.

Use

Manim

to generate animated equations and derivations.

Step 9 – Programming Renderer

Programming lessons should display executable code rather than screenshots.

Use

HTML
Shiki
Monaco Editor styling

Animations include

typing effect
syntax highlighting
execution flow
line highlighting
Step 10 – Motion Graphics

Static slides should be enhanced with motion.

Animations include

Fade
Zoom
Slide
Morph
Highlight
Draw
Scale
Pulse

Use

SVG
Lottie
Step 11 – Audio

Narration is generated using

Kokoro TTS

Fallback

Piper

Audio is synchronized with scene timing.

Step 12 – Subtitle Engine

Every lesson includes synchronized subtitles.

Requirements

word-level timing
highlighted active word
accessibility support
Step 13 – Video Composition

Instead of MoviePy,

use

ffmpeg-python

Responsibilities

merge scenes
synchronize narration
burn subtitles
transitions
encode final MP4

MoviePy may still be retained as a lightweight fallback for simple prototypes.

Step 14 – Quality Assurance

Every rendered lesson is validated.

Checks

subtitle timing
audio synchronization
visual overlap
missing assets
rendering errors
empty scenes

Failed scenes are regenerated automatically.

Step 15 – Final Output

The renderer produces:

Course

├── Videos

├── Audio

├── Scene Graph

├── Educational Assets

├── Subtitles

├── Thumbnails

└── Metadata
Future Enhancements

The architecture is intentionally renderer-agnostic.

Future renderers can be added without changing lesson generation.

Potential additions

AI Avatar Renderer
Interactive 3D Renderer
Virtual Lab Renderer
AR Renderer
VR Renderer
WebGL Renderer
AI Character Narrator
Success Criteria

The Educational Rendering Engine is considered complete when it:

Selects renderers automatically based on lesson content.
Produces visually consistent educational videos.
Uses reusable templates and assets.
Generates videos that are significantly more engaging than static narrated slides.
Operates entirely with local, open-source technologies.
Allows new renderers to be added without modifying the orchestration pipeline.