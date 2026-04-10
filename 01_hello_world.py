# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 01: Hello, World!
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - How the print() function works
    - Printing text, numbers, and multiple values
    - Escape characters (newlines, tabs)
    - Getting input from the user
    - The difference between a script and interactive execution

  Why this matters for AI:
    print() is your primary debugging tool. When your AI model gives
    unexpected results, you will print intermediate values to figure out
    what went wrong. Mastering output is step one.

  Estimated time: 15 minutes

===============================================================================
"""


# === YOUR FIRST PROGRAM ======================================================
#
# By tradition, the first program anyone writes in a new language prints
# "Hello, World!" to the screen. This tradition goes back to 1978.

print("Hello, World!")


# === HOW print() WORKS =======================================================
#
# print() is a FUNCTION. A function is a reusable block of code that does
# something specific. Python comes with many built-in functions, and print()
# is the most basic one.
#
# The structure is:
#   print(what_you_want_to_display)
#
# The parentheses are mandatory. The thing inside them is called an ARGUMENT.

# You can print text (called "strings" -- we will cover this in depth later):
print("I am learning Python for AI")

# You can print numbers:
print(42)
print(3.14159)

# You can print the result of calculations:
print(2 + 2)
print(100 * 365)


# === PRINTING MULTIPLE VALUES ================================================
#
# You can give print() multiple arguments separated by commas.
# Python will put a space between each one automatically.

print("My name is", "Prawin")
print("I am", 22, "years old")
print("Python version:", 3.12)

# The sep parameter changes what goes between values (default is a space):
print("2026", "04", "10", sep="-")     # Output: 2026-04-10
print("usr", "local", "bin", sep="/")  # Output: usr/local/bin

# The end parameter changes what goes at the end (default is a newline):
print("Loading", end="")
print("...", end="")
print(" Done!")
# Output: Loading... Done!  (all on one line)


# === QUOTES: SINGLE vs DOUBLE ================================================
#
# Python accepts both single quotes and double quotes for text. They are
# identical in behavior. Choose one style and stick with it.

print("Hello")   # double quotes
print('Hello')   # single quotes -- exact same result

# When your text contains a quote character, use the other type:
print("It's a beautiful day")    # text has single quote, use double outside
print('She said "hello"')        # text has double quotes, use single outside

# For text that spans multiple lines, use triple quotes:
print("""This is a
multi-line
string""")


# === ESCAPE CHARACTERS ========================================================
#
# Sometimes you need to include special characters in your text. You do this
# with a backslash (\) followed by a character:
#
#   \n  = newline (moves to next line)
#   \t  = tab (indentation)
#   \\  = actual backslash
#   \'  = single quote inside single-quoted string
#   \"  = double quote inside double-quoted string

print("Line one\nLine two\nLine three")
print("Name:\tAlice\nAge:\t30")
print('It\'s Python')
print("Path: C:\\Users\\Documents")


# === GETTING USER INPUT =======================================================
#
# The input() function pauses the program and waits for the user to type
# something. Whatever they type becomes a string value.
#
# NOTE: input() works best when running the file as a script (not in
# Interactive Window). You can skip this section for now and come back later.

# Uncomment the lines below to try (select all 3 lines and run):
# name = input("What is your name? ")
# print("Hello,", name)
# print("Welcome to Python for AI!")

# IMPORTANT: input() ALWAYS returns a string, even if the user types a number.
# We will learn how to convert types in lesson 03.


# === COMMENTS =================================================================
#
# Lines starting with # are COMMENTS. Python ignores them completely.
# Comments are notes for humans reading the code.

# This is a comment -- Python skips this line
print("This line runs")  # You can also put comments at the end of a line

# Good comments explain WHY, not WHAT:
# Bad:  # print hello
# Good: # greet the user when the program starts

# In AI code, comments are crucial for explaining:
# - Why you chose certain model parameters
# - What a complex data transformation does
# - Assumptions your code makes about the input data


# === REAL-WORLD EXAMPLE: SIMPLE AI OUTPUT =====================================
#
# Imagine you are building a simple AI assistant. Even the most advanced
# chatbot ultimately needs to print its response to the user:

user_question = "What is the weather today?"
ai_response = "Based on current data, it is 24 degrees and sunny."

print("User:", user_question)
print("AI:", ai_response)
print("-" * 50)  # Print a separator line (- repeated 50 times. String multiplication is covered in 04_operators.py)

# This pattern -- receiving input, processing it, and printing output --
# is the fundamental loop of every AI application, from ChatGPT to
# self-driving cars.


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Forgetting the parentheses
# Wrong:
#   print "Hello"    # This is Python 2 syntax, it does NOT work in Python 3
# Right:
print("Hello")

# MISTAKE 2: Mismatched quotes
# Wrong:
#   print("Hello')   # Started with double, ended with single
# Right:
print("Hello")

# MISTAKE 3: Forgetting to close the string
# Wrong:
#   print("Hello)    # Missing closing quote
# Right:
print("Hello")


# === EXERCISES ================================================================
#
# Try these yourself before looking at the solutions below.
#
# Exercise 1: Print your full name on one line.
#
# Exercise 2: Print your name, age, and city using a single print() statement
#             with commas.
#
# Exercise 3: Print the following pattern using \n and \t:
#             Name:    Alice
#             Age:     30
#             City:    New York
#
# Exercise 4: Print a line of 40 asterisks (*) using the * operator on a string.
#
# Exercise 5: Print a date in YYYY/MM/DD format using sep="/".


# === SOLUTIONS ================================================================
#
# (Try the exercises yourself first!)
#
# Exercise 1:
# print("Prawin Kumar")
#
# Exercise 2:
# print("Prawin", 22, "Bokaro")
#
# Exercise 3:
# print("Name:\tAlice\nAge:\t30\nCity:\tNew York")
#
# Exercise 4:
# print("*" * 40)
#
# Exercise 5:
# print("2026", "04", "10", sep="/")


# === KEY TAKEAWAYS ============================================================
#
# - print() displays output to the screen
# - You can print strings, numbers, and expressions
# - Use commas to print multiple values with automatic spacing
# - Use sep and end parameters to control formatting
# - Comments (#) are for humans, Python ignores them
# - input() reads text from the user (always returns a string)
# - Escape characters (\n, \t, \\) let you include special characters


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (02_variables.py), you will learn how to store data in
# variables -- giving names to values so you can use them throughout your
# program. This is how every AI program manages its data.
