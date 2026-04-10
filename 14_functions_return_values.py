# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 14: Functions -- Return Values
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - The return statement: how functions give back results
    - return vs print: the critical difference
    - Returning multiple values
    - Early returns and guard clauses
    - Functions returning None (implicitly and explicitly)
    - Chaining function calls
    - Building reusable processing pipelines

  Why this matters for AI:
    In AI, every processing step needs to pass its output to the next step.
    load_data() returns data, preprocess() returns cleaned data,
    model.predict() returns predictions, evaluate() returns metrics.
    Without return values, you cannot build pipelines.

  Estimated time: 25 minutes

===============================================================================
"""


# === PRINT vs RETURN: THE CRITICAL DIFFERENCE =================================
#
# This is one of the most important distinctions for beginners to grasp.
#
# print: DISPLAYS a value on the screen for humans to see. The value
#        disappears -- no other code can use it.
#
# return: SENDS a value back to the code that called the function.
#         The value can be stored, used in expressions, or passed to
#         other functions.
#
# Analogy:
#   print() is like shouting the answer across the room. Everyone hears it,
#   but nobody can grab it and use it.
#
#   return is like handing a written note to the person who asked. They
#   receive it and can do whatever they want with it.

# Function that prints (display only):
def add_print(a, b):
    print(a + b)

# Function that returns (gives back a usable value):
def add_return(a, b):
    return a + b

# The difference becomes clear when you try to use the result:
result1 = add_print(5, 3)   # Prints "8" but...
print(f"result1 is: {result1}")  # result1 is None (print returns nothing!)

result2 = add_return(5, 3)  # Returns 8
print(f"result2 is: {result2}")  # result2 is 8 (we can use this!)

# Can we do math with the result?
# total = result1 + 10   # TypeError! None + 10 doesn't work
total = result2 + 10      # Works! 8 + 10 = 18
print(total)


# === THE RETURN STATEMENT =====================================================
#
# When Python hits a return statement, it:
# 1. Evaluates the expression after "return"
# 2. Sends that value back to the caller
# 3. IMMEDIATELY exits the function (any code after return does NOT run)

def double(number):
    return number * 2

result = double(5)
print(result)  # 10

# Direct return (concise style):
def add(a, b):
    return a + b

# Variable then return (explicit style -- better for complex operations):
def calculate_area(width, height):
    area = width * height
    return area

room_area = calculate_area(10, 12)
print(f"Room size: {room_area} sq ft")  # 120 sq ft


# === USING RETURN VALUES =====================================================
#
# Return values can be used anywhere a regular value can be used.

def double(number):
    return number * 2

# Store in a variable:
result = double(5)
print(result)         # 10

# Use in expressions:
total = double(5) + double(3)  # 10 + 6 = 16
print(total)

# Pass to other functions:
print(double(10))     # 20

# Use in conditions:
if double(7) > 10:
    print("Big number!")

# Use in f-strings:
print(f"Doubled: {double(25)}")

# Chain function calls:
result = double(double(double(2)))  # double(2)=4, double(4)=8, double(8)=16
print(result)  # 16


# === RETURNING MULTIPLE VALUES ================================================
#
# Python functions can return multiple values. Under the hood, this returns
# a tuple, which you can unpack into separate variables.

def get_min_max(numbers):
    return min(numbers), max(numbers)

# Unpack into separate variables:
minimum, maximum = get_min_max([5, 2, 8, 1, 9])
print(f"Min: {minimum}, Max: {maximum}")

# Or keep as a tuple:
result = get_min_max([5, 2, 8, 1, 9])
print(result)        # (1, 9)
print(type(result))  # <class 'tuple'>


def get_user_info():
    name = "Prawin"
    location = "Bokaro"
    return name, location

user_name, user_city = get_user_info()
print(f"{user_name} lives in {user_city}")


# More practical example -- statistics:
def calculate_stats(data):
    """Calculate basic statistics for a dataset."""
    n = len(data)
    mean = sum(data) / n
    sorted_data = sorted(data)  # sorted() and sum() were covered in 08_lists.py
    median = sorted_data[n // 2] if n % 2 else (sorted_data[n//2-1] + sorted_data[n//2]) / 2
    data_range = max(data) - min(data)
    return mean, median, data_range

scores = [85, 92, 78, 95, 88, 72, 90]
avg, med, rng = calculate_stats(scores)
print(f"Mean: {avg:.1f}, Median: {med}, Range: {rng}")


# === MULTIPLE RETURN POINTS (EARLY RETURNS) ===================================
#
# A function can have multiple return statements. Only ONE will ever execute
# per function call. This is used for conditional logic.

def check_voting_age(age):
    if age >= 18:
        return "You can vote!"    # Exit point 1
    else:
        return "Too young!"       # Exit point 2

print(check_voting_age(20))  # "You can vote!"
print(check_voting_age(15))  # "Too young!"


# Guard clause pattern (check bad cases first, return early):
def get_legal_summary(case_text):
    if not case_text:
        return "Error: No text provided"   # Guard: exit immediately

    if len(case_text) < 10:
        return "Error: Text too short"      # Guard: exit immediately

    # Main logic only runs if all guards pass:
    summary = f"Summary of: {case_text[:50]}..."
    return summary

print(get_legal_summary(""))
print(get_legal_summary("Short"))
print(get_legal_summary("This is a detailed legal case involving multiple parties."))


# === FUNCTIONS THAT RETURN NONE ===============================================
#
# If a function has no return statement, it implicitly returns None.
# If it has "return" with no value, it also returns None.

def greet(name):
    print(f"Hello, {name}!")
    # No return statement

result = greet("Alice")  # Prints: Hello, Alice!
print(result)            # None

# Explicit None return:
def maybe_process(data):
    if data is None:
        return None              # Explicit return None
    return data.upper()

# This is a common pattern in AI for optional processing steps.


# === RETURNING DIFFERENT TYPES ================================================
#
# Python allows returning different types based on conditions.
# This is flexible but can make code harder to predict.

def divide(a, b):
    if b == 0:
        return None              # Cannot divide by zero
    return a / b

result = divide(10, 3)
if result is not None:
    print(f"Result: {result:.2f}")
else:
    print("Division by zero!")

# In more complex code, returning a dictionary is often cleaner:
def divide_safe(a, b):
    if b == 0:
        return {"success": False, "error": "Division by zero"}
    return {"success": True, "result": a / b}

outcome = divide_safe(10, 0)
if outcome["success"]:
    print(f"Result: {outcome['result']}")
else:
    print(f"Error: {outcome['error']}")


# === BUILDING A PROCESSING PIPELINE ==========================================
#
# The real power of return values: chaining functions together.
# Each function takes input from the previous one's return value.

def load_raw_text(source):
    """Step 1: Load raw text data."""
    # In real code, this would read from a file or API
    return "  Hello, World!  This is RAW data...  "

def clean_text(text):
    """Step 2: Clean the text."""
    text = text.strip()
    text = text.lower()
    text = text.replace("...", "")
    return text

def tokenize(text):
    """Step 3: Split into words."""
    return text.split()

def remove_short_words(words, min_length=3):
    """Step 4: Filter out short words."""
    return [w for w in words if len(w) >= min_length]

def count_words(words):
    """Step 5: Count unique words."""
    from collections import Counter
    return Counter(words)

# The pipeline:
raw = load_raw_text("data/input.txt")
cleaned = clean_text(raw)
tokens = tokenize(cleaned)
filtered = remove_short_words(tokens)
word_counts = count_words(filtered)

print(f"Raw: {raw}")
print(f"Cleaned: {cleaned}")
print(f"Tokens: {tokens}")
print(f"Filtered: {filtered}")
print(f"Counts: {word_counts}")

# Each step is independent, testable, and reusable.
# This is EXACTLY how real AI pipelines are structured.


# === REAL-WORLD EXAMPLE: MODEL EVALUATION =====================================

def calculate_accuracy(predictions, actual):
    """Calculate classification accuracy."""
    correct = sum(1 for p, a in zip(predictions, actual) if p == a)
    return correct / len(actual)

def calculate_precision(predictions, actual, positive_label=1):
    """Calculate precision: of all positive predictions, how many were correct?"""
    true_pos = sum(1 for p, a in zip(predictions, actual) if p == positive_label and a == positive_label)
    pred_pos = sum(1 for p in predictions if p == positive_label)
    if pred_pos == 0:
        return 0.0
    return true_pos / pred_pos

def evaluate_model(predictions, actual):
    """Run full model evaluation and return a report."""
    accuracy = calculate_accuracy(predictions, actual)
    precision = calculate_precision(predictions, actual)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "total_samples": len(actual),
        "correct": sum(1 for p, a in zip(predictions, actual) if p == a)
    }

# Use it:
preds  = [1, 0, 1, 1, 0, 1, 0, 1, 0, 0]
actual = [1, 0, 1, 0, 0, 1, 1, 1, 0, 0]

report = evaluate_model(preds, actual)
print("\n--- Model Evaluation Report ---")
for metric, value in report.items():
    if isinstance(value, float):  # isinstance() was covered in 03_data_types.py
        print(f"  {metric}: {value:.1%}")
    else:
        print(f"  {metric}: {value}")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Forgetting to return (function returns None)
def calculate_total_bad(items):
    total = sum(items)
    # Forgot return!

result = calculate_total_bad([10, 20, 30])
print(result)  # None!

# Right:
def calculate_total_good(items):
    total = sum(items)
    return total

# MISTAKE 2: Code after return (dead code)
def get_status():
    return "Done"
    print("This never prints!")   # Unreachable!

# Right:
def get_status():
    print("Checking status...")   # Do everything before return
    return "Done"

# MISTAKE 3: Using print when you should use return
def multiply_bad(a, b):
    print(a * b)

result = multiply_bad(3, 4)    # Prints 12
# total = result + 10          # TypeError! result is None

# Right:
def multiply_good(a, b):
    return a * b

result = multiply_good(3, 4)   # Returns 12
total = result + 10             # Works! 22


# === EXERCISES ================================================================
#
# Exercise 1: Write a function that takes a list of numbers and returns
#             a dictionary with "sum", "count", "average", "min", and "max".
#
# Exercise 2: Write a function that takes a temperature in Celsius and returns
#             "frozen" (below 0), "cold" (0-15), "warm" (15-25), or "hot" (25+).
#             Use early returns (guard clauses).
#
# Exercise 3: Write a three-function pipeline:
#             a) generate_data() returns a list of 20 random numbers (1-100)
#             b) filter_outliers(data, threshold) removes values above threshold
#             c) summarize(data) returns (mean, min, max) as a tuple
#             Chain them together.
#
# Exercise 4: Write a function that takes a string and returns a dict with:
#             "original", "reversed", "uppercase", "word_count", "char_count"


# === SOLUTIONS ================================================================
#
# Exercise 1:
# def number_stats(numbers):
#     return {
#         "sum": sum(numbers),
#         "count": len(numbers),
#         "average": sum(numbers) / len(numbers),
#         "min": min(numbers),
#         "max": max(numbers)
#     }
# print(number_stats([10, 20, 30, 40, 50]))
#
# Exercise 2:
# def classify_temp(celsius):
#     if celsius < 0:
#         return "frozen"
#     if celsius <= 15:
#         return "cold"
#     if celsius <= 25:
#         return "warm"
#     return "hot"
# for t in [-5, 10, 22, 35]:
#     print(f"{t}C -> {classify_temp(t)}")
#
# Exercise 3:
# import random
# def generate_data():
#     return [random.randint(1, 100) for _ in range(20)]
# def filter_outliers(data, threshold=80):
#     return [x for x in data if x <= threshold]
# def summarize(data):
#     return sum(data)/len(data), min(data), max(data)
# raw = generate_data()
# filtered = filter_outliers(raw)
# avg, lo, hi = summarize(filtered)
# print(f"Mean: {avg:.1f}, Min: {lo}, Max: {hi}")
#
# Exercise 4:
# def analyze_string(text):
#     return {
#         "original": text,
#         "reversed": text[::-1],
#         "uppercase": text.upper(),
#         "word_count": len(text.split()),
#         "char_count": len(text)
#     }
# for k, v in analyze_string("Hello World Python").items():
#     print(f"  {k}: {v}")


# === KEY TAKEAWAYS ============================================================
#
# - return sends a value back to the caller; print just displays it
# - A function without return implicitly returns None
# - Code after return never executes
# - Return multiple values as a tuple: return a, b, c
# - Guard clauses (early returns for invalid input) make code cleaner
# - Chain functions by using one function's return as another's input
# - This chaining pattern is how AI pipelines work
# - Always choose return over print unless you specifically want display-only


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (15_packages_and_modules.py), you will learn how to use
# code that other people have written: Python's standard library and
# third-party packages. This is how you get access to powerful AI tools
# like requests, pandas, and matplotlib without building them yourself.
