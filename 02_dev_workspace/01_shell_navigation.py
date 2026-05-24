# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 19: Shell Navigation & Command Line Basics
  Difficulty: Beginner-Intermediate
===============================================================================

  What you will learn:
    - How to navigate the filesystem using commands (ls, cd, pwd, mkdir)
    - Moving, copying, and deleting files (cp, mv, rm)
    - Redirecting output (>, >>) and piping commands (|)
    - Searching content within files and outputs (grep)
    - Understanding how shell concepts translate to AI-assisted coding

  Why this matters for AI:
    AI models are great at writing shell scripts, setting up environments,
    and running installations. But if you cannot run the terminal commands,
    debug permission issues, or check active directories, you cannot use
    AI-generated code safely or effectively. Master the command line, and
    you master the execution layer of all AI agents.

  Estimated time: 20 minutes

===============================================================================
"""

import os
import subprocess
import shutil
from pathlib import Path

# === SHELL NAVIGATION ========================================================
#
# WHAT IS THE TERMINAL OR SHELL?
#   Think of your operating system as a giant house. The graphical interface (icons,
#   windows, and buttons) is like using a touch-screen home automation tablet. The
#   Terminal or Shell is like having a direct intercom line to the building engineer:
#   you type specific commands, and the system executes them directly. A terminal is
#   the window where you type, and the shell is the program behind it that translates
#   your text commands into actions.
#
# WHAT IS THE CURRENT WORKING DIRECTORY (CWD)?
#   The CWD is like your coordinate position in a physical building. At any given
#   moment, you are standing in a specific room (folder). If you ask someone to
#   "hand me the keys," they will look in the same room. Similarly, if a command
#   or Python script opens a file without a full path, it assumes the file is
#   located in the CWD (the exact folder you are standing in).
#
# When using a terminal, you are ALWAYS "inside" a directory. This is the CWD.
#
# Key Navigation Commands:
#   pwd      - Print Working Directory (shows exactly where you are)
#   ls       - List files and folders in the current directory
#   cd       - Change Directory (move to a different folder)
#   mkdir    - Make Directory (create a new folder)

# print("--- 1. NAVIGATION IN PYTHON & SHELL ---")

# Let's print the current working directory (equivalent to running 'pwd'):
cwd = Path.cwd()
print(f"Current Directory (pwd): {cwd}")

# Let's list files in the current directory (equivalent to running 'ls'):
print("\nFiles in directory (ls):")
for item in cwd.glob("*"):
    # Print name and identify if it's a directory or a file
    type_label = "[DIR]" if item.is_dir() else "[FILE]"
    print(f"  {type_label} {item.name}")

# Let's create a temporary directory for our CLI sandbox (equivalent to 'mkdir cli_sandbox'):
sandbox_dir = cwd / "cli_sandbox"
sandbox_dir.mkdir(exist_ok=True)
print(f"\nCreated sandbox directory: {sandbox_dir.name}")


# === FILE OPERATIONS =========================================================
#
# In a shell, you manipulate files using simple, short verbs:
#   cp [source] [destination] - Copy a file or directory
#   mv [source] [destination] - Move or rename a file or directory
#   rm [target]               - Remove (delete) a file
#   rm -rf [target]           - Recursively remove a directory and its contents

# print("\n--- 2. FILE OPERATIONS (cp, mv, rm) ---")

# Create a sample text file in our sandbox
test_file = sandbox_dir / "notes.txt"
test_file.write_text("AI is a force multiplier for software engineering.\n", encoding="utf-8")
print(f"Created file: {test_file.relative_to(cwd)}")

# 1. Copying a file (cp notes.txt backup.txt)
backup_file = sandbox_dir / "backup.txt"
shutil.copy(test_file, backup_file)
print(f"Copied file to: {backup_file.relative_to(cwd)}")

# 2. Moving / Renaming a file (mv backup.txt archive.txt)
archive_file = sandbox_dir / "archive.txt"
shutil.move(backup_file, archive_file)
print(f"Moved/Renamed to: {archive_file.relative_to(cwd)}")

# List the sandbox directory contents (ls cli_sandbox)
print("Sandbox files:")
for item in sandbox_dir.glob("*"):
    print(f"  - {item.name}")


# === REDIRECTS AND PIPING ====================================================
#
# WHAT IS STDOUT AND STDERR?
#   When a computer program runs, it has standard "communication tubes" or streams.
#   Standard Output (stdout) is the main tube where the program sends its normal messages
#   (like standard print output). Standard Error (stderr) is a separate tube used exclusively
#   for emergency distress signals or warning messages. Even if the main screen is redirected
#   or hidden, you can still see the emergency errors because they travel down a different tube!
#
# WHAT IS PIPING (|)?
#   Piping is like a factory assembly line. Instead of having one giant machine do
#   everything, you have specialized machines. You take the output of Machine A
#   (e.g., listing all items in a room) and feed it directly into the intake of
#   Machine B (e.g., filtering out everything except red items). In the command line,
#   the pipe symbol (`|`) connects the output of one command to the input of another.
#
# Redirects send command outputs to files instead of printing them on screen:
#   >  - Overwrite file with output (e.g., echo "hello" > file.txt)
#   >> - Append output to end of file (e.g., echo "world" >> file.txt)
#
# Piping passes the output of one command as the input of another command:
#   |  - Connect standard output to standard input (e.g., ls | grep "notes")

# print("\n--- 3. REDIRECTS AND PIPING (>, >>, |) ---")

# In pure Python, we write and append using open modes 'w' (write) and 'a' (append):
output_file = sandbox_dir / "logs.txt"

# Simulate command redirect (echo "Process Started" > logs.txt)
with open(output_file, "w", encoding="utf-8") as f:
    f.write("LOG: Process Started\n")

# Simulate command append (echo "Model Initialized" >> logs.txt)
with open(output_file, "a", encoding="utf-8") as f:
    f.write("LOG: AI Model Initialized successfully\n")
    f.write("LOG: Connection established on port 8000\n")

print(f"Wrote redirect logs to: {output_file.relative_to(cwd)}")
print(f"Log content:\n{output_file.read_text(encoding='utf-8')}")


# === SEARCHING CONTENT WITH GREP ============================================
#
# 'grep' is one of the most powerful command line utilities. It searches files
# for lines matching a pattern and returns the results.
#
# Common formats:
#   grep "pattern" filename.txt   - Search file for text match
#   grep -i "pattern" filename.txt - Case-insensitive search
#   ls | grep ".py"               - Pipeline filter: find all python files

# print("--- 4. SEARCHING CONTENT WITH GREP ---")

# Let's search inside logs.txt for any lines containing "Initialized" or "Model"
# We can simulate grep in Python by scanning lines and matching substrings:
def simulate_grep(pattern, filepath, case_insensitive=False):
    matches = []
    search_pat = pattern.lower() if case_insensitive else pattern
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            match_line = line.lower() if case_insensitive else line
            if search_pat in match_line:
                matches.append(line.strip())
    return matches

results = simulate_grep("AI", output_file)
print(f"Grep search results for 'AI' in logs.txt:")
for res in results:
    print(f"  Matched line: {res}")


# Cleanup sandbox directory
if sandbox_dir.exists():
    shutil.rmtree(sandbox_dir)
    print("\nCleaned up cli_sandbox temporary folder.")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Running "rm -rf /" or removing files blindly
#   'rm' is permanent! There is NO Recycle Bin / Trash in the command line.
#   Always verify your paths before running 'rm' commands.

# MISTAKE 2: Confusion between relative and absolute paths
#   cd sandbox  -> relative (works only if 'sandbox' is inside your current folder)
#   cd /sandbox -> absolute (attempts to go to '/' folder at root and find 'sandbox')

# MISTAKE 3: Using backslashes instead of forward slashes
#   On Linux/macOS and in python relative paths, always use '/'.
#   Windows terminal (Command Prompt) historically used '\', but Bash and modern Shells use '/'.


# === EXERCISES ================================================================
#
# Exercise 1: Write a function `simulate_ls(path)` that takes a directory path,
#             scans all items, and returns a tuple: (list_of_dirs, list_of_files).
#
# Exercise 2: Write a python program that appends a log status to a file,
#             acting like `echo "Status: OK" >> system.log`.
#
# Exercise 3: Build a custom Python script that mimics `ls | grep "test"` by scanning
#             the current directory and filtering all filenames matching a given keyword.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# def simulate_ls(path):
#     p = Path(path)
#     dirs = [x.name for x in p.glob("*") if x.is_dir()]
#     files = [x.name for x in p.glob("*") if x.is_file()]
#     return dirs, files
#
# Exercise 3:
# def ls_grep(keyword):
#     return [x.name for x in Path(".").glob("*") if keyword.lower() in x.name.lower()]


# === KEY TAKEAWAYS ============================================================
#
# - Shell utilities are extremely fast, powerful, and standard across servers.
# - Navigating paths and working directories is key to executing files.
# - Piping allows small tools to chain together to solve massive operations.
# - Working safely with file system mutations prevents data loss during AI deployments.
