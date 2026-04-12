# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 18: Practical Python
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - Real project structure (folders, files, organization)
    - File paths (relative, absolute, pathlib)
    - Reading and writing files (text, CSV, JSON)
    - The with statement (context managers)
    - Organizing code into modules
    - The if __name__ == "__main__" pattern
    - Environment variables and .env files
    - Putting it all together: a mini project

  Why this matters for AI:
    Knowing Python syntax is one thing. Building a real project that loads
    data from files, processes it, saves results, and has clean organization
    is what separates a student from a practitioner. Every AI project has
    a structure: data folders, source code folders, configuration files,
    and output directories.

  Estimated time: 35 minutes

===============================================================================
"""


# === PROJECT STRUCTURE ========================================================
#
# A well-organized project looks like this:
#
#   my_ai_project/
#   |-- .venv/                  # Virtual environment (never commit to git)
#   |-- data/
#   |   |-- raw/                # Original, unmodified data
#   |   |-- processed/          # Cleaned, transformed data
#   |   +-- output/             # Results, predictions
#   |-- src/                    # Source code
#   |   |-- __init__.py         # Makes src a Python package
#   |   |-- data_loader.py      # Functions for loading data
#   |   |-- preprocessing.py    # Data cleaning functions
#   |   |-- model.py            # Model training and prediction
#   |   +-- utils.py            # Helper functions
#   |-- tests/                  # Unit tests
#   |   +-- test_utils.py
#   |-- notebooks/              # Jupyter notebooks for exploration
#   |-- .env                    # Environment variables (API keys)
#   |-- .gitignore              # Files to exclude from git
#   |-- README.md               # Project documentation
#   |-- requirements.txt        # Package dependencies
#   +-- main.py                 # Entry point
#
# Key principles:
# - Separate data from code
# - Separate raw data from processed data
# - Keep configuration separate from logic
# - Never commit secrets (.env) or virtual environments (.venv) to git


# === FILE PATHS ===============================================================
#
# A file path tells Python WHERE a file is on your computer.
#
# There are two types:
#
# ABSOLUTE path: The full path from the root of your file system
#   Linux/Mac:  /home/prawin/Documents/GitHub/py4ai/data/input.csv
#   Windows:    C:\Users\prawin\Documents\GitHub\py4ai\data\input.csv
#
# RELATIVE path: The path from your CURRENT working directory
#   data/input.csv           (file is in a data subfolder)
#   ../other_project/file.py (.. means "go up one folder")
#
# Relative paths are preferred because they work on any computer.

import os
from pathlib import Path

# Current working directory:
print(f"Current directory: {os.getcwd()}")

# --- pathlib (modern, recommended) ---
project_dir = Path(".")
data_dir = project_dir / "data"
output_file = data_dir / "output" / "results.csv"

print(f"Project: {project_dir.resolve()}")   # Full absolute path
print(f"Data dir: {data_dir}")
print(f"Output: {output_file}")


"""Why use resolve() instead of just print(project_dir)?
If you just print project_dir, it will simply output .—which isn't very helpful if you're trying to debug where your AI model is saving its data.

By using project_dir.resolve(), you get the "Truth":

Without resolve: .

