# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 00: Getting Started
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - What Python actually is (and what it is not)
    - How a computer reads your code
    - What "running a program" means
    - The difference between compiled and interpreted languages
    - Why Python was chosen as the language for AI

  Why this matters for AI:
    Understanding what Python is and how it works gives you the mental model
    you need to debug problems, understand error messages, and reason about
    what your code is doing when you start building AI systems.

  Estimated time: 15 minutes

  How to use this file:
    Read through the comments to understand the concepts.
    Select code blocks and press Shift+Enter to run them in the Interactive
    Window. Experiment by changing values and re-running.

===============================================================================
"""


# === WHAT IS PYTHON? =========================================================
#
# Python is a programming language -- a way to write instructions that a
# computer can follow. Think of it like writing a very precise recipe.
#
# When you cook, you write:
#   "Boil water for 10 minutes"
#
# In Python, you might write:
#   temperature = 100
#   duration = 10
#   boil(water, temperature, duration)
#
# The difference is that a computer follows your instructions EXACTLY.
# It will never "eyeball" something or use common sense. If you say
# "boil 10 minutes", it boils exactly 10 minutes.
#
# This precision is what makes programming powerful -- and also what makes
# bugs happen when your instructions are slightly wrong.


# === HOW DOES PYTHON WORK? ===================================================
#
# There are two main types of programming languages:
#
# COMPILED languages (like C, Java):
#   You write code -> A "compiler" translates ALL of it to machine code
#   -> Then you run the machine code.
#   Analogy: Writing a book, sending it to a translator, getting the full
#   translated book back, then publishing it.
#
# INTERPRETED languages (like Python):
#   You write code -> Python reads it line by line and executes each line
#   immediately.
#   Analogy: Having a live interpreter at a conference who translates each
#   sentence as the speaker says it.
#
# Python is INTERPRETED. This means:
#   - You can run code one line at a time (which is why the Interactive
#     Window works so well)
#   - You see results immediately
#   - It is slower than compiled languages, but much faster to develop with
#   - Most AI work is not bottlenecked by Python's speed because the heavy
#     computation happens in optimized C/C++ libraries under the hood


# === YOUR FIRST PYTHON CODE ==================================================
#
# The simplest thing you can do in Python is print something to the screen.
# Select the line below and press Shift+Enter:

print("Welcome to Python for AI!")

# What just happened:
# 1. Python read the line
# 2. It recognized "print" as a built-in function (a command Python already knows)
# 3. It took the text inside the parentheses
# 4. It displayed that text in the output


# === PYTHON AS A CALCULATOR ==================================================
#
# Python can do math immediately. Try each of these:

print(2 + 2)
print(100 - 37)
print(15 * 4)
print(10 / 3)

# Notice that 10 / 3 gives you 3.3333... Python handles decimal numbers
# automatically. Most programming languages have quirks with decimals --
# Python makes it straightforward.


# === THE PYTHON INTERPRETER ===================================================
#
# When you press Shift+Enter, VS Code sends your code to the Python
# INTERPRETER. The interpreter is the program that reads and executes
# your Python code.
#
# You can think of the relationship like this:
#
#   You (the programmer)
#     |
#     | write code in a .py file
#     v
#   Python Interpreter (reads your code)
#     |
#     | translates to instructions the CPU understands
#     v
#   Computer (executes the instructions)
#
# When an error happens, the interpreter stops and tells you what went wrong.
# This is one of Python's strengths -- the error messages are usually helpful
# and point you to the exact line that failed.


# === WHY PYTHON FOR AI? ======================================================
#
# In the world of AI and machine learning, Python dominates. Here is why:
#
# 1. READABILITY
#    Python code reads like English. Compare:
#
#    Python:  if temperature > 100: print("Too hot!")
#    Java:    if (temperature > 100) { System.out.println("Too hot!"); }
#    C:       if (temperature > 100) { printf("Too hot!\n"); }
#
#    When you are working on complex AI algorithms, you want to focus on the
#    LOGIC, not on semicolons and curly braces.
#
# 2. LIBRARIES
#    Python has thousands of pre-built tools for AI:
#    - NumPy: Fast math on large arrays of numbers
#    - pandas: Working with tabular data (like spreadsheets)
#    - scikit-learn: Classical machine learning
#    - TensorFlow / PyTorch: Deep learning and neural networks
#    - LangChain / OpenAI: Building AI agents and chatbots
#    - matplotlib: Creating charts and visualizations
#
# 3. COMMUNITY
#    Almost every AI research paper publishes its code in Python.
#    Every major AI company (Google, OpenAI, Meta, Anthropic) builds their
#    tools and APIs with Python support first.
#
# 4. THE "GLUE" LANGUAGE
#    Python is often called a glue language. You use Python to connect
#    together powerful components written in C/C++ (which are fast).
#    So you get the ease of Python with the speed of C.
#    When you write model.fit(data), the actual computation happens in
#    optimized C code -- you just control it from Python.


# === KEY CONCEPTS TO REMEMBER ================================================
#
# - Python is an interpreted language: code runs line by line
# - The interpreter is what reads and executes your code
# - Python's strength is readability and its massive library ecosystem
# - For AI work, Python's "slowness" rarely matters because heavy computation
#   is handled by optimized libraries written in C
# - Everything you learn in this course builds toward being able to use those
#   AI libraries effectively


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (01_hello_world.py), you will write your first real Python
# program, learn how the print() function works in detail, and understand
# the concept of "output".
