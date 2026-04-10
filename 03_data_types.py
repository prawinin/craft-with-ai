# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 03: Data Types
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - The four fundamental data types: int, float, str, bool
    - How to check and convert between types
    - Type behavior and edge cases
    - The None type
    - Why types matter in AI programming

  Why this matters for AI:
    AI models are extremely particular about data types. A neural network
    expects numerical inputs as floats, not strings. A classification model
    returns integers representing categories. Getting type conversions wrong
    is one of the most common sources of bugs in data science code.

  Estimated time: 25 minutes

===============================================================================
"""


# === THE FOUR FUNDAMENTAL TYPES ===============================================
#
# Every piece of data in Python has a TYPE. Think of it like this:
#
#   - A mailbox holds letters (type: string)
#   - A calculator display shows numbers (type: int or float)
#   - A light switch is on or off (type: boolean)
#
# Python has four fundamental types you will use constantly:


# --- INTEGERS (int) ----------------------------------------------------------
# Whole numbers, positive or negative, with no decimal point.
# There is no size limit in Python -- integers can be as large as your
# memory allows.

age = 25
year = 2026
population = 8_000_000_000      # Underscores are allowed for readability
negative = -42
very_large = 10 ** 100          # 1 followed by 100 zeros -- no problem

print(type(age))                # <class 'int'>
print(type(very_large))         # <class 'int'>

# In AI: integers are used for counting (epochs, batch size, number of
# layers), indexing into arrays, and representing categories.


# --- FLOATS (float) ----------------------------------------------------------
# Numbers with a decimal point. Internally stored as 64-bit floating-point
# numbers (this means they have about 15-17 digits of precision).

price = 19.99
pi = 3.14159265
negative_float = -0.5
scientific = 2.5e6              # 2.5 * 10^6 = 2,500,000

print(type(price))              # <class 'float'>
print(type(scientific))         # <class 'float'>

# IMPORTANT: Floating-point arithmetic is not always exact:
print(0.1 + 0.2)               # 0.30000000000000004 (not 0.3!)

# This is NOT a Python bug -- it is how all computers store decimal numbers
# in binary. For most purposes it does not matter. For financial calculations,
# use the decimal module.

# In AI: floats are everywhere -- model weights, learning rates, probabilities,
# loss values, accuracy scores. Almost all neural network computation uses floats.


# --- STRINGS (str) -----------------------------------------------------------
# Text data, enclosed in quotes. Can use single, double, or triple quotes.

greeting = "Hello, World"
name = 'Alice'
paragraph = """This is a
multi-line string that preserves
line breaks."""

empty_string = ""               # A string with nothing in it

print(type(greeting))           # <class 'str'>
print(len(greeting))            # 12 (len() gets the length of the string)
print(len(empty_string))        # 0 (empty string length is 0)

# Strings are IMMUTABLE -- you cannot change a character in place.
# You have to create a new string (we will cover this in lesson 05).

# In AI: strings are the raw input for Natural Language Processing (NLP).
# Every chatbot, translator, and text classifier works with strings.
# Understanding string manipulation is essential for preprocessing text data.


# --- BOOLEANS (bool) ---------------------------------------------------------
# True or False. Only two possible values. Named after mathematician
# George Boole who invented boolean algebra.

is_sunny = True
is_raining = False

print(type(is_sunny))           # <class 'bool'>

# Booleans are created by comparisons:
score = 75
passed = score >= 60
print(passed)                   # True
print(type(passed))             # <class 'bool'>

# You can also check membership:
print("a" in "cat")             # True
print(5 in [1, 2, 3])           # False

# In AI: booleans control training loops ("has the model converged?"),
# filter data ("is this sample valid?"), and represent binary classifications
# ("is this email spam or not?").


# === THE NONE TYPE ============================================================
#
# None represents "nothing" or "no value". It is NOT the same as 0, False,
# or an empty string. It means the absence of any value.

result = None
print(result)                   # None
print(type(result))             # <class 'NoneType'>

# None is commonly used for:
#   - Variables that have not been assigned a real value yet
#   - Functions that do not return anything (they implicitly return None)
#   - Default parameter values (covered in the functions lesson)
#   - Representing missing data

# Check for None using "is", not ==:
if result is None:
    print("No result yet")      # This is the correct way

# In AI: None is used to represent missing data points, uninitialized model
# weights, and optional parameters that were not provided.


# === TYPE CHECKING ============================================================
#
# Use type() to see the type, use isinstance() to check if a value is a
# specific type:

value = 42
print(type(value))                      # <class 'int'>
print(type(value) == int)               # True
print(isinstance(value, int))           # True (preferred way)

# isinstance() can check multiple types at once:
print(isinstance(42, (int, float)))     # True
print(isinstance(3.14, (int, float)))   # True
print(isinstance("hi", (int, float)))   # False


# === TYPE CONVERSION (CASTING) ================================================
#
# You can convert between types using the type name as a function:

# --- String to Number --------------------------------------------------------
age_string = "25"
age_number = int(age_string)
print(age_number + 5)                   # 30 (math works now)

price_string = "19.99"
price_number = float(price_string)
print(price_number * 2)                 # 39.98

# This is critical because input() always returns strings:
# user_input = input("Enter your age: ")  # Returns "25" (a string!)
# age = int(user_input)                   # Now it is a number

# --- Number to String --------------------------------------------------------
count = 42
message = "There are " + str(count) + " items"
print(message)

# Or use f-strings (the modern, preferred way):
message = f"There are {count} items"    # Automatic conversion
print(message)

# --- Number Type Conversions -------------------------------------------------
integer_val = int(3.7)      # 3 (truncates, does NOT round)
float_val = float(42)       # 42.0
rounded_val = round(3.7)    # 4 (rounds properly)

print(integer_val)
print(float_val)
print(rounded_val)

# --- To Boolean ---------------------------------------------------------------
# Everything in Python has a "truthiness" value:
print(bool(0))         # False  -- zero is falsy
print(bool(42))        # True   -- any non-zero number is truthy
print(bool(""))        # False  -- empty string is falsy
print(bool("hello"))   # True   -- non-empty string is truthy
print(bool([]))        # False  -- empty list is falsy
print(bool([1, 2]))    # True   -- non-empty list is truthy
print(bool(None))      # False  -- None is always falsy

# This is why you can write things like:
name = "Alice"
if name:                # Same as: if name is not empty
    print("Name is set")


# === TYPE CONVERSION ERRORS ===================================================
#
# Not all conversions work:

# This will crash:
# int("hello")         # ValueError: invalid literal for int()
# int("3.14")          # ValueError: cannot convert float string directly to int

# To convert "3.14" to an integer, go through float first:
result = int(float("3.14"))     # 3
print(result)


# === DYNAMIC TYPING ===========================================================
#
# Python is DYNAMICALLY TYPED. This means:
# 1. You do not declare the type of a variable in advance
# 2. A variable can hold different types at different times

x = 42          # x is an int
print(type(x))  # <class 'int'>

x = "hello"     # now x is a string
print(type(x))  # <class 'str'>

x = [1, 2, 3]   # now x is a list
print(type(x))  # <class 'list'>

# This flexibility is convenient but can lead to bugs. In large AI projects,
# tools like type hints and mypy are used to catch type errors early:
# def train_model(data: list, epochs: int, lr: float) -> dict:
#     ...


# === REAL-WORLD EXAMPLE: DATA PREPROCESSING ===================================
#
# When you load data from a CSV file or API, values often come in as strings.
# You must convert them to the right type before feeding them to a model.

# Raw data from a CSV (everything is a string):
raw_age = "34"
raw_salary = "75000.50"
raw_employed = "True"

# Cleaned data (proper types):
clean_age = int(raw_age)
clean_salary = float(raw_salary)
clean_employed = raw_employed == "True"    # Convert string "True" to bool True

print(f"Age: {clean_age} (type: {type(clean_age).__name__})")
print(f"Salary: {clean_salary} (type: {type(clean_salary).__name__})")
print(f"Employed: {clean_employed} (type: {type(clean_employed).__name__})")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Confusing int() truncation with rounding
print(int(2.9))      # 2 (NOT 3! int() truncates, use round() to round)
print(round(2.9))    # 3

# MISTAKE 2: Comparing floats directly
print(0.1 + 0.2 == 0.3)    # False! (floating-point precision issue)
# Better: use a small tolerance
print(abs((0.1 + 0.2) - 0.3) < 0.0001)  # True

# MISTAKE 3: Concatenating strings and numbers
# Wrong:
#   print("Score: " + 95)   # TypeError: can only concatenate str to str
# Right:
print("Score: " + str(95))  # Convert number to string first
print(f"Score: {95}")        # Or use f-strings (better)

# MISTAKE 4: Assuming input() returns a number
# user_age = input("Age: ")
# if user_age > 18:          # TypeError! Comparing string to int
#     print("Adult")
# Fix: user_age = int(input("Age: "))


# === EXERCISES ================================================================
#
# Exercise 1: Create one variable of each type (int, float, str, bool).
#             Print each variable and its type.
#
# Exercise 2: The variable price = "49.99" is a string. Convert it to a float,
#             calculate 8% tax, and print the total.
#
# Exercise 3: Predict what bool() returns for each of these, then verify:
#             0, 1, -1, "", "False", [], [0], None
#             (Note: "False" is a non-empty string!)
#
# Exercise 4: Write code that safely converts a string to an integer.
#             If the string is "42", it should work. Think about what
#             happens with "hello" (you will learn try/except later, for
#             now just use an if statement to check if the string is numeric).
#             Hint: "42".isnumeric() returns True


# === SOLUTIONS ================================================================
#
# Exercise 1:
# my_int = 10
# my_float = 3.14
# my_str = "AI"
# my_bool = True
# for var in [my_int, my_float, my_str, my_bool]:
#     print(f"{var} -> {type(var).__name__}")
#
# Exercise 2:
# price = "49.99"
# price_float = float(price)
# tax = price_float * 0.08
# total = price_float + tax
# print(f"Price: {price_float}, Tax: {tax:.2f}, Total: {total:.2f}")
#
# Exercise 3:
# print(bool(0))        # False
# print(bool(1))        # True
# print(bool(-1))       # True (any non-zero number)
# print(bool(""))       # False
# print(bool("False"))  # True (non-empty string!)
# print(bool([]))       # False
# print(bool([0]))      # True (non-empty list, even if contents are falsy)
# print(bool(None))     # False
#
# Exercise 4:
# text = "42"
# if text.lstrip("-").isnumeric():
#     number = int(text)
#     print(f"Converted: {number}")
# else:
#     print(f"Cannot convert '{text}' to integer")


# === KEY TAKEAWAYS ============================================================
#
# - Python has four fundamental types: int, float, str, bool (plus None)
# - Use type() to check a type, isinstance() to test a type
# - Convert between types using int(), float(), str(), bool()
# - Floating-point math is not always exact (0.1 + 0.2 != 0.3)
# - Python is dynamically typed: variables can change type
# - None means "no value" and is checked with "is None"
# - Every value has a truthiness (bool() tells you what it is)


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (04_operators.py), you will learn how to DO things with
# your data: math, comparisons, and logical operations. These are the building
# blocks for every calculation in AI -- from computing loss functions to
# evaluating model accuracy.