With resolve: /home/prawin/Documents/GitHub/py4ai"""

# pathlib advantages:
# - / operator for joining paths (cleaner than os.path.join)
# - Works on all operating systems automatically
# - Rich methods: .exists(), .is_file(), .is_dir(), .suffix, .stem, .name

# Check if path exists:
print(f"\nData dir exists: {data_dir.exists()}")

# Get file info:
this_file = Path(__file__) if "__file__" in dir() else Path("18_practical_python.py")
if this_file.exists():
    print(f"This file: {this_file.name}")
    print(f"Extension: {this_file.suffix}")
    print(f"Name without extension: {this_file.stem}")
    print(f"Parent directory: {this_file.parent}")


# === CREATING DIRECTORIES ====================================================

from pathlib import Path

# Create directories (with parents=True, creates all missing parent folders):
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)                    # Create data/
(data_dir / "raw").mkdir(exist_ok=True)          # Create data/raw/
(data_dir / "processed").mkdir(exist_ok=True)    # Create data/processed/
(data_dir / "output").mkdir(exist_ok=True)       # Create data/output/

print("Created project data directories")


# === READING AND WRITING TEXT FILES ==========================================
#
# The with statement (context manager) is the proper way to work with files.
# It automatically closes the file when you are done, even if an error occurs.

# --- Writing a text file ---
with open("data/raw/sample.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("This is line 2.\n")
    f.write("Python is great for AI.\n")

print("Wrote data/raw/sample.txt")

# --- Reading a text file ---
with open("data/raw/sample.txt", "r") as f:
    content = f.read()          # Read entire file as a string
print(f"\nFile contents:\n{content}")

# Read line by line (memory efficient for large files):
with open("data/raw/sample.txt", "r") as f:
    for line_number, line in enumerate(f, start=1):  # enumerate() was covered in 07_loops.py
        print(f"  Line {line_number}: {line.strip()}")

# Read all lines into a list:
with open("data/raw/sample.txt", "r") as f:
    lines = f.readlines()
print(f"\nTotal lines: {len(lines)}")

# --- Appending to a file (adds to end, does not overwrite) ---
with open("data/raw/sample.txt", "a") as f:
    f.write("This line was appended.\n")


# === READING AND WRITING CSV FILES ============================================
#
# CSV (Comma-Separated Values) is one of the most common data formats.

import csv

# --- Writing CSV ---
headers = ["name", "age", "city", "score"]
rows = [
    ["Alice", 25, "New York", 92],
    ["Bob", 30, "London", 85],
    ["Charlie", 35, "Paris", 78],
    ["Dave", 28, "Tokyo", 88],
]

with open("data/raw/students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)       # Write header
    writer.writerows(rows)         # Write all data rows

print("\nWrote data/raw/students.csv")

# --- Reading CSV ---
with open("data/raw/students.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)          # First row is the header
    print(f"Columns: {header}")
    for row in reader:
        print(f"  {row[0]}: age={row[1]}, city={row[2]}, score={row[3]}")

# --- CSV with DictReader (access by column name) ---
with open("data/raw/students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']} from {row['city']}: {row['score']}")

# For more complex CSV work, use pandas (covered in lesson 17):
# import pandas as pd
# df = pd.read_csv("data/raw/students.csv")


# === READING AND WRITING JSON FILES ==========================================
#
# JSON is the standard format for configuration, API data, and structured text.

import json

# --- Writing JSON ---
config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000,
    "training": {
        "epochs": 10,
        "batch_size": 32,
        "learning_rate": 0.001
    },
    "features": ["text", "metadata", "embeddings"]
}

with open("data/raw/config.json", "w") as f:
    json.dump(config, f, indent=2)

print("\nWrote data/raw/config.json")

# --- Reading JSON ---
with open("data/raw/config.json", "r") as f:
    loaded_config = json.load(f)

print(f"Model: {loaded_config['model']}")
print(f"Learning rate: {loaded_config['training']['learning_rate']}")
print(f"Features: {loaded_config['features']}")


# === THE with STATEMENT (CONTEXT MANAGERS) ====================================
#
# The with statement ensures resources are properly cleaned up.
# Without it, you risk leaving files open (which can cause data loss).

# WITHOUT with (bad):
# f = open("file.txt", "r")
# content = f.read()
# f.close()      # What if an error happens before this line?

# WITH with (good):
# with open("file.txt", "r") as f:
#     content = f.read()
# File is automatically closed here, even if an error occurred.

# You can open multiple files at once:
# with open("input.txt", "r") as fin, open("output.txt", "w") as fout:
#     for line in fin:
#         fout.write(line.upper())


# === ORGANIZING CODE INTO MODULES =============================================
#
# As your project grows, put related functions into separate .py files.

# Example: src/text_utils.py
# This would be a separate file in a real project:

# --- src/text_utils.py ---
def clean_text(text):
    """Remove extra whitespace and convert to lowercase."""
    return " ".join(text.lower().split())

def count_words(text):
    """Count the number of words in a text."""
    return len(text.split())

def extract_keywords(text, min_length=4):
    """Extract unique words above a minimum length."""
    words = clean_text(text).split()
    return sorted(set(w for w in words if len(w) >= min_length))

# --- In your main.py, you would import these: ---
# from src.text_utils import clean_text, count_words, extract_keywords

# For now, let's use them directly:
sample = "  Hello World!  This is a  SAMPLE text for testing.  "
print(f"\nOriginal: '{sample}'")
print(f"Cleaned: '{clean_text(sample)}'")
print(f"Word count: {count_words(sample)}")
print(f"Keywords: {extract_keywords(sample)}")


# === THE if __name__ == "__main__" PATTERN ====================================
#
# This is one of the most important patterns in Python. It lets a file
# work as BOTH a runnable script AND an importable module.

def process_data(data):
    """Process a list of numbers."""
    return [x * 2 for x in data if x > 0]

def generate_report(results):
    """Print a summary report."""
    print(f"Processed {len(results)} items")
    print(f"Sum: {sum(results)}")
    print(f"Average: {sum(results)/len(results):.1f}")

# This block runs ONLY when the file is executed directly:
# If someone imports this file (from lesson18 import process_data),
# this block will NOT run.
if __name__ == "__main__":
    data = [1, -2, 3, 4, -5, 6]
    results = process_data(data)
    generate_report(results)


# === ENVIRONMENT VARIABLES ====================================================
#
# Environment variables store configuration and SECRETS (like API keys)
# outside your code. Never put API keys directly in your source files.

import os

# Reading environment variables:
home_dir = os.getenv("HOME", "Not set")
user = os.getenv("USER", "Unknown")
print(f"\nHome directory: {home_dir}")
print(f"User: {user}")

# For API keys, you would do:
# api_key = os.getenv("OPENAI_API_KEY")
# if api_key is None:
#     raise ValueError("OPENAI_API_KEY not set! Add it to your .env file")

# --- Using .env files ---
# Create a file called .env in your project root:
#   OPENAI_API_KEY=sk-abc123...
#   DATABASE_URL=postgresql://localhost/mydb
#   DEBUG=true
#
# Then load it with python-dotenv:
#   pip install python-dotenv
#
#   from dotenv import load_dotenv
#   load_dotenv()  # Loads .env file into environment
#   api_key = os.getenv("OPENAI_API_KEY")
#
# NEVER commit .env files to git. Add .env to your .gitignore.


# === PUTTING IT ALL TOGETHER: MINI PROJECT ===================================
#
# Let's combine everything into a small but realistic data processing project.

import json
import csv
from pathlib import Path
from collections import Counter

def load_student_data(filepath):
    """Load student data from a CSV file."""
    students = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["age"] = int(row["age"])
            row["score"] = int(row["score"])
            students.append(row)
    return students

def analyze_students(students):
    """Perform analysis on student data."""
    scores = [s["score"] for s in students]
    cities = [s["city"] for s in students]

    return {
        "total_students": len(students),
        "average_score": sum(scores) / len(scores),
        "highest_score": max(scores),
        "lowest_score": min(scores),
        "city_distribution": dict(Counter(cities)),
        "top_student": max(students, key=lambda s: s["score"])["name"]
    }

def save_report(analysis, filepath):
    """Save analysis results to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(analysis, f, indent=2)

