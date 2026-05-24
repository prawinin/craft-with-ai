<div align="center">
  <h1>Craft with AI 🤖</h1>
  <p><b>Build Enterprise-Grade AI from Scratch — The absolute fastest path from beginner to AI Engineer.</b></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version" />
    <img src="https://img.shields.io/badge/Lessons-42-success.svg" alt="Lessons" />
    <img src="https://img.shields.io/badge/License-CC--BY--NC--ND-red.svg" alt="License" />
  </p>
</div>

---

Welcome to **Craft with AI** — a comprehensive, browser-first course that teaches you the architecture of modern software engineering and AI systems. Unlike boring, text-heavy bootcamps, this course is designed specifically for building alongside modern AI coding assistants (Cursor, Copilot, Gemini). 

We don't just teach you the code; we teach you **"Why this matters for AI"** using brilliant, real-world analogies.

### ✨ The "Zero-Install" Experience
1. Run **one** python file (`course_runner.py`).
2. The entire course opens automatically in a gorgeous, responsive browser UI.
3. Your progress is saved automatically. 
4. **Interactive Code Runner:** You can read, edit, and run Python code directly inside your browser!

---

## 📚 The Curriculum

The course features **42 heavily-polished lessons** (~16 hours of guided content) broken into 7 progressive modules. 

| Module | Topics |
|--------|--------|
| **1 · Python Programming** | Variables, data types, loops, functions, APIs, pandas (19 lessons) |
| **2 · Dev Workspace** | Linux shell, Git (local & remote), paths, **Virtual Environments**, codebase packaging |
| **3 · APIs & FastAPI** | HTTP protocol, Pydantic, async/await, FastAPI routers, Dependency Injection |
| **4 · Containerization** | Docker architecture, Dockerfiles, Multi-stage builds, Docker Compose, Healthchecks |
| **5 · AI Stack** | LLM API clients, structured JSON outputs, chunking strategies, Vector Databases (ChromaDB) |
| **6 · Autonomous Systems** | Tool calling (OpenAI stubs), ReAct loops, stateful agent management, persistence |
| **7 · Observability & LLMOps** | Tracing, CI/CD with GitHub Actions, cloud deployment |

---

## 🚀 Quick Start

To launch the course, you don't need to install any heavy packages. Just use the startup script for your OS:

### Linux / macOS
```bash
chmod +x start_linux.sh   # (or start_mac.sh)
./start_linux.sh
```

### Windows
Double-click `start_windows.bat`

### 🛠️ Manual Setup (If You Prefer)

**1. Create a Virtual Environment**
```bash
python3 -m venv .venv
```

**2. Activate the Environment**
- **Mac/Linux:** `source .venv/bin/activate`
- **Windows:** `.venv\Scripts\activate`

**3. Install Dependencies & Launch**
```bash
pip install -r requirements.txt
python course_runner.py
```

---

## 🛠️ What You'll Build & Learn

By completing this course, you won't just "know Python"—you'll be able to orchestrate full AI systems:
- Write robust Python scripts that interact with LLM APIs.
- Navigate the Linux terminal, manage Virtual Environments, and use Git remotely.
- Build production-grade, secure APIs with FastAPI and Pydantic.
- Containerize massive AI dependencies using Multi-stage Docker builds.
- Connect to Vector Databases and build semantic search pipelines.
- Create autonomous AI agents with working memory (State Persistence) and tool-calling capabilities.

---

## 🎨 The UI Experience

- **Browser UI:** Instantly served via standard library Python.
- **7-Module Accordion:** Clean, distraction-free navigation.
- **Smart Code Runner:** Edit code directly in the lesson. If your code runs successfully but has no print output, the runner smartly tells you: *"✨ Success! (No output to display)"* so you're never confused.
- **Day / Night Mode:** Beautiful, minimalist toggle.
- **Spotlight Search:** Instantly find concepts across all 42 lessons.
- **In Simple Words:** Beginner-friendly summaries and vivid analogies (like the "Kitchen Assistant" for Dependency Injection, or "Toolboxes" for Virtual Environments).

---

## 🏗️ Architecture

All lesson content lives inside numbered Python files that double as actual, runnable scripts!

```text
├── 01_python_programming/       # 19 lessons
├── 02_dev_workspace/            # 5 lessons
├── 03_apis_fastapi/             # 4 lessons
├── 04_containerization_docker/  # 4 lessons
├── 05_ai_stack/                 # 4 lessons
├── 06_autonomous_systems/       # 3 lessons
├── 07_observability_llmops/     # 3 lessons
└── course_runner.py             # The engine that runs it all
```

---

## ⚖️ License

**Copyright (c) 2026 Prawin Kumar. All rights reserved.**<br>
Licensed under CC BY-NC-ND 4.0.

- ✅ **Allowed:** Personal learning and sharing unmodified material.
- ❌ **Not allowed:** Commercial use, rebranding, or derivative redistribution.

See [LICENSE](LICENSE) for full terms.
