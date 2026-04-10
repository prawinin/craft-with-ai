# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 06: If Statements (Control Flow)
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - if, elif, and else statements
    - Combining conditions with and, or, not
    - Nested conditionals
    - Ternary expressions (one-line if)
    - Match statements (Python 3.10+)
    - Best practices for writing clean conditionals

  Why this matters for AI:
    Every AI system makes decisions. A chatbot decides which response to
    give. A spam filter decides if an email is spam. A self-driving car
    decides when to brake. All of these are if-statements at their core --
    checking conditions and choosing actions.

  Estimated time: 25 minutes

===============================================================================
"""


# === BASIC IF STATEMENT =======================================================
#
# The simplest form: do something only IF a condition is true.
#
# Real-world analogy:
#   "If it is raining, take an umbrella."
#   You only take the umbrella when the condition (raining) is true.

age = 18

if age >= 18:
    print("You can vote!")
    print("You are an adult")

# Breaking this down:
#   1. Python evaluates the condition: age >= 18 -> 18 >= 18 -> True
#   2. Because the condition is True, it runs the indented code below
#   3. The colon (:) after the condition is MANDATORY
#   4. The indentation (4 spaces) is MANDATORY -- it defines the code block


# === IF-ELSE ==================================================================
#
# Do one thing if the condition is true, another thing if it is false.
#
# Real-world analogy:
#   "If the store is open, go shopping. Otherwise, go home."

temperature = 25

if temperature > 30:
    print("It's hot!")
else:
    print("Nice weather!")


# === IF-ELIF-ELSE =============================================================
#
# Check multiple conditions in order. Python stops at the FIRST one that is true.
#
# Real-world analogy:
#   "What grade did the student get?"
#   Grade A if 90+, Grade B if 80+, Grade C if 70+, otherwise fail.
#   A student with 85 gets B -- Python stops checking after finding 80+.

score = 85

if score >= 90:
    print("A - Excellent!")
elif score >= 80:
    print("B - Good job!")
elif score >= 70:
    print("C - Keep it up!")
elif score >= 60:
    print("D - Needs improvement")
else:
    print("F - Failed")

# IMPORTANT: The order matters! Python checks conditions from top to bottom
# and runs ONLY the first matching block. Even though score >= 70 is also
# true when score is 85, that block never runs because score >= 80 matched first.


# === COMBINING CONDITIONS =====================================================

age = 25
has_license = True

# AND: Both conditions must be true
if age >= 16 and has_license:
    print("You can drive!")

# OR: At least one condition must be true
import datetime
today = datetime.datetime.now().weekday()  # (imports are covered in 15_packages_and_modules.py)
holiday = False

if today >= 5 or holiday:      # weekday() returns 5 for Saturday, 6 for Sunday
    print("It's a day off!")
else:
    print("Back to work!")

# NOT: Reverse a condition
raining = False
if not raining:
    print("Let's go outside!")

# Complex conditions with parentheses for clarity:
temperature = 22
humidity = 45
if (temperature > 20 and temperature < 30) and (humidity < 60):
    print("Perfect weather for a walk")


# === NESTED IF STATEMENTS =====================================================
#
# You can put if statements inside other if statements. Use this sparingly --
# too much nesting makes code hard to read.

has_ticket = True
age = 15

if has_ticket:
    if age >= 18:
        print("Enjoy the movie!")
    else:
        print("Need adult supervision")
else:
    print("Buy a ticket first")

# Better approach (flatten when possible):
if not has_ticket:
    print("Buy a ticket first")
elif age >= 18:
    print("Enjoy the movie!")
else:
    print("Need adult supervision")


# === TERNARY EXPRESSION (ONE-LINE IF) =========================================
#
# For simple if-else, Python has a compact one-line syntax:
#   value_if_true IF condition ELSE value_if_false

age = 20
status = "adult" if age >= 18 else "minor"
print(status)  # "adult"

# Useful for quick assignments:
score = 85
grade = "Pass" if score >= 60 else "Fail"
print(grade)  # "Pass"

# Do NOT overuse this. If the logic is complex, use a regular if-else.
# Readability matters more than brevity.


# === TRUTHY AND FALSY VALUES ==================================================
#
# In Python, every value has a truthiness. When used in an if statement:
#
# FALSY values (treated as False):
#   - False
#   - None
#   - 0 (zero of any numeric type)
#   - "" (empty string)
#   - [] (empty list)
#   - {} (empty dict)
#   - () (empty tuple)
#   - set() (empty set)
#
# TRUTHY values (treated as True):
#   - Everything else

name = "Alice"
if name:                   # True, because non-empty string
    print(f"Hello, {name}")

items = []
if not items:              # True, because empty list is falsy
    print("Shopping cart is empty")

# This is a common Python idiom. Instead of:
#   if len(items) == 0:
# Write:
#   if not items:


# === MATCH STATEMENT (Python 3.10+) ==========================================
#
# For matching a value against multiple patterns. Similar to switch/case in
# other languages, but more powerful.

command = "start"

match command:
    case "start":
        print("Starting the engine...")
    case "stop":
        print("Stopping the engine...")
    case "pause":
        print("Pausing...")
    case _:                # _ is the wildcard (matches anything else)
        print(f"Unknown command: {command}")

# Match with multiple values:
day = "Saturday"
match day:
    case "Saturday" | "Sunday":
        print("Weekend!")
    case _:
        print("Weekday")


# === REAL-WORLD EXAMPLE: AI RESPONSE ROUTING ==================================
#
# Imagine building an AI assistant that routes user requests:

user_intent = "weather"
user_location = "Paris"
is_authenticated = True

if not is_authenticated:
    response = "Please log in first."
elif user_intent == "weather":
    response = f"Fetching weather data for {user_location}..."
elif user_intent == "news":
    response = "Here are today's top headlines..."
elif user_intent == "email":
    response = "Opening your email inbox..."
elif user_intent == "schedule":
    response = "Checking your calendar..."
else:
    response = "I'm not sure how to help with that. Can you rephrase?"

print(f"AI: {response}")


# === REAL-WORLD EXAMPLE: DATA VALIDATION ======================================

def validate_age(age_input):
    """Validate user age input with clear error messages."""
    if not isinstance(age_input, (int, float)):  # isinstance() was covered in 03_data_types.py
        return "Error: Age must be a number"
    elif age_input < 0:
        return "Error: Age cannot be negative"
    elif age_input > 150:
        return "Error: Age seems unrealistic"
    elif age_input < 18:
        return "You must be 18 or older to sign up"
    else:
        return f"Welcome! You are {int(age_input)} years old"

print(validate_age(25))     # Welcome!
print(validate_age(-5))     # Error: negative
print(validate_age(200))    # Error: unrealistic
print(validate_age(15))     # Must be 18+
print(validate_age("abc"))  # Error: must be a number


# === GUARD CLAUSES (BEST PRACTICE) ============================================
#
# Instead of deeply nested if-else, use "guard clauses" -- check for invalid
# cases first and return early.

# Bad (deeply nested):
def process_order_bad(order):
    if order is not None:
        if order.get("items"):
            if order.get("payment"):
                return "Order processed!"
            else:
                return "No payment info"
        else:
            return "No items in order"
    else:
        return "No order provided"

# Good (guard clauses -- flat and readable):
def process_order_good(order):
    if order is None:
        return "No order provided"
    if not order.get("items"):
        return "No items in order"
    if not order.get("payment"):
        return "No payment info"
    return "Order processed!"


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Missing colon
# Wrong:
#   if x > 5
#       print("Big")
# Right:
x = 10
if x > 5:
    print("Big")

# MISTAKE 2: Using = instead of ==
# Wrong:
#   if x = 5:        # SyntaxError! This is assignment, not comparison
# Right:
if x == 5:
    print("Five")

# MISTAKE 3: Wrong indentation
# Wrong:
#   if True:
#   print("Hello")   # IndentationError!
# Right:
if True:
    print("Hello")

# MISTAKE 4: Checking for True/False explicitly (unnecessary)
is_valid = True
# Unnecessary:
if is_valid == True:
    print("Valid")
# Better:
if is_valid:
    print("Valid")

# MISTAKE 5: Using elif after else
# Wrong (will cause SyntaxError):
#   if x > 10:
#       print("Big")
#   else:
#       print("Small")
#   elif x == 10:          # Too late! else already caught this
#       print("Medium")
# Right:
if x > 10:
    print("Big")
elif x == 10:
    print("Medium")
else:
    print("Small")


# === EXERCISES ================================================================
#
# Exercise 1: Write a program that takes a temperature (in Celsius) and prints:
#             "Freezing" if below 0, "Cold" if 0-15, "Warm" if 15-25,
#             "Hot" if 25-35, "Extreme heat" if above 35.
#
# Exercise 2: Write a simple login checker. Given a username and password,
#             check if username is "admin" and password is "secret123".
#             Print appropriate messages for wrong username, wrong password,
#             or successful login.
#
# Exercise 3: Write a program that classifies a year as a leap year or not.
#             Rules: divisible by 4, BUT not by 100, UNLESS also by 400.
#             Examples: 2024 is leap, 1900 is not, 2000 is leap.
#
# Exercise 4: Convert this nested if-else into guard clauses:
#             def check_password(password):
#                 if password is not None:
#                     if len(password) >= 8:
#                         if any(c.isdigit() for c in password): # any() checks if at least one item is True
#                             return "Strong password"
#                         else:
#                             return "Need a digit"
#                     else:
#                         return "Too short"
#                 else:
#                     return "No password"
#
# Exercise 5: Write an AI confidence classifier. Given a confidence score
#             (0.0 to 1.0), print:
#             - "High confidence" if >= 0.9
#             - "Medium confidence" if >= 0.7
#             - "Low confidence" if >= 0.5
#             - "Very uncertain -- needs human review" if < 0.5


# === SOLUTIONS ================================================================
#
# Exercise 1:
# temp = 22
# if temp < 0:
#     print("Freezing")
# elif temp <= 15:
#     print("Cold")
# elif temp <= 25:
#     print("Warm")
# elif temp <= 35:
#     print("Hot")
# else:
#     print("Extreme heat")
#
# Exercise 2:
# username = "admin"
# password = "secret123"
# if username != "admin":
#     print("Unknown user")
# elif password != "secret123":
#     print("Wrong password")
# else:
#     print("Login successful!")
#
# Exercise 3:
# year = 2024
# if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
#     print(f"{year} is a leap year")
# else:
#     print(f"{year} is not a leap year")
#
# Exercise 4:
# def check_password(password):
#     if password is None:
#         return "No password"
#     if len(password) < 8:
#         return "Too short"
#     if not any(c.isdigit() for c in password):
#         return "Need a digit"
#     return "Strong password"
#
# Exercise 5:
# confidence = 0.85
# if confidence >= 0.9:
#     print("High confidence")
# elif confidence >= 0.7:
#     print("Medium confidence")
# elif confidence >= 0.5:
#     print("Low confidence")
# else:
#     print("Very uncertain -- needs human review")


# === KEY TAKEAWAYS ============================================================
#
# - if checks a condition, elif checks additional conditions, else is the fallback
# - Conditions are checked in order; only the first matching block runs
# - Use and/or/not to combine conditions
# - Ternary expressions (x if cond else y) are good for simple cases
# - Every Python value is either truthy or falsy
# - Guard clauses (check bad cases first, return early) are cleaner than nesting
# - match/case (Python 3.10+) is cleaner than long elif chains for value matching
# - Always use == for comparison, = for assignment


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (07_loops.py), you will learn how to repeat actions.
# Loops are what let AI models train on thousands of data points, process
# every word in a document, or retry failed API calls.
