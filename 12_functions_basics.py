# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 12: Functions -- Basics
  Difficulty: Beginner to Intermediate
===============================================================================

  What you will learn:
    - What functions are and why they exist
    - Defining and calling functions
    - The def keyword, naming conventions, and docstrings
    - Variable scope (local vs global)
    - Why global variables are dangerous
    - Functions as first-class objects

  Why this matters for AI:
    Every AI system is built from functions. A function to load data.
    A function to preprocess it. A function to train the model. A function
    to evaluate it. A function to predict on new data. Functions let you
    break a complex AI pipeline into manageable, testable, reusable pieces.

  Estimated time: 30 minutes

===============================================================================
"""


# === WHAT IS A FUNCTION? ======================================================
#
# A function is a NAMED, REUSABLE block of code that performs a specific task.
#
# Real-world analogy:
#   Think of a function like a recipe. It has a name ("Chocolate Cake"),
#   it requires ingredients (parameters), it has steps to follow (the body),
#   and it produces something (the return value). Once you write the recipe,
#   you can follow it as many times as you want without rewriting it.
#
# Why use functions:
#   1. REUSABILITY: Write once, use many times
#   2. ORGANIZATION: Break complex problems into small pieces
#   3. READABILITY: Give names to operations (calculate_tax vs 20 lines of math)
#   4. TESTABILITY: Test each function independently
#   5. MAINTENANCE: Fix a bug in one place, fixed everywhere


# === DEFINING AND CALLING FUNCTIONS ===========================================

# Define a function with the "def" keyword:
def greet():
    print("Hello, World!")
    print("Welcome to Python!")

# Call (invoke) the function by using its name with parentheses:
greet()

# You can call it as many times as you want:
greet()
greet()

# IMPORTANT: Defining a function does NOT run its code.
# The code only runs when you CALL the function.


# === FUNCTION ANATOMY =========================================================
#
#   def function_name():       <- "def" keyword, name, parentheses, colon
#       """Docstring"""        <- Optional documentation (but always write one)
#       # code goes here       <- The function body (indented)
#       return value           <- Optional return statement
#
# Then to use it:
#   result = function_name()   <- Call the function


# === NAMING CONVENTIONS =======================================================
#
# Function names should:
#   - Use snake_case (lowercase with underscores)
#   - Be descriptive verbs (they DO things)
#   - Describe what the function does, not how

# Good names (clear what they do):
def calculate_total():
    pass

def send_email():
    pass

def validate_password():
    pass

def load_training_data():
    pass

def preprocess_text():
    pass

# Bad names:
def func1():               # Not descriptive
    pass

def Calculate():            # Should be lowercase
    pass

def do_stuff():             # Too vague
    pass


# === DOCSTRINGS ==============================================================
#
# A docstring is a string that documents what a function does. It goes
# right after the def line. Python and tools can read it automatically.

def calculate_bmi(weight_kg, height_m):
    """
    Calculate Body Mass Index (BMI).

    Args:
        weight_kg: Weight in kilograms.
        height_m: Height in meters.

    Returns:
        The BMI value as a float.
    """
    return weight_kg / (height_m ** 2)

# Access the docstring with help() or .__doc__:
help(calculate_bmi)
print(calculate_bmi.__doc__)


# === FUNCTIONS WITH LOGIC =====================================================

def check_weather():
    temperature = 25
    if temperature > 30:
        print("It is hot!")
    elif temperature > 20:
        print("Nice weather!")
    else:
        print("It is cold!")

check_weather()


def say_goodbye():
    print("Goodbye!")
    print("See you later!")

# Call it multiple times to see reusability:
say_goodbye()
say_goodbye()
say_goodbye()


# === VARIABLE SCOPE ===========================================================
#
# SCOPE determines where a variable can be accessed. There are two main scopes:
#
# LOCAL scope: Variables created INSIDE a function. They exist only while
# the function is running. They are destroyed when the function ends.
#
# GLOBAL scope: Variables created OUTSIDE any function. They exist for
# the entire program.
#
# Think of it like this:
#   Local variables are like notes written on a classroom whiteboard.
#   When class ends, the board is erased.
#   Global variables are like signs on the building wall.
#   They are visible to everyone and persist all day.

def calculate_price():
    # These are LOCAL variables:
    price = 100
    tax = price * 0.1
    total = price + tax
    print(f"Total: {total}")

calculate_price()  # Total: 110.0

# Trying to access a local variable outside the function:
# print(price)    # NameError: name 'price' is not defined


# === GLOBAL VARIABLES =========================================================
#
# Functions CAN read global variables, but SHOULD NOT modify them.

discount_rate = 0.15      # Global variable

def apply_discount(price):
    discount = price * discount_rate    # Reading global variable (OK)
    return price - discount

result = apply_discount(100)
print(result)  # 85.0


# === WHY GLOBAL VARIABLES ARE DANGEROUS =======================================
#
# You CAN modify global variables with the "global" keyword, but you SHOULD NOT.

counter = 0    # Global

def increment():
    global counter       # Declare we want to modify the global
    counter += 1

increment()
increment()
print(counter)  # 2

# Why is this bad?
#
# 1. HIDDEN SIDE EFFECTS: If you have a project with 50 functions all
#    modifying the same global variable, finding which function broke it
#    becomes a nightmare. Imagine your NyayAI project has a global accuracy
#    value that 10 different functions can modify -- chaos.
#
# 2. HARDER TO TEST: A good function is a "black box" -- give it input,
#    get output, and it does not mess with anything else. Functions that
#    rely on globals are unreliable because they depend on external state.
#
# 3. THREADING ISSUES: In AI applications that process data in parallel,
#    global variables can cause race conditions (two functions trying to
#    modify the same variable at the same time).

# BAD pattern:
total = 0
def add_to_total_bad(amount):
    global total
    total += amount

# GOOD pattern (pure function):
def add_amounts(current_total, amount):
    return current_total + amount

total = 0
total = add_amounts(total, 10)
total = add_amounts(total, 20)
print(total)  # 30


# === FUNCTIONS AS FIRST-CLASS OBJECTS =========================================
#
# In Python, functions are objects -- just like numbers, strings, and lists.
# You can assign them to variables, pass them to other functions, and store
# them in lists.

def square(x):
    return x * x

def cube(x):
    return x * x * x

# Assign a function to a variable:
operation = square
print(operation(5))    # 25

operation = cube
print(operation(5))    # 125

# Store functions in a list:
operations = [square, cube]
for op in operations:
    print(f"{op.__name__}(3) = {op(3)}")

# Pass a function as an argument:
def apply_operation(func, value):
    return func(value)

print(apply_operation(square, 4))  # 16
print(apply_operation(cube, 4))    # 64

# This pattern is used extensively in AI:
# - sorting with key functions: sorted(data, key=len)
# - mapping transformations: map(preprocess, dataset)  # map() applies a function to every item
# - callback functions in training frameworks


# === LAMBDA FUNCTIONS (ANONYMOUS FUNCTIONS) ===================================
#
# A lambda is a tiny, one-line function without a name.
# Syntax: lambda arguments: expression

# Regular function:
def double(x):
    return x * 2

# Same thing as a lambda:
double = lambda x: x * 2
print(double(5))  # 10

# Lambdas are most useful when passed to other functions:
numbers = [3, 1, 4, 1, 5, 9]
sorted_numbers = sorted(numbers, key=lambda x: -x)  # Sort descending
print(sorted_numbers)  # [9, 5, 4, 3, 1, 1]

# Sort strings by last character:
words = ["hello", "world", "python", "code"]
sorted_words = sorted(words, key=lambda w: w[-1])
print(sorted_words)  # ['code', 'world', 'python', 'hello']

# NOTE: If a lambda is more than one line or gets complex, use a regular
# function instead. Readability matters.


# === REAL-WORLD EXAMPLE: AI PIPELINE ==========================================
#
# Here is how functions structure a real AI workflow:

def load_data(filepath):
    """Load data from a file."""
    print(f"Loading data from {filepath}...")
    # In real code: return pd.read_csv(filepath)
    return [{"text": "hello", "label": 1}, {"text": "spam", "label": 0}]

def preprocess(data):
    """Clean and prepare data for the model."""
    print(f"Preprocessing {len(data)} samples...")
    return [{"text": d["text"].lower(), "label": d["label"]} for d in data]

def train_model(data, epochs=10):
    """Train the model on the prepared data."""
    print(f"Training on {len(data)} samples for {epochs} epochs...")
    return {"accuracy": 0.92, "loss": 0.15}

def evaluate(results):
    """Report model performance."""
    print(f"Model accuracy: {results['accuracy']:.1%}")
    print(f"Model loss: {results['loss']:.4f}")

# The pipeline is clean, readable, and each step can be tested independently:
data = load_data("data/train.csv")
processed = preprocess(data)
results = train_model(processed, epochs=5)
evaluate(results)


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Forgetting parentheses when calling
def greet():
    print("Hello!")

# Wrong:
#   greet         # Does nothing! This is just a reference to the function object
# Right:
greet()           # Actually calls the function

# MISTAKE 2: Defining but never calling
def important_calculation():
    return 42 * 365
# If you never call it, the code inside never runs.
result = important_calculation()  # Now it runs

# MISTAKE 3: Using global variables instead of parameters
# Bad:
name = "Alice"
def greet_bad():
    print(f"Hello, {name}")  # Depends on external state

# Good:
def greet_good(name):
    print(f"Hello, {name}")  # Self-contained


# === EXERCISES ================================================================
#
# Exercise 1: Write a function called is_even that takes a number and returns
#             True if it is even, False otherwise.
#
# Exercise 2: Write a function called fahrenheit_to_celsius that converts
#             a temperature from Fahrenheit to Celsius.
#             Formula: C = (F - 32) * 5/9
#             Include a docstring.
#
# Exercise 3: Write a function that takes a list of numbers and returns a
#             new list with only the positive numbers.
#
# Exercise 4: Write a function that takes a string and returns a dictionary
#             with the count of vowels and consonants.
#
# Exercise 5: Refactor this code into functions:
#             words = "hello world python ai"
#             word_list = words.split()
#             upper_words = [w.upper() for w in word_list]
#             result = " | ".join(upper_words)
#             print(result)


# === SOLUTIONS ================================================================
#
# Exercise 1:
# def is_even(number):
#     return number % 2 == 0
# print(is_even(4))   # True
# print(is_even(7))   # False
#
# Exercise 2:
# def fahrenheit_to_celsius(f):
#     """Convert temperature from Fahrenheit to Celsius.
#     Args: f (float): Temperature in Fahrenheit.
#     Returns: float: Temperature in Celsius.
#     """
#     return (f - 32) * 5 / 9
# print(fahrenheit_to_celsius(212))  # 100.0
# print(fahrenheit_to_celsius(32))   # 0.0
#
# Exercise 3:
# def positive_only(numbers):
#     return [n for n in numbers if n > 0]
# print(positive_only([-3, 5, -1, 8, 0, -2, 7]))  # [5, 8, 7]
#
# Exercise 4:
# def count_letters(text):
#     vowels = set("aeiouAEIOU")
#     v_count = sum(1 for c in text if c in vowels)
#     c_count = sum(1 for c in text if c.isalpha() and c not in vowels)
#     return {"vowels": v_count, "consonants": c_count}
# print(count_letters("Hello World"))
#
# Exercise 5:
# def process_words(text, separator=" | "):
#     words = text.split()
#     upper_words = [w.upper() for w in words]
#     return separator.join(upper_words)
# print(process_words("hello world python ai"))


# === KEY TAKEAWAYS ============================================================
#
# - Functions are defined with def, called with ()
# - Name functions with descriptive snake_case verbs
# - Always write docstrings for non-trivial functions
# - Local variables exist only inside the function
# - Avoid modifying global variables -- use parameters and return values
# - Functions are first-class objects (can be passed around like data)
# - Lambda functions are tiny anonymous functions for simple operations
# - Good code is made of small, focused, well-named functions


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (13_functions_parameters.py), you will learn how to make
# functions flexible by accepting parameters -- the inputs that customize
# what a function does each time you call it.