def print_report(analysis):
    """Display a formatted analysis report."""
    print("\n" + "=" * 40)
    print("  STUDENT ANALYSIS REPORT")
    print("=" * 40)
    print(f"  Total students: {analysis['total_students']}")
    print(f"  Average score:  {analysis['average_score']:.1f}")
    print(f"  Highest score:  {analysis['highest_score']}")
    print(f"  Lowest score:   {analysis['lowest_score']}")
    print(f"  Top student:    {analysis['top_student']}")
    print(f"\n  City distribution:")
    for city, count in analysis["city_distribution"].items():
        print(f"    {city}: {count} student(s)")
    print("=" * 40)


# Run the mini project:
if __name__ == "__main__":
    # Setup
    input_file = Path("data/raw/students.csv")
    output_file = Path("data/output/analysis.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Pipeline
    students = load_student_data(input_file)
    analysis = analyze_students(students)
    save_report(analysis, output_file)
    print_report(analysis)

    print(f"\n  Report saved to: {output_file}")

    # Cleanup demo files (comment out to keep them)
    import shutil  # Built-in module for high-level file operations
    if Path("data").exists():
        shutil.rmtree("data")      # Recursively remove the data directory we created
    for f in ["salary_chart.png", "temperature_chart.png",
              "scores_histogram.png", "scatter_plot.png",
              "student_analysis.csv"]:
        if Path(f).exists():
            Path(f).unlink()
    print("  Cleaned up demo files")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Using backslashes in file paths
# Wrong (Windows-specific and breaks on Mac/Linux):
#   path = "data\raw\file.csv"  # \r is actually a carriage return!
# Right:
#   path = "data/raw/file.csv"        # Forward slashes work everywhere
#   path = Path("data") / "raw" / "file.csv"  # pathlib (best)

# MISTAKE 2: Not using with for files
# Wrong:
#   f = open("file.txt")
#   data = f.read()
#   # If error here, file never closes!
# Right:
#   with open("file.txt") as f:
#       data = f.read()

# MISTAKE 3: Hardcoding absolute paths
# Wrong:
#   df = pd.read_csv("/home/prawin/Documents/data.csv")
# Right:
#   df = pd.read_csv("data/raw/data.csv")  # Relative path

# MISTAKE 4: Committing secrets to git
# Create a .gitignore file with:
#   .env
#   .venv/
#   __pycache__/
#   *.pyc
#   data/output/


# === EXERCISES ================================================================
#
# Exercise 1: Create a function that reads a text file and returns a dict
#             with: line_count, word_count, char_count, most_common_word.
#
# Exercise 2: Create a project structure with folders: src/, data/raw/,
#             data/processed/, and tests/. Write a README.md file in the
#             root explaining your project.
#
# Exercise 3: Write a function that loads a JSON config file, overrides
#             any values passed as keyword arguments, and saves the
#             updated config back.
#
# Exercise 4: Build a simple CSV data pipeline:
#             a) Create a CSV with 20 rows of fake student data
#             b) Read and filter to students with score > 80
#             c) Save the filtered data to a new CSV
#             d) Print a summary report


# === SOLUTIONS ================================================================
#
# Exercise 1:
# def analyze_text_file(filepath):
#     with open(filepath, "r") as f:
#         text = f.read()
#     lines = text.strip().split("\n")
#     words = text.lower().split()
#     from collections import Counter
#     most_common = Counter(words).most_common(1)[0][0] if words else None
#     return {
#         "line_count": len(lines),
#         "word_count": len(words),
#         "char_count": len(text),
#         "most_common_word": most_common
#     }
#
# Exercise 3:
# def update_config(filepath, **overrides):
#     import json
#     with open(filepath, "r") as f:
#         config = json.load(f)
#     config.update(overrides)
#     with open(filepath, "w") as f:
#         json.dump(config, f, indent=2)
#     return config


# === KEY TAKEAWAYS ============================================================
#
# - Organize projects with separate folders for data, source, and tests
# - Use pathlib for file paths (cross-platform, clean syntax)
# - Always use the with statement for file operations
# - CSV for tabular data, JSON for structured/nested data
# - Put reusable functions in separate modules (files)
# - Use if __name__ == "__main__" to make files work as both scripts and modules
# - Store secrets in environment variables or .env files, never in code
# - Use .gitignore to keep secrets and generated files out of git


# === CONGRATULATIONS! =========================================================
#
# You have completed the Python for AI course!
#
# Here is what you now know:
#   - Python fundamentals (variables, types, operators, strings)
#   - Control flow (if/elif/else, for/while loops)
#   - Data structures (lists, dicts, tuples, sets)
#   - Functions (defining, parameters, return values, scope)
#   - Packages (importing, pip, standard library)
#   - APIs (HTTP requests, JSON, error handling)
#   - Data analysis (pandas, matplotlib, visualization)
#   - Practical skills (file I/O, project structure, modules)
#
# Next steps to continue your AI journey:
#   1. Learn NumPy for numerical computing
#   2. Deepen your pandas skills with real datasets
#   3. Study scikit-learn for classical machine learning
#   4. Explore PyTorch or TensorFlow for deep learning
#   5. Try the Hugging Face transformers library for NLP
#   6. Build a project: chatbot, recommendation system, or data dashboard
#
# The best way to learn is to BUILD something. Pick a problem you care
# about and use Python to solve it. You have all the fundamentals. Now go
# build something amazing.
