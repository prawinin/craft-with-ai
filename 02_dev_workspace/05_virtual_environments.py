# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 23: Virtual Environments & Dependencies
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - What a Virtual Environment (.venv) is and why it's necessary
    - How to create and activate a virtual environment
    - How to install packages and freeze them into requirements.txt
    - The "Toolbox Analogy" for isolating Python projects

  Why this matters for AI:
    AI libraries (like PyTorch, LangChain, OpenAI) are massive and update weekly.
    If you install everything globally on your computer, Project A (using LangChain v0.1) 
    might break when Project B installs LangChain v0.2. Virtual environments ensure 
    each AI project has its own isolated "sandbox" of dependencies.

  Estimated time: 15 minutes

===============================================================================
"""

import sys
from pathlib import Path

# === THE TOOLBOX ANALOGY ======================================================
#
# WHAT IS A VIRTUAL ENVIRONMENT?
#   Imagine you are a mechanic. You work on two cars:
#   - Car A requires Metric wrenches.
#   - Car B requires Imperial wrenches.
#   If you throw all your wrenches into one giant global toolbox, you'll constantly
#   grab the wrong size and strip the bolts. 
#
#   A Virtual Environment (.venv) is like buying a separate, smaller toolbox
#   just for Car A, and another toolbox just for Car B. When you work on Car A,
#   you "activate" that toolbox, meaning you only see and use the Metric wrenches.
#
#   In Python, "wrenches" are packages (like pandas, requests, openai).

# print("--- 1. CHECKING THE ACTIVE ENVIRONMENT ---")

def is_virtual_env():
    """Detects if we are currently running inside a virtual environment."""
    # sys.prefix points to the active environment directory.
    # sys.base_prefix points to the global Python installation.
    # If they are different, we are in a virtual environment!
    return sys.prefix != sys.base_prefix

print(f"Are we inside a virtual environment right now? {'Yes ✅' if is_virtual_env() else 'No ❌'}")
print(f"Active Python path: {sys.prefix}")


# === CREATING AND ACTIVATING ==================================================
#
# HOW TO CREATE A VIRTUAL ENVIRONMENT (in your terminal):
#   1. Navigate to your project folder:  `cd my_ai_project`
#   2. Create the environment:           `python3 -m venv .venv`
#      (This creates a hidden folder named '.venv' containing a fresh Python copy)
#
# HOW TO ACTIVATE IT:
#   - Mac / Linux:   `source .venv/bin/activate`
#   - Windows (CMD): `.venv\\Scripts\\activate`
#   - Windows (PS):  `.venv\\Scripts\\Activate.ps1`
#
#   Once activated, your terminal prompt will usually change to show `(.venv)` 
#   at the beginning of the line!

# print("\n--- 2. MANAGING DEPENDENCIES (requirements.txt) ---")
#
# WHAT IS A requirements.txt FILE?
#   It's a shopping list. When you share your AI code with someone else (or deploy
#   it to the cloud), you don't send them your massive `.venv` folder. Instead,
#   you send them the code and the `requirements.txt` shopping list.
#
#   To generate the list:      `pip freeze > requirements.txt`
#   To install from the list:  `pip install -r requirements.txt`

def simulate_requirements_parsing(req_file_content: str):
    """Parses a requirements.txt file to show what packages are needed."""
    print("Parsing requirements.txt shopping list:")
    for line in req_file_content.strip().split("\n"):
        line = line.strip()
        # Ignore comments and empty lines
        if not line or line.startswith("#"):
            continue
            
        # Split on the version pinning '=='
        if "==" in line:
            package, version = line.split("==")
            print(f"  📦 Need package: {package:<15} (Version: {version})")
        else:
            print(f"  📦 Need package: {line:<15} (Version: Latest)")

sample_requirements = """
# AI Stack Dependencies
openai==1.14.0
langchain==0.1.13
python-dotenv==1.0.1
requests
"""

simulate_requirements_parsing(sample_requirements)


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Committing the .venv folder to Git
#   The `.venv` folder contains thousands of files specific to your operating system
#   (Mac/Windows/Linux). If you push it to GitHub, it will waste gigabytes of space
#   and won't even work on your teammate's computer. 
#   Fix: ALWAYS add `.venv/` to your `.gitignore` file!

# MISTAKE 2: Installing packages before activating
#   If you run `pip install openai` without activating the `.venv` first, it
#   installs globally. You'll wonder why your code works on your laptop but crashes
#   everywhere else.

# MISTAKE 3: "ModuleNotFoundError" confusion
#   If you see `ModuleNotFoundError: No module named 'requests'`, 99% of the time
#   it means either:
#   A) You forgot to pip install it.
#   B) You installed it, but forgot to activate your `.venv` before running the script.


# === EXERCISES ================================================================
#
# Exercise 1: Write a function `generate_gitignore_entry()` that returns a string
#             containing standard ignore rules for Python environments, preventing
#             the .venv from being accidentally uploaded.
#
# Exercise 2: You just cloned an AI project from GitHub. List the exact 3 terminal
#             commands you would run to set up the environment and install dependencies.


# === SOLUTIONS ================================================================
#
# Exercise 1:
# def generate_gitignore_entry():
#     return "# Environments\n.env\n.venv/\nenv/\nvenv/\n__pycache__/"
#
# Exercise 2:
# 1. python3 -m venv .venv
# 2. source .venv/bin/activate
# 3. pip install -r requirements.txt


# === KEY TAKEAWAYS ============================================================
#
# - A virtual environment (.venv) is an isolated toolbox for a specific project.
# - Always activate your environment before running `pip install` or `python`.
# - Never commit the `.venv` folder to Git; share a `requirements.txt` instead.
