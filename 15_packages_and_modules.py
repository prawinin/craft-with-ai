# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 15: Packages and Modules
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - What modules and packages are
    - Importing: import, from...import, as (aliasing)
    - Python's Standard Library (built-in modules)
    - Installing third-party packages with pip
    - Virtual environments (why and how)
    - Creating your own modules
    - Common AI/data science packages overview

  Why this matters for AI:
    Nobody builds AI from scratch. You stand on the shoulders of giants by
    importing packages: requests for APIs, pandas for data, numpy for
    math, scikit-learn for ML, torch/tensorflow for deep learning. Knowing
    how to find, install, and import packages is what unlocks the entire
    Python AI ecosystem.

  Estimated time: 25 minutes

===============================================================================
"""


# === WHAT IS A MODULE? ========================================================
#
# A MODULE is simply a .py file containing Python code (functions, variables,
# classes) that you can reuse in other files.
#
# A PACKAGE is a directory of modules, organized with an __init__.py file.
#
# Think of it like a toolbox:
#   - A module is one tool (like a hammer)
#   - A package is a toolbox containing multiple tools
#   - The standard library is a massive hardware store with every tool
#     you could need
#   - Third-party packages are specialty tools you order online (pip install)


# === IMPORTING MODULES ========================================================

# --- Pattern 1: Import the whole module ---
import math

print(math.sqrt(16))     # 4.0
print(math.pi)           # 3.141592653589793
print(math.ceil(3.2))    # 4 (round up)
print(math.floor(3.8))   # 3 (round down)

# You must prefix with the module name: math.sqrt(), not sqrt()


# --- Pattern 2: Import specific items ---
from math import sqrt, pi

print(sqrt(25))           # 5.0 (no need for math. prefix)
print(pi)                 # 3.14159...


# --- Pattern 3: Import with an alias ---
import datetime as dt

today = dt.date.today()
print(today)

# In AI, you will see these aliases constantly:
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import tensorflow as tf
# import torch


# --- Pattern 4: Import everything (generally AVOID this) ---
# from math import *
# This imports all names from math into your namespace.
# Problem: you do not know where functions came from, and names can collide.
# Use this only in interactive sessions for quick testing, never in real code.


# === THE STANDARD LIBRARY ====================================================
#
# Python comes with a huge collection of built-in modules. No installation
# needed. Here are the most useful ones:

# --- random: Generate random numbers ---
import random

number = random.randint(1, 10)          # Random integer from 1 to 10
choice = random.choice(["apple", "banana", "orange"])  # Random pick
items = [1, 2, 3, 4, 5]
random.shuffle(items)                    # Shuffle in place
print(f"Random: {number}, Choice: {choice}, Shuffled: {items}")

# For reproducible results (crucial in AI for experiment comparison):
random.seed(42)                          # Same seed = same "random" numbers
print(random.randint(1, 100))           # Always gives the same result with seed 42


# --- datetime: Dates and times ---
import datetime

today = datetime.date.today()
now = datetime.datetime.now()
print(f"Today: {today}")
print(f"Now: {now}")
print(f"Formatted: {now.strftime('%Y-%m-%d %H:%M')}")

# Date arithmetic:
week_ago = today - datetime.timedelta(days=7)
print(f"One week ago: {week_ago}")


# --- os: Operating system interaction ---
import os

current_dir = os.getcwd()               # Current working directory
print(f"Current directory: {current_dir}")
print(f"Files here: {os.listdir('.')[:5]}")  # List first 5 files

# Path manipulation:
path = os.path.join("data", "models", "best_model.pt")
print(f"Path: {path}")
print(f"Exists: {os.path.exists(path)}")


# --- pathlib: Modern path handling (preferred over os.path) ---
from pathlib import Path

project_dir = Path(".")
data_dir = project_dir / "data"          # / operator builds paths
print(f"Data dir: {data_dir}")
print(f"Is directory: {data_dir.is_dir()}")

# List all Python files:
py_files = list(project_dir.glob("*.py"))
print(f"Python files: {[f.name for f in py_files[:5]]}")


# --- json: Read and write JSON data ---
import json

# Python dict to JSON string:
data = {"name": "Alice", "age": 30, "scores": [85, 92, 78]}
json_string = json.dumps(data, indent=2)
print(json_string)

# JSON string back to Python dict:
parsed = json.loads(json_string)
print(parsed["name"])                    # "Alice"

# Read/write JSON files:
# (The 'with open' syntax for files is covered in 18_practical_python.py)
# with open("data.json", "w") as f:
#     json.dump(data, f, indent=2)
# with open("data.json", "r") as f:
#     loaded = json.load(f)


# --- collections: Specialized data structures ---
from collections import Counter, defaultdict, OrderedDict

# Counter: count occurrences
words = "the cat sat on the mat the cat".split()
word_freq = Counter(words)
print(word_freq)                       # Counter({'the': 3, 'cat': 2, ...})
print(word_freq.most_common(2))        # [('the', 3), ('cat', 2)]

# defaultdict: dict with default values
word_lengths = defaultdict(list)
for word in words:
    word_lengths[len(word)].append(word)
print(dict(word_lengths))              # {3: ['the', 'cat', 'sat', ...], 2: ['on']}


# --- time: Timing and delays ---
import time

start = time.time()
# ... some operation ...
time.sleep(0.1)  # Sleep for 0.1 seconds
elapsed = time.time() - start
print(f"Elapsed: {elapsed:.3f} seconds")

# Useful for timing model training and inference


# === INSTALLING THIRD-PARTY PACKAGES =========================================
#
# Python's real power comes from third-party packages. Install them with pip.
#
# In your terminal (with virtual environment activated):
#
#   pip install requests           # Single package
#   pip install pandas numpy       # Multiple packages
#   pip install requests==2.31.0   # Specific version
#   pip install -r requirements.txt  # All packages from a file
#
# Key commands:
#   pip list                       # See installed packages
#   pip show requests              # Package details
#   pip freeze > requirements.txt  # Save all package versions to a file
#   pip install --upgrade requests # Update a package

# IMPORTANT: Always install in a virtual environment, never system-wide!
# This keeps each project's dependencies separate.


# === VIRTUAL ENVIRONMENTS =====================================================
#
# A virtual environment is an isolated Python installation for your project.
#
# Why: Different projects may need different package versions.
# Project A might need requests 2.28, Project B might need requests 2.31.
# Without virtual environments, they would conflict.
#
# How to create and use:
#
#   python3 -m venv .venv           # Create (Linux/macOS)
#   python -m venv .venv            # Create (Windows)
#
#   source .venv/bin/activate       # Activate (Linux/macOS)
#   .venv\Scripts\activate          # Activate (Windows)
#
#   deactivate                      # Deactivate
#
# When active, your terminal shows (.venv) at the start of the prompt.
# All pip install commands go into this isolated environment.


# === USING THIRD-PARTY PACKAGES ===============================================

# requests: HTTP requests (API calls)
# First: pip install requests
import requests

response = requests.get("https://api.github.com")
print(f"Status: {response.status_code}")  # 200 = success

# IMPORTANT: your file name should NOT be the same as a module name.
# If your file is called "requests.py", Python will try to import your
# file instead of the real requests library. This is called a circular
# import and will cause an error.


# === AI/DATA SCIENCE PACKAGES OVERVIEW ========================================
#
# Here are the packages you will use as you progress in AI:
#
# DATA HANDLING:
#   pandas       -- DataFrames (spreadsheet-like data structures)
#   numpy        -- Fast numerical arrays and math operations
#
# VISUALIZATION:
#   matplotlib   -- Charts and plots
#   seaborn      -- Statistical visualizations (built on matplotlib)
#   plotly       -- Interactive charts
#
# MACHINE LEARNING:
#   scikit-learn -- Classical ML (regression, classification, clustering)
#   xgboost      -- Gradient boosting (competition-winning algorithms)
#
# DEEP LEARNING:
#   torch        -- PyTorch (research-focused deep learning)
#   tensorflow   -- TensorFlow (production-focused deep learning)
#
# NATURAL LANGUAGE PROCESSING:
#   transformers -- Hugging Face (pre-trained language models)
#   langchain    -- Building AI agents and chains
#   openai       -- OpenAI API client (GPT, DALL-E, etc.)
#
# WEB/API:
#   requests     -- HTTP requests
#   fastapi      -- Building APIs
#   flask        -- Web applications
#
# Install them as you need them:
#   pip install pandas numpy matplotlib scikit-learn


# === CREATING YOUR OWN MODULES ================================================
#
# Any .py file can be imported as a module. This is how you organize
# larger projects.

# Suppose you have a file called utils.py with:
# def clean_text(text):
#     return text.strip().lower()
#
# def count_words(text):
#     return len(text.split())

# You can import and use it from another file:
# from utils import clean_text, count_words
# result = clean_text("  Hello World  ")

# The if __name__ == "__main__" pattern:
# This block runs only when the file is executed directly,
# NOT when it is imported as a module.

def main():
    print("This runs when executed directly")
    print("But NOT when imported")

if __name__ == "__main__":
    main()

# This is a standard pattern in Python. You will see it everywhere.
# It lets a file serve dual purpose: both as a runnable script AND as
# an importable module.


# === REAL-WORLD EXAMPLE: BUILDING A UTILITY MODULE ============================

# In a real AI project, you might create a utils.py file like this:

def load_config(filepath):
    """Load a JSON configuration file."""
    with open(filepath, "r") as f:
        return json.load(f)

def setup_logging(level="INFO"):
    """Configure logging for the project."""
    import logging
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

def ensure_directory(path):
    """Create directory if it does not exist."""
    os.makedirs(path, exist_ok=True)

def timer(description="Operation"):
    """Time an operation using a context manager."""
    class Timer:
        def __enter__(self):
            self.start = time.time()
            return self
        def __exit__(self, *args):
            elapsed = time.time() - self.start
            print(f"{description} took {elapsed:.3f}s")
    return Timer()

# Usage:
# with timer("Data loading"):
#     data = load_data("big_file.csv")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Naming your file the same as a module
# If you create a file called "random.py" and try to import random,
# Python imports YOUR file instead of the standard library module.
# Solution: never name your files after built-in modules.

# MISTAKE 2: Importing everything with *
# from math import *    # Bad: pollutes namespace, hides origins
# from math import sqrt, pi  # Good: explicit and clear

# MISTAKE 3: Not using a virtual environment
# Installing globally causes version conflicts between projects.
# Always create a .venv for each project.

# MISTAKE 4: Forgetting to install
# import pandas   # ModuleNotFoundError if not installed
# Fix: pip install pandas (in your virtual environment)


# === EXERCISES ================================================================
#
# Exercise 1: Import the random module and write a function that generates
#             a random password of a given length using letters and digits.
#
# Exercise 2: Use the datetime module to calculate how many days until
#             the end of the current year.
#
# Exercise 3: Use the json module to create a dictionary, save it to
#             a JSON file, then read it back and print it.
#
# Exercise 4: Use the collections.Counter to find the 3 most common
#             characters in the string "abracadabra alakazam".
#
# Exercise 5: Use the pathlib module to list all .py files in the current
#             directory and print their sizes in KB.


# === SOLUTIONS ================================================================
#
# Exercise 1:
# import random
# import string
# def generate_password(length=12):
#     chars = string.ascii_letters + string.digits + "!@#$%"
#     return "".join(random.choice(chars) for _ in range(length))
# print(generate_password())
# print(generate_password(20))
#
# Exercise 2:
# import datetime
# today = datetime.date.today()
# end_of_year = datetime.date(today.year, 12, 31)
# days_left = (end_of_year - today).days
# print(f"Days until end of {today.year}: {days_left}")
#
# Exercise 3:
# import json
# data = {"model": "gpt-4", "temperature": 0.7, "max_tokens": 1000}
# with open("config.json", "w") as f:
#     json.dump(data, f, indent=2)
# with open("config.json", "r") as f:
#     loaded = json.load(f)
# print(loaded)
# import os; os.remove("config.json")  # Clean up
#
# Exercise 4:
# from collections import Counter
# text = "abracadabra alakazam"
# freq = Counter(text.replace(" ", ""))
# print(freq.most_common(3))  # [('a', 10), ('b', 2), ('r', 2)]
#
# Exercise 5:
# from pathlib import Path
# for f in sorted(Path(".").glob("*.py")):
#     size_kb = f.stat().st_size / 1024
#     print(f"{f.name}: {size_kb:.1f} KB")


# === KEY TAKEAWAYS ============================================================
#
# - import module / from module import item / import module as alias
# - Standard library: math, random, datetime, os, pathlib, json, collections
# - Third-party packages: install with pip install package_name
# - Always use virtual environments to isolate project dependencies
# - Never name your files the same as built-in modules
# - if __name__ == "__main__" lets files work as both scripts and modules
# - AI ecosystem: pandas, numpy, matplotlib, scikit-learn, torch, transformers


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (16_working_with_apis.py), you will put your knowledge
# to use by calling real APIs over the internet. You will fetch live weather
# data, parse JSON responses, and build a function-based weather tool.
