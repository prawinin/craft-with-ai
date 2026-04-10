# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 04: Operators
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - Arithmetic operators (+, -, *, /, //, %, **)
    - Comparison operators (==, !=, >, <, >=, <=)
    - Logical operators (and, or, not)
    - Assignment operators (+=, -=, *=, etc.)
    - Operator precedence (what runs first)
    - Bitwise operators (brief introduction)
    - Membership and identity operators

  Why this matters for AI:
    Operators are how you compute everything: loss functions, accuracy scores,
    gradient updates, data filtering. The expression
    "loss = prediction - actual" uses an operator. So does
    "if accuracy > 0.95 and epoch < 100". You will use operators in every
    single line of AI code.

  Estimated time: 25 minutes

===============================================================================
"""


# === ARITHMETIC OPERATORS =====================================================
#
# These work like a calculator, but with some Python-specific behaviors.

# --- Basic math ---------------------------------------------------------------
print(10 + 3)     # 13   Addition
print(10 - 3)     # 7    Subtraction
print(10 * 3)     # 30   Multiplication
print(10 / 3)     # 3.33 Division (ALWAYS returns a float, even 10/2 gives 5.0)

# --- Special operators --------------------------------------------------------
print(10 // 3)    # 3    Floor division (rounds DOWN to nearest integer)
print(10 % 3)     # 1    Modulo (remainder after division)
print(10 ** 3)    # 1000 Exponent (10 raised to the power of 3)

# Real-world uses of each:
# Floor division: determining which page a result is on
#   page = result_number // results_per_page
#
# Modulo: checking if a number is even or odd
#   is_even = number % 2 == 0
#
# Exponent: compound interest, exponential growth, powers of 2
#   compound = principal * (1 + rate) ** years

# --- Division always returns float -------------------------------------------
print(10 / 2)     # 5.0 (not 5)
print(type(10/2)) # <class 'float'>
print(10 // 2)    # 5   (if you want an int, use floor division)

# --- Floor division with negative numbers (a common gotcha) -------------------
print(7 // 2)     #  3  (rounds toward negative infinity)
print(-7 // 2)    # -4  (rounds DOWN, not toward zero!)


# === OPERATOR PRECEDENCE ======================================================
#
# Python follows standard mathematical order of operations (PEMDAS):
# P - Parentheses
# E - Exponents
# M/D - Multiplication / Division (left to right)
# A/S - Addition / Subtraction (left to right)

result = 2 + 3 * 4       # 14 (multiplication first, then addition)
print(result)

result = (2 + 3) * 4     # 20 (parentheses override the default order)
print(result)

# When in doubt, use parentheses. They make code clearer:
# Unclear:
total = base_price + base_price * tax_rate + shipping if 'base_price' in dir() else 0  # dir() gets a list of defined variables
# Clear:
# total = (base_price * (1 + tax_rate)) + shipping

# In AI, parentheses make formulas readable:
# mean_squared_error = sum((prediction - actual) ** 2) / n


# === COMPARISON OPERATORS =====================================================
#
# These compare two values and return True or False (a boolean).
# Think of them as questions you ask Python.

age = 18

print(age == 18)    # True   "Is age equal to 18?"
print(age != 21)    # True   "Is age NOT equal to 21?"
print(age > 17)     # True   "Is age greater than 17?"
print(age < 20)     # True   "Is age less than 20?"
print(age >= 18)    # True   "Is age greater than or equal to 18?"
print(age <= 18)    # True   "Is age less than or equal to 18?"

# CRITICAL DISTINCTION:
#   =  is ASSIGNMENT (puts a value into a variable)
#   == is COMPARISON (asks "are these equal?")
#
# This is the #1 mistake beginners make:
# age = 18     means "set age to 18"
# age == 18    means "is age equal to 18?" (returns True or False)

# You can chain comparisons (Python is special here):
x = 15
print(10 < x < 20)       # True  ("is x between 10 and 20?")
print(1 <= x <= 100)     # True  ("is x between 1 and 100 inclusive?")
# Most other languages require: 10 < x and x < 20

# Comparing strings:
print("apple" < "banana")    # True (alphabetical order)
print("apple" == "Apple")    # False (case-sensitive!)


# === LOGICAL OPERATORS ========================================================
#
# Combine multiple conditions. These are the backbone of decision-making.
#
# and  -- True only if BOTH sides are True
# or   -- True if AT LEAST ONE side is True
# not  -- Reverses True to False, and False to True

age = 25
has_license = True

# AND: both conditions must be true
can_drive = age >= 16 and has_license
print(can_drive)  # True

# OR: at least one condition must be true
day = "Saturday"
is_weekend = day == "Saturday" or day == "Sunday"
print(is_weekend)  # True

# NOT: reverses the condition
is_adult = age >= 18
is_child = not is_adult
print(is_child)  # False

# --- Truth tables (the complete logic) ----------------------------------------
# AND: Both must be True
print(True and True)     # True
print(True and False)    # False
print(False and True)    # False
print(False and False)   # False

# OR: At least one must be True
print(True or True)      # True
print(True or False)     # True
print(False or True)     # True
print(False or False)    # False

# NOT: Flips the value
print(not True)          # False
print(not False)         # True


# --- Short-circuit evaluation -------------------------------------------------
# Python is smart about AND and OR:
#
# AND: if the first value is False, Python does not even check the second.
#      (because False AND anything is always False)
#
# OR:  if the first value is True, Python does not even check the second.
#      (because True OR anything is always True)
#
# This matters when the second expression could cause an error:

my_list = []
# Without short-circuit: this would crash with IndexError
# But Python stops at the first False (empty list is falsy)
if my_list and my_list[0] > 5:
    print("First element is big")
else:
    print("List is empty or first element is small")


# === ASSIGNMENT OPERATORS =====================================================
#
# Shortcuts for updating variables.

score = 100

# Instead of:
score = score + 10    # Long form
# Write:
score += 10           # Short form (same result)
print(score)          # 120

# All assignment operators:
x = 10
x += 5     # x = x + 5   -> 15
x -= 3     # x = x - 3   -> 12
x *= 2     # x = x * 2   -> 24
x /= 4     # x = x / 4   -> 6.0
x //= 2    # x = x // 2  -> 3.0
x **= 3    # x = x ** 3  -> 27.0
x %= 10    # x = x % 10  -> 7.0
print(x)

# In AI, you will see this constantly in training loops:
# total_loss += batch_loss
# epoch += 1
# learning_rate *= decay_factor


# === MEMBERSHIP OPERATORS =====================================================
#
# Check if a value exists inside a collection.

fruits = ["apple", "banana", "orange"]
print("apple" in fruits)       # True
print("grape" in fruits)       # False
print("grape" not in fruits)   # True

# Works with strings too:
message = "Python is powerful"
print("Python" in message)     # True
print("java" in message)       # False

# Works with dictionaries (checks keys, not values):
person = {"name": "Alice", "age": 30}
print("name" in person)        # True
print("Alice" in person)       # False (Alice is a value, not a key)


# === IDENTITY OPERATORS =======================================================
#
# Check if two variables point to the SAME object in memory (not just
# equal values).

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)    # True  (same values)
print(a is b)    # False (different objects in memory)
print(a is c)    # True  (same object -- c points to a's list)

# The most common use: checking for None
result = None
print(result is None)       # True  (correct way)
print(result == None)       # True  (works but considered bad style)


# === STRING OPERATORS =========================================================
#
# The + and * operators work differently with strings:

# Concatenation (joining strings):
full_name = "John" + " " + "Doe"
print(full_name)  # John Doe

# Repetition:
separator = "-" * 40
print(separator)  # ----------------------------------------

stars = "*" * 10
print(stars)      # **********


# === REAL-WORLD EXAMPLE: MODEL EVALUATION =====================================
#
# After training an AI model, you evaluate how well it performs.
# This involves many operators:

predictions = [1, 0, 1, 1, 0, 1, 0, 1, 0, 0]
actual      = [1, 0, 1, 0, 0, 1, 1, 1, 0, 0]

# Count correct predictions
correct = 0
total = len(predictions)                  # len() was covered in 03_data_types.py

for i in range(total):
    if predictions[i] == actual[i]:      # comparison operator
        correct += 1                      # assignment operator

accuracy = correct / total                # arithmetic operator
passed = accuracy >= 0.7                  # comparison operator

print(f"Correct: {correct}/{total}")
print(f"Accuracy: {accuracy:.1%}")        # .1% formats as percentage
print(f"Passed threshold: {passed}")

# (Do not worry about the for loop yet -- we cover that in lesson 07.
# Focus on understanding the operators being used here.)


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Using = instead of ==
x = 5
# Wrong (in an if statement):
#   if x = 5:          # SyntaxError! This assigns, not compares
# Right:
if x == 5:
    print("x is five")

# MISTAKE 2: Confusing "and" with "or"
age = 25
# "Can this person drive?" (must be 16+ AND have a license)
# Wrong:
#   can_drive = age >= 16 or has_license   # Too permissive!
# Right:
#   can_drive = age >= 16 and has_license  # Both must be true

# MISTAKE 3: Integer division vs float division
print(7 / 2)    # 3.5 (float division)
print(7 // 2)   # 3   (floor division -- drops the decimal)

# MISTAKE 4: Operator precedence surprises
print(2 ** 3 ** 2)   # 512 (exponents are right-to-left: 3**2=9, then 2**9=512)
print((2 ** 3) ** 2) # 64  (if you want left-to-right, use parentheses)


# === EXERCISES ================================================================
#
# Exercise 1: Write expressions to calculate:
#             a) The area of a rectangle (width=7, height=4)
#             b) The area of a circle (radius=5, use 3.14159 for pi)
#             c) The volume of a box (length=3, width=4, height=5)
#
# Exercise 2: A store has a "buy 2 get 1 free" deal. Each item costs $15.
#             Using floor division and modulo, calculate the total cost
#             for buying 7 items.
#             Hint: paid_items = total_items - (total_items // 3)
#
# Exercise 3: Write a boolean expression that checks if a number is:
#             a) Between 1 and 100 (inclusive)
#             b) Even AND greater than 50
#             c) Divisible by both 3 and 5
#
# Exercise 4: Predict the output without running, then verify:
#             print(True and False or True)
#             print(not True or True and False)
#             print(10 > 5 and 3 < 1 or 7 == 7)
#
# Exercise 5: Calculate a model's F1 score:
#             Given: precision = 0.85, recall = 0.78
#             F1 = 2 * (precision * recall) / (precision + recall)


# === SOLUTIONS ================================================================
#
# Exercise 1:
# width, height = 7, 4
# print(f"Rectangle area: {width * height}")
# radius = 5
# print(f"Circle area: {3.14159 * radius ** 2}")
# length, width, height = 3, 4, 5
# print(f"Box volume: {length * width * height}")
#
# Exercise 2:
# item_price = 15
# total_items = 7
# free_items = total_items // 3       # 2 free items
# paid_items = total_items - free_items  # 5 paid items
# total_cost = paid_items * item_price   # $75
# print(f"Buying {total_items} items, {free_items} free, cost: ${total_cost}")
#
# Exercise 3:
# number = 75
# print(1 <= number <= 100)
# print(number % 2 == 0 and number > 50)
# print(number % 3 == 0 and number % 5 == 0)
#
# Exercise 4:
# True and False or True   -> (True and False) or True -> False or True -> True
# not True or True and False -> (not True) or (True and False)
#                             -> False or False -> False
# 10 > 5 and 3 < 1 or 7 == 7 -> (True and False) or True -> False or True -> True
#
# Exercise 5:
# precision = 0.85
# recall = 0.78
# f1 = 2 * (precision * recall) / (precision + recall)
# print(f"F1 Score: {f1:.4f}")  # F1 Score: 0.8135


# === KEY TAKEAWAYS ============================================================
#
# - Arithmetic: +, -, *, /, //, %, **
# - Division (/) always returns float; floor division (//) returns int
# - Comparison operators return booleans (True/False)
# - = assigns, == compares
# - Logical operators: and (both), or (either), not (reverse)
# - Short-circuit: Python stops evaluating as soon as the result is known
# - Assignment shortcuts: +=, -=, *=, /=, etc.
# - in checks membership; is checks identity (same object)
# - Use parentheses to make precedence explicit


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (05_string_manipulation.py), you will learn how to work
# with text data in depth: formatting, searching, replacing, and slicing.
# String manipulation is the foundation of all text-based AI work.
