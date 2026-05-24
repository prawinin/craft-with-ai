# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 22: Context-Driven AI (Codebase Packaging)
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - How LLMs process code context (and the cost of "Token Bloat")
    - Generating text-based directory maps programmatically
    - Writing a codebase packager tool to merge files for AI prompts
    - Filtering out clutter (like .venv, .git, and binaries)
    - Writing structured prompt contexts for complex debugging

  Why this matters for AI:
    To get accurate code output from an LLM, you must supply the correct context.
    If you paste random files, you exceed token limits, confuse the model,
    and pay higher costs. If you give no context, the model makes up fake variables.
    Learning to package and map your codebase is the ultimate multiplier
    for AI-assisted software building.

  Estimated time: 20 minutes

===============================================================================
"""

import os
from pathlib import Path

# === THE SYSTEM CONTEXT PROBLEM ==============================================
#
# WHAT IS A CONTEXT WINDOW?
#   Think of an LLM's Context Window like a human's short-term memory or the size of
#   a desk you are working on. When you ask a question, all the files, prompts, and prior
#   messages must fit on that desk. If you dump too many files on the desk, the older papers
#   fall off the edge and are forgotten. The bigger the context window, the more information
#   the AI can remember at one time—but it also makes the desk more cluttered and harder to search!
#
# WHAT IS A TOKEN (LLM sense)?
#   Tokens are the "syllables" or word-chunks that an AI reads. AI models don't read words
#   character-by-character; instead, they chop text into small pieces (usually 3–4 characters
#   each). For example, the word "Antigravity" might be chopped into three tokens: "Anti",
#   "grav", and "ity". Every token sent to the AI costs a tiny fraction of a cent, so keeping
#   your code clean and compact keeps your AI bills low!
#
# LLMs work on "tokens" (chunks of text). When asking an AI to add a feature
# to your codebase, you must answer three questions:
#   1. Where does this fit in the structure? (Directory Tree Map)
#   2. What are the dependencies? (Imports & API signatures of surrounding files)
#   3. What are the constraints? (Configurations & requirements.txt)
#
# Crucial Rule: Avoid sending `.git/`, `.venv/`, `node_modules/`, `__pycache__` or
# databases to the model. They consume millions of tokens and break the model's focus.

# print("--- 1. THE CODEBASE CONTEXT MODEL ---")
print("Provide Structure -> Provide Selected Code Files -> State Goal clearly")


# === GENERATING DIRECTORY TREES ==============================================
#
# WHAT IS A DIRECTORY TREE?
#   A directory tree is a text representation of your project's folders and files. It's like
#   a blueprint of a house showing the layout of the rooms. By showing the AI this map, it instantly
#   understands where files are located relative to each other, preventing it from inventing
#   fictional directories that don't exist in your actual project!
#
# A text-based tree is the fastest way to explain your project architecture
# to an AI. It looks like this:
#
#   my_project/
#   ├── data/
#   │   └── raw.csv
#   ├── src/
#   │   └── utils.py
#   └── main.py
#
# Let's write a recursive Python function to build this map programmatically!

# print("\n--- 2. GENERATING CODEBASE DIRECTORY MAPS ---")

def generate_tree_map(directory, prefix="", ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = {".git", ".venv", "__pycache__", "node_modules", "data"}
        
    dir_path = Path(directory)
    tree_lines = []
    
    # Get sorted files and folders (excluding ignored ones)
    items = sorted(
        [x for x in dir_path.iterdir() if x.name not in ignore_dirs],
        key=lambda x: (not x.is_dir(), x.name.lower())
    )
    
    for idx, item in enumerate(items):
        is_last = (idx == len(items) - 1)
        connector = "└── " if is_last else "├── "
        
        # Append name
        tree_lines.append(f"{prefix}{connector}{item.name}/" if item.is_dir() else f"{prefix}{connector}{item.name}")
        
        # Recurse if directory
        if item.is_dir():
            next_prefix = prefix + ("    " if is_last else "│   ")
            tree_lines.extend(generate_tree_map(item, next_prefix, ignore_dirs))
            
    return tree_lines

# Let's print a map of our current workspace!
workspace_map = generate_tree_map(".")
print("Project Tree Structure (omitting .venv, .git, databases):")
for line in workspace_map[:15]: # Print first 15 entries
    print(line)


# === PROGRAMMATIC CODEBASE PACKAGING =========================================
#
# To let an AI debug a cross-file bug, you can merge your core python source
# files into a single structured Markdown document that you copy-paste:
#
#   # File: src/utils.py
#   ```python
#   def process()...
#   ```
#
#   # File: main.py
#   ```python
#   ...
#   ```
#
# Let's write a utility to package our workspace files into a clean markdown codepack!

# print("\n--- 3. SYSTEM CODEBASE PACKAGER UTILITY ---")

def package_codebase(root_dir, include_suffixes=None, ignore_dirs=None):
    if include_suffixes is None:
        include_suffixes = {".py", ".txt", ".json"}
    if ignore_dirs is None:
        ignore_dirs = {".git", ".venv", "__pycache__", "node_modules", "data", "cli_sandbox"}
        
    root = Path(root_dir)
    codepack = []
    
    # Walk directory tree
    for dirpath, dirnames, filenames in os.walk(root):
        # Modify dirnames in-place to avoid traversing ignored folders
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        
        for filename in filenames:
            filepath = Path(dirpath) / filename
            if filepath.suffix in include_suffixes:
                try:
                    # Skip massive generated files or course_runner (too large)
                    if filepath.name == "course_runner.py" or filepath.stat().st_size > 50000:
                        continue
                        
                    content = filepath.read_text(encoding="utf-8")
                    relative_path = filepath.relative_to(root)
                    
                    codepack.append(f"## File: {relative_path}")
                    codepack.append(f"```{filepath.suffix[1:]}")
                    codepack.append(content)
                    codepack.append("```\n")
                except Exception as e:
                    # Skip files that can't be read (binaries, encodings)
                    continue
                    
    return "\n".join(codepack)

# Generate a codebase bundle of our workspace
codebase_bundle = package_codebase(".", include_suffixes={".py"})
print(f"Generated Codebase Bundle: {len(codebase_bundle)} characters compiled.")
print("Bundle format example (first 10 lines):")
print("\n".join(codebase_bundle.split("\n")[:10]))


# === PRECISE AI PROMPT STRUCTURING ===========================================
#
# WHAT IS STDIN (STANDARD INPUT)?  (Related to stdout/stderr in Module 2, Lesson 1 — "Shell Navigation")
#   While Standard Output (stdout) is the program's output tube, stdin (Standard Input) is the
#   program's input intake tube. Think of it like a funnel: when a script asks you to "type your name"
#   in the terminal, it is waiting for data to flow down the stdin tube from your keyboard.
#
# Once you have the codebase map and packaged files, structure your prompt
# like a professional architect:
#
#   === CONTEXT ===
#   [Insert Directory Tree Map here]
#
#   === CODEFILES ===
#   [Insert Codebase Bundle here]
#
#   === TASK ===
#   Explain why running main.py fails with DBConnectionError and suggest a fix.

# Provide the CWD structure, specific dependent files, and target commands.


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Pasting binary files or system logs
#   Always verify that you are only copying text-based code files (.py, .js, .json, .html).
#   Sending massive log outputs or compiled binaries wastes prompt window space.

# MISTAKE 2: Forgetting to update the tree map
#   If you add files to your project, regenerate the directory map so the AI
#   understands where to place newly written classes.

# MISTAKE 3: Sending the virtual environment (.venv)
#   The `.venv` folder contains thousands of internal Python package scripts.
#   Never include `.venv` in your search or copy operations!


# === EXERCISES ================================================================
#
# Exercise 1: Extend `generate_tree_map` to count and return the total number of
#             files and directories it discovered during traversal.
#
# Exercise 2: Write a python program that saves the generated codebase bundle
#             directly to a file named `codebase_prompt_context.md`.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# def count_files_and_dirs(directory, ignore_dirs=None):
#     if ignore_dirs is None:
#         ignore_dirs = {".git", ".venv", "__pycache__"}
#     file_count = 0
#     dir_count = 0
#     for p in Path(directory).rglob("*"):
#         if any(part in ignore_dirs for part in p.parts):
#             continue
#         if p.is_file():
#             file_count += 1
#         elif p.is_dir():
#             dir_count += 1
#     return dir_count, file_count
#
# Exercise 2:
# bundle = package_codebase(".", include_suffixes={".py"})
# Path("codebase_prompt_context.md").write_text(bundle, encoding="utf-8")


# === KEY TAKEAWAYS ============================================================
#
# - LLM prompts thrive on minimal, highly-relevant context, not huge dumps of code.
# - Directory trees let AIs map project structures instantly and accurately.
# - Codebase packagers allow you to combine multiple source files safely for debugging.
# - Excluding binary and virtual environments preserves token limits and reduces latency.
# - Formatted codepacks make copy-pasting structured and parsing-friendly for AI.
