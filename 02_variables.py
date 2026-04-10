# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 02: Variables and Comments
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - What variables are and why they exist
    - How to create, update, and use variables
    - Naming rules and conventions
    - Multiple assignment and swapping
    - Constants and naming conventions for them
    - How Python manages memory (references)

  Why this matters for AI:
    Every AI program stores data in variables: model parameters, training
    data, user inputs, predictions, accuracy scores. Understanding how
    variables work is understanding how your program holds and moves data.

  Estimated time: 20 minutes

===============================================================================
"""


# === WHAT IS A VARIABLE? =====================================================
#
# A variable is a NAME that refers to a VALUE stored in your computer's memory.
#
# Real-world analogy:
#   Think of a variable like a labeled box. The label is the name, and the
#   thing inside the box is the value. You can look at what is inside using
#   the label, change what is inside, or pass the box to someone else.

age = 22
name = "Prawin"
temperature = 36.6

# What happened:
#   - Python created a space in memory for each value
#   - It attached the name "age" to the value 22
#   - It attached the name "name" to the value "Prawin"
#   - The = sign means "assign this value to this name"
#     (it is NOT the same as "equals" in math -- we use == for that)

print(age)          # 22
print(name)         # Prawin
print(temperature)  # 36.6


# === USING VARIABLES ==========================================================
#
# Once you have a variable, you can use it anywhere you would use the value itself.

birth_year = 2003
current_year = 2026
years_old = current_year - birth_year
print("Age:", years_old)  # Age: 23

# Variables make code readable. Compare:
print(100 * 0.18)                  # What is this? Tax? Tip? Discount?

price = 100
tax_rate = 0.18
tax_amount = price * tax_rate
print("Tax:", tax_amount)          # Much clearer what is happening


# === UPDATING VARIABLES =======================================================
#
# Variables can be changed at any time. The old value is replaced.

score = 0
print("Starting score:", score)    # 0

score = 10
print("After first round:", score) # 10

score = score + 5
print("After bonus:", score)       # 15

# The line "score = score + 5" is read right to left:
#   1. Python evaluates the right side: score + 5 => 15 + 5 => 20... wait,
#      score is 10 at that point, so 10 + 5 = 15
#   2. The result (15) is assigned to score
#   3. The old value (10) is gone


# === NAMING RULES (WHAT PYTHON ALLOWS) =======================================
#
# Python has strict rules for variable names:
#
# 1. Must start with a letter or underscore (_)
# 2. Can contain letters, numbers, and underscores
# 3. Cannot be a Python keyword (like if, for, while, print, etc.)
# 4. Case-sensitive (age, Age, and AGE are three different variables)

# Valid names:
user_name = "Alice"
score2 = 95
_private = "hidden"
firstName = "Bob"

# Invalid names (these would cause errors):
# 2nd_place = "Silver"     # Cannot start with a number
# my-name = "Alice"        # Hyphens are not allowed
# class = "Biology"        # "class" is a Python keyword


# === NAMING CONVENTIONS (WHAT GOOD PROGRAMMERS DO) ============================
#
# Beyond the rules, there are strong conventions the Python community follows:
#
# 1. Use snake_case for variables and functions:
#    user_name, total_score, learning_rate, training_data
#
# 2. Use UPPER_SNAKE_CASE for constants (values that should not change):
#    MAX_RETRIES, API_KEY, DATABASE_URL
#
# 3. Use descriptive names that explain what the variable holds:
#    Good: student_count, average_temperature, model_accuracy
#    Bad:  x, temp, sc, n

# In AI code specifically, you will see conventions like:
# X = training features (capital because it is a matrix)
# y = target labels (lowercase because it is a vector)
# lr = learning rate (common abbreviation everyone knows)
# n_epochs = number of training epochs
# batch_size = number of samples per batch


# === MULTIPLE ASSIGNMENT ======================================================
#
# Python lets you assign multiple variables in one line:

x, y, z = 10, 20, 30
print(x, y, z)  # 10 20 30

# Assign the same value to multiple variables:
a = b = c = 0
print(a, b, c)  # 0 0 0

# Swap two variables (Python makes this elegant):
first = "hello"
second = "world"
first, second = second, first
print(first, second)  # world hello

# In most other languages, swapping requires a temporary variable:
# temp = first
# first = second
# second = temp
# Python's version is cleaner and less error-prone.


# === CONSTANTS ================================================================
#
# Python does not have true constants (values that cannot be changed).
# Instead, the convention is to use ALL_CAPS to signal "do not change this":

MAX_RETRIES = 3
PI = 3.14159
API_BASE_URL = "https://api.openai.com/v1"

# Nothing stops you from changing these, but other programmers (and your
# future self) will understand that they should not be modified.
# In AI projects, constants are used for:
#   - Model hyperparameters
#   - API endpoints
#   - Configuration values


# === HOW PYTHON MANAGES MEMORY ================================================
#
# When you write age = 25, Python does NOT put 25 "inside" the variable.
# Instead:
#   1. Python creates the object 25 somewhere in memory
#   2. The name "age" is a REFERENCE (a pointer) to that object
#
# This distinction matters when you copy variables:

list_a = [1, 2, 3]
list_b = list_a          # list_b points to the SAME list, not a copy
list_b.append(4)
print(list_a)            # [1, 2, 3, 4] -- list_a changed too!

# This is a common source of bugs. We will cover this in depth in the
# lists lesson (08_lists.py), but for now just know: for simple values
# like numbers and strings, this is not a problem.

number_a = 10
number_b = number_a
number_b = 20
print(number_a)  # 10 -- unchanged, because numbers are immutable


# === CHECKING VARIABLE TYPE ===================================================
#
# The type() function tells you what kind of data a variable holds:

age = 25
name = "Alice"
price = 19.99
is_student = True

print(type(age))         # <class 'int'>
print(type(name))        # <class 'str'>
print(type(price))       # <class 'float'>
print(type(is_student))  # <class 'bool'>

# We will explore these types in detail in the next lesson.


# === DELETING VARIABLES =======================================================
#
# You can remove a variable with the del keyword:

temporary = "I will be deleted"
print(temporary)
del temporary
# print(temporary)  # This would cause a NameError


# === REAL-WORLD EXAMPLE: AI MODEL CONFIGURATION ==============================
#
# Here is what variables look like in a real AI project setup:

# Model configuration
model_name = "gpt-4"
max_tokens = 1000
temperature = 0.7          # Controls randomness (0 = deterministic, 1 = creative)
top_p = 0.9                # Controls diversity of responses
system_prompt = "You are a helpful assistant that answers coding questions."

# Training configuration
learning_rate = 0.001
batch_size = 32
n_epochs = 10
dropout_rate = 0.2

# Data paths
training_data_path = "data/train.csv"
model_save_path = "models/best_model.pt"

print(f"Configuring {model_name} with temperature={temperature}")
print(f"Training for {n_epochs} epochs with lr={learning_rate}")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Using a variable before defining it
# Wrong:
#   print(username)     # NameError: name 'username' is not defined
#   username = "Alice"
# Right:
username = "Alice"
print(username)

# MISTAKE 2: Spaces in variable names
# Wrong:
#   my name = "Alice"   # SyntaxError
# Right:
my_name = "Alice"

# MISTAKE 3: Starting with a number
# Wrong:
#   1st_place = "Gold"  # SyntaxError
# Right:
first_place = "Gold"

# MISTAKE 4: Using = when you mean ==
# = assigns a value
# == compares values
x = 5         # assigns 5 to x
print(x == 5) # compares: is x equal to 5? True
print(x == 3) # compares: is x equal to 3? False


# === EXERCISES ================================================================
#
# Exercise 1: Create variables for your first name, last name, and age.
#             Print a sentence using all three.
#
# Exercise 2: Create two number variables. Swap their values without using
#             a temporary variable. Print both before and after swapping.
#
# Exercise 3: Create variables for an AI chatbot configuration:
#             model_name, temperature, max_response_length, and system_role.
#             Print a summary of the configuration.
#
# Exercise 4: Calculate compound interest.
#             Principal = 1000, rate = 5% (0.05), years = 10
#             Formula: principal * (1 + rate) ** years
#             Store the result and print it with a descriptive message.
#
# Exercise 5: What will this print? Predict the answer, then run it.
#             a = 10
#             b = a
#             a = 20
#             print(b)


# === SOLUTIONS ================================================================
#
# Exercise 1:
# first_name = "Prawin"
# last_name = "Kumar"
# age = 25
# print(f"My name is {first_name} {last_name} and I am {age} years old")
#
# Exercise 2:
# x = 42
# y = 99
# print("Before:", x, y)
# x, y = y, x
# print("After:", x, y)
#
# Exercise 3:
# model_name = "gpt-4"
# temperature = 0.7
# max_response_length = 500
# system_role = "coding assistant"
# print(f"Model: {model_name}")
# print(f"Temperature: {temperature}")
# print(f"Max tokens: {max_response_length}")
# print(f"Role: {system_role}")
#
# Exercise 4:
# principal = 1000
# rate = 0.05
# years = 10
# final_amount = principal * (1 + rate) ** years
# print(f"After {years} years, {principal} becomes {final_amount:.2f}")
#
# Exercise 5:
# It prints 10. Because b was assigned the value of a (which was 10).
# When a later changes to 20, b still holds 10. Numbers are immutable.


# === KEY TAKEAWAYS ============================================================
#
# - Variables are names that refer to values in memory
# - Use = to assign, == to compare
# - Follow snake_case naming conventions
# - Use descriptive names that explain the purpose
# - Use ALL_CAPS for constants
# - Python variables are references: be careful with mutable types (lists, dicts)
# - type() tells you what kind of data a variable holds


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (03_data_types.py), you will learn about the different
# types of data Python can handle: numbers (integers and floats), text
# (strings), and true/false values (booleans). Understanding types is
# essential because AI models expect specific data types as input.
