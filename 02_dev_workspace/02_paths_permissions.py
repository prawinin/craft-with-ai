# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 20: Paths, Environments & Permissions
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - Path Shortcuts: Absolute vs. Relative, Home (~), Current (.), and Parent (..)
    - Environment Variables: Reading, setting, and using .env configuration files
    - The PATH Variable: How the operating system locates python, git, and scripts
    - File Permissions: Understanding read, write, execute (chmod)

  Why this matters for AI:
    When you deploy an AI agent or backend server, the app must read secret
    API keys from the environment, resolve file paths to read local datasets,
    and have correct executable permissions to run shell scripts. Improper
    permission management is the #1 reason deployed containers crash in cloud systems.

  Estimated time: 20 minutes

===============================================================================
"""

import os
import sys
from pathlib import Path

# === PATH SHORTCUTS ==========================================================
#
# WHAT IS AN ABSOLUTE VS. RELATIVE PATH?
#   An Absolute Path is like a complete mailing address with a postal code and country
#   (e.g., "1600 Amphitheatre Pkwy, Mountain View, CA"). It starts from the system's root
#   (`/` on Mac/Linux or `C:\` on Windows) and works anywhere, regardless of where you are standing.
#   A Relative Path is like giving directions from your current spot ("Walk two doors down
#   and turn left"). If you move to a different room, "two doors down" points to a completely
#   different place!
#
# Path symbols represent shortcuts to navigate directories:
#   .   - Represents the CURRENT directory (e.g., ./script.py)
#   ..  - Represents the PARENT directory (e.g., ../data/dataset.csv goes up 1 level)
#   ~   - Represents the user's HOME directory (e.g., /home/prawin or /Users/prawin)
#   /   - Represents the system root (the absolute base of the operating system)

# print("--- 1. PATH RESOLUTIONS ---")

cwd = Path(".")
print(f"Current Directory (.): {cwd.resolve()}")
print(f"Parent Directory (..): {cwd.resolve().parent}")

# User's Home Directory (equivalent to '~')
home_dir = Path.home()
print(f"User Home Directory (~): {home_dir}")

# Resolving absolute paths programmatically
relative_path = Path("data/raw/dataset.csv")
absolute_path = relative_path.resolve()
print(f"Relative: {relative_path}")
print(f"Resolved Absolute: {absolute_path}")


# === ENVIRONMENT VARIABLES & .env ============================================
#
# WHAT IS AN ENVIRONMENT VARIABLE?
#   Think of your operating system as an airport, and your running program as a passenger.
#   Instead of tattooing flight details directly onto the passenger's skin (hardcoding API keys),
#   the airport puts up notice boards (Environment Variables) that say "Gate=12" or "Timezone=EST".
#   Any passenger can look up at the notice board to get context. This keeps secrets out of your
#   source code so they don't leak when you share your project!
#
# Environment variables store config values outside your code (like API keys).
#
# Linux Command Line:
#   export OPENAI_API_KEY="sk-12345"  - Set an environment variable in the active terminal
#   echo $OPENAI_API_KEY              - Read the variable
#
# The .env File:
#   To prevent setting variables manually every session, developer setups use
#   a `.env` file loaded at startup.

# print("\n--- 2. ENVIRONMENT VARIABLES & SECRETS ---")

# Setting an environment variable programmatically in Python (mimics 'export DB_PORT=5432')
os.environ["DB_PORT"] = "5432"

# Reading environment variables (mimics 'echo $DB_PORT' and 'echo $USER')
db_port = os.getenv("DB_PORT", "Default: 5432")
current_user = os.getenv("USER", "Unknown User")

print(f"Retrieved DB_PORT: {db_port}")
print(f"System User: {current_user}")

# --- Simulating .env parser ---
# Instead of installing python-dotenv, we can parse it easily in standard Python:
def parse_env_file(content):
    variables = {}
    for line in content.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            variables[key.strip()] = val.strip().strip('"').strip("'")
    return variables

sample_dotenv = """
# Database Configuration
DATABASE_URL="postgresql://localhost/mydb"
API_KEY=secret_llm_key_9988
DEBUG=True
"""

config = parse_env_file(sample_dotenv)
print("\nParsed .env properties:")
for k, v in config.items():
    print(f"  {k} = {v}")


# === THE PATH VARIABLE =======================================================
#
# WHAT IS THE PATH VARIABLE?
#   Imagine your computer is a chef in a kitchen, and when you type a command like `python`
#   or `git`, you are yelling "pass me the blender!" The chef doesn't search the entire house
#   for the blender; they only look in a specific list of drawers. The `PATH` variable is
#   literally that list of drawers (folders). If a program isn't in one of those drawers,
#   the shell throws a "command not found" error!
#
# When you type `python` or `git` in a shell, how does the terminal know which
# executable to run? It searches folders listed in the `PATH` environment variable.
#
# Shell utilities:
#   which python   - Shows the absolute location of the 'python' executable
#   echo $PATH     - Lists all folders checked for command matching

# print("\n--- 3. SYSTEM PATH BINARIES ---")

# Let's inspect the system executable folders
sys_paths = os.environ.get("PATH", "").split(os.pathsep)
print(f"System search paths list (first 3 directories in PATH):")
for path_item in sys_paths[:3]:
    print(f"  - {path_item}")

# Find where the Python executable itself resides
executable_binary = sys.executable
print(f"\nRunning Python Binary: {executable_binary}")


# === FILE PERMISSIONS (chmod) ================================================
#
# WHAT IS CHMOD?
#   `chmod` stands for "Change Mode". Think of every file on your computer as a document in
#   a shared office. It has checkboxes for three types of people: Owner (the creator), Group (co-workers),
#   and Others (everyone else). Each class can be allowed to READ (r), WRITE (w), or RUN/EXECUTE (x)
#   the file. By running `chmod`, you are checking or unchecking these boxes.
#   "chmod +x" is like turning a regular text file into an active tool that you're allowed to run.
#   Numbers like "755" are just a shortcut representing combinations of these rights (e.g., 7 means Read+Write+Execute).
#
# Files have three permission classes: Owner, Group, and Others.
# Each class can have:
#   Read (r / 4)       - Permission to view content
#   Write (w / 2)      - Permission to edit content
#   Execute (x / 1)    - Permission to run file (like running shell scripts)
#
# Linux Command Line:
#   chmod +x run.sh   - Grant execution permission to run.sh (so you can run ./run.sh)
#   chmod 755 file.py - Sets Owner to Read/Write/Execute (7), and others to Read/Execute (5)

# print("\n--- 4. PERMISSIONS & EXECUTABILITY ---")

# Create a temporary script file
temp_script = Path("temp_script.sh")
temp_script.write_text("#!/bin/bash\necho 'Executing script!'\n", encoding="utf-8")

# In Python, we check access permissions using os.access():
is_readable = os.access(temp_script, os.R_OK)
is_writable = os.access(temp_script, os.W_OK)
is_executable = os.access(temp_script, os.X_OK)

print(f"File permissions check:")
print(f"  Readable: {is_readable}")
print(f"  Writable: {is_writable}")
print(f"  Executable: {is_executable} (cannot run script directly if false)")

# Grant execution rights (mimics 'chmod +x temp_script.sh')
# S_IXUSR = Execution permission for user owner
import stat
current_mode = temp_script.stat().st_mode
temp_script.chmod(current_mode | stat.S_IXUSR)

print(f"  Executable after chmod +x: {os.access(temp_script, os.X_OK)}")

# Clean up
if temp_script.exists():
    temp_script.unlink()


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Committing .env files to Github
#   Never push secret API keys. Always add `.env` to your `.gitignore`.
#   Create a `.env.example` file instead with empty keys (e.g., API_KEY=YOUR_KEY_HERE).

# MISTAKE 2: Running scripts with "Permission Denied"
#   If you try running `./run.sh` and get "Permission Denied", you forgot to grant
#   execute rights. Run `chmod +x run.sh` to fix it.

# MISTAKE 3: Reading env variables directly before loading
#   Running `os.getenv("API_KEY")` returns `None` unless you have loaded the dotenv
#   or exported the keys prior to starting the Python session.


# === EXERCISES ================================================================
#
# Exercise 1: Write a function `check_environment_secrets(required_keys)` that loops
#             over a list of strings, verifies if they are set in `os.environ`,
#             and raises a ValueError listing all missing keys.
#
# Exercise 2: Write a python snippet that checks if a file exists, and if it does NOT
#             have executable permission, grants it.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# def check_environment_secrets(required_keys):
#     missing = [key for key in required_keys if os.getenv(key) is None]
#     if missing:
#         raise ValueError(f"Missing environment secrets: {', '.join(missing)}")
#
# Exercise 2:
# import stat
# def make_executable(filepath):
#     p = Path(filepath)
#     if p.exists() and not os.access(p, os.X_OK):
#         p.chmod(p.stat().st_mode | stat.S_IXUSR)
#         return True
#     return False


# === KEY TAKEAWAYS ============================================================
#
# - Env variables keep code dry, secure, and easily configurable on production servers.
# - Shortcuts like '.' and '..' provide relative referencing that works on any machine.
# - Executable modes are required for running automated scripts and containers.
# - The PATH directory variable dictates where system shells look to execute binary files.
