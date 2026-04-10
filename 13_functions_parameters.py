# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 13: Functions -- Parameters
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - Positional and keyword arguments
    - Default parameter values
    - The mutable default argument trap
    - *args and **kwargs (flexible argument patterns)
    - Type hints (optional but recommended)

  Why this matters for AI:
    AI functions often have many configurable options: learning rate, batch
    size, number of epochs, model architecture, loss function. Default
    parameters let you set sensible defaults while allowing users to
    override them. *args and **kwargs let you build flexible APIs that
    can accept varied inputs -- just like real ML frameworks do.

  Estimated time: 25 minutes

===============================================================================
"""


# === PARAMETERS vs ARGUMENTS =================================================
#
# - PARAMETER: the variable name in the function definition
# - ARGUMENT: the actual value you pass when calling the function
#
# Think of parameters as empty boxes with labels.
# Arguments are the things you put in the boxes.

def greet(name):          # "name" is the PARAMETER
    print(f"Hello, {name}!")

greet("Alice")            # "Alice" is the ARGUMENT
greet("Bob")              # "Bob" is the ARGUMENT


# === POSITIONAL ARGUMENTS =====================================================
#
# The simplest form: arguments are matched to parameters by position.
# The first argument goes to the first parameter, and so on.

def introduce(name, age):
    print(f"My name is {name}")
    print(f"I am {age} years old")

introduce("Alice", 25)    # name="Alice", age=25
introduce(25, "Alice")    # name=25, age="Alice" -- WRONG order, no error!
                          # Python does not check if the types make sense.

# With more parameters:
def calculate_total(price, tax_rate, discount):
    tax = price * tax_rate
    final = price + tax - discount
    print(f"Total: ${final:.2f}")

calculate_total(100, 0.08, 10)  # price=100, tax_rate=0.08, discount=10


# === KEYWORD ARGUMENTS ========================================================
#
# You can pass arguments by name. This makes the code self-documenting
# and lets you pass arguments in any order.

def create_profile(name, age, city):
    print(f"{name}, {age}, from {city}")

# Positional (order matters):
create_profile("Alice", 25, "NYC")

# Keyword (order does not matter):
create_profile(city="NYC", age=25, name="Alice")
create_profile(name="Bob", city="LA", age=30)

# Mix positional and keyword (positional must come first):
create_profile("Charlie", city="London", age=28)

# In AI, keyword arguments make function calls readable:
# model.compile(optimizer="adam", loss="crossentropy", metrics=["accuracy"])


# === DEFAULT PARAMETER VALUES =================================================
#
# You can give parameters default values. If the caller does not provide
# an argument, the default is used.
#
# Rule: Parameters WITHOUT defaults must come BEFORE parameters WITH defaults.

def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")                # Uses default: "Hello, Alice!"
greet("Bob", "Hi")            # Overrides: "Hi, Bob!"
greet("Charlie", "Hey")       # Overrides: "Hey, Charlie!"

# A more practical example:
def train_model(data, epochs=10, learning_rate=0.001, verbose=True):
    """Train a model with configurable hyperparameters."""
    if verbose:
        print(f"Training for {epochs} epochs with lr={learning_rate}")
    # ... training logic would go here ...
    return {"accuracy": 0.95}

# Call with all defaults:
train_model([1, 2, 3])

# Override just what you need:
train_model([1, 2, 3], epochs=50)
train_model([1, 2, 3], learning_rate=0.01, verbose=False)
train_model([1, 2, 3], epochs=100, learning_rate=0.0001)


# === THE MUTABLE DEFAULT ARGUMENT TRAP =======================================
#
# This is one of the most notorious gotchas in Python. NEVER use a mutable
# object (list, dict, set) as a default parameter value.
#
# The reason: default values are evaluated ONCE when the function is defined,
# not each time it is called. A mutable default is shared across all calls.

# WRONG -- the same list is reused across calls:
def add_item_bad(item, my_list=[]):
    my_list.append(item)
    return my_list

print(add_item_bad("Apple"))     # ['Apple']
print(add_item_bad("Banana"))    # ['Apple', 'Banana'] -- Wait, where did Apple come from?!

# RIGHT -- use None and create a new list inside:
def add_item_good(item, my_list=None):
    if my_list is None:
        my_list = []      # A BRAND NEW list is created each time
    my_list.append(item)
    return my_list

print(add_item_good("Apple"))    # ['Apple']
print(add_item_good("Banana"))   # ['Banana'] -- Fresh list each time

# The "if None" pattern works because:
# - When the user does NOT provide a list: my_list is None, so we create []
# - When the user DOES provide a list: my_list is their list, so we use it
#
# Real-world analogy:
#   The None is a "Vacant" sign on a hotel room. The if-statement is the
#   maid who sees "Vacant" and prepares a fresh room for the new guest.
#   If a guest already booked (provided their own list), the maid does not
#   reset their room.


# === *args: VARIABLE NUMBER OF POSITIONAL ARGUMENTS ==========================
#
# Sometimes you do not know how many arguments will be passed.
# *args collects any extra positional arguments into a tuple.

def add_all(*numbers):
    """Add any number of values together."""
    total = 0
    for num in numbers:
        total += num
    return total

print(add_all(1, 2))              # 3
print(add_all(1, 2, 3, 4, 5))    # 15
print(add_all(10))                # 10
print(add_all())                  # 0

# Mix regular parameters with *args:
def greet_all(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")

greet_all("Hello", "Alice", "Bob", "Charlie")
# Hello, Alice!
# Hello, Bob!
# Hello, Charlie!


# === **kwargs: VARIABLE NUMBER OF KEYWORD ARGUMENTS ===========================
#
# **kwargs collects any extra keyword arguments into a dictionary.

def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="NYC")
# name: Alice
# age: 30
# city: NYC

# This is how many AI frameworks accept configuration:
def create_model(model_type, **config):
    """Create a model with flexible configuration."""
    print(f"Creating {model_type} model with config:")
    for param, value in config.items():
        print(f"  {param} = {value}")

create_model("transformer",
    hidden_size=768,
    num_layers=12,
    num_heads=12,
    dropout=0.1
)


# === COMBINING EVERYTHING ====================================================
#
# The order of parameters must be:
# 1. Regular positional parameters
# 2. *args
# 3. Keyword-only parameters (after *args or a bare *)
# 4. **kwargs

def full_example(required, default=10, *args, keyword_only=True, **kwargs):
    print(f"required: {required}")
    print(f"default: {default}")
    print(f"args: {args}")
    print(f"keyword_only: {keyword_only}")
    print(f"kwargs: {kwargs}")

full_example("hello", 20, 1, 2, 3, keyword_only=False, extra="data")


# === UNPACKING ARGUMENTS =====================================================
#
# You can "spread" a list or dict into function arguments using * and **:

def calculate(a, b, c):
    return a + b + c

# Unpack a list:
values = [10, 20, 30]
print(calculate(*values))     # Same as calculate(10, 20, 30)

# Unpack a dictionary:
params = {"a": 10, "b": 20, "c": 30}
print(calculate(**params))    # Same as calculate(a=10, b=20, c=30)

# This is extremely useful for forwarding configuration:
config = {"epochs": 10, "learning_rate": 0.001, "verbose": True}
# train_model(data, **config)  # Spreads the dict as keyword arguments


# === TYPE HINTS ===============================================================
#
# Python is dynamically typed, but you can add TYPE HINTS to document
# what types a function expects and returns. They do not enforce anything
# at runtime, but they help readers and tools like mypy catch bugs.

def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b

def greet_user(name: str, times: int = 1) -> None:
    """Greet a user a specified number of times."""
    for _ in range(times):
        print(f"Hello, {name}!")

# With more complex types:
from typing import Optional

def find_user(user_id: int, database: Optional[dict] = None) -> Optional[str]:
    """Look up a user by ID. Returns None if not found."""
    if database is None:
        database = {}
    return database.get(user_id)

# Type hints are a best practice in professional Python code and especially
# in AI projects where data types are critical.


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Wrong number of arguments
def greet(name, age):
    print(f"Hi {name}, you are {age}")

# Wrong:
#   greet("Alice")                   # TypeError: missing 'age'
#   greet("Alice", 25, "NYC")       # TypeError: too many arguments
# Right:
greet("Alice", 25)

# MISTAKE 2: Mutable default arguments (covered above)
# Wrong:  def func(items=[]):
# Right:  def func(items=None):

# MISTAKE 3: Positional argument after keyword argument
# Wrong:
#   greet(name="Alice", 25)         # SyntaxError!
# Right:
greet("Alice", age=25)              # Positional first, then keyword

# MISTAKE 4: Modifying a passed-in list unintentionally
def process(items):
    items.append("new")    # This modifies the ORIGINAL list!
    return items

original = [1, 2, 3]
processed = process(original)
print(original)  # [1, 2, 3, 'new'] -- Original was changed!
# If you do not want this, copy inside the function:
# items = items.copy()


# === EXERCISES ================================================================
#
# Exercise 1: Write a function that takes a student name and any number of
#             test scores (*args), and prints their name and average score.
#
# Exercise 2: Write a function configure_model that takes model_name as
#             required, and learning_rate, batch_size, and dropout as
#             optional parameters with sensible defaults. Print the config.
#
# Exercise 3: Write a function that takes **kwargs and returns a formatted
#             string like "key1=value1, key2=value2, ...".
#
# Exercise 4: Write a function with type hints that takes a list of floats
#             and returns a dictionary with "mean", "min", and "max".
#
# Exercise 5: Write a function `retry` that takes a function and a number
#             of attempts, and calls the function up to that many times.
#             If the function raises an exception, try again. If it succeeds,
#             return the result.


# === SOLUTIONS ================================================================
#
# Exercise 1:
# def student_average(name, *scores):
#     if scores:
#         avg = sum(scores) / len(scores)
#         print(f"{name}: average score = {avg:.1f}")
#     else:
#         print(f"{name}: no scores recorded")
# student_average("Alice", 85, 92, 78, 90)
#
# Exercise 2:
# def configure_model(model_name, learning_rate=0.001, batch_size=32, dropout=0.1):
#     print(f"Model: {model_name}")
#     print(f"  Learning Rate: {learning_rate}")
#     print(f"  Batch Size: {batch_size}")
#     print(f"  Dropout: {dropout}")
# configure_model("BERT", learning_rate=2e-5, batch_size=16)
#
# Exercise 3:
# def format_params(**kwargs):
#     return ", ".join(f"{k}={v}" for k, v in kwargs.items())
# print(format_params(lr=0.001, epochs=10, model="gpt4"))
#
# Exercise 4:
# def list_stats(numbers: list[float]) -> dict[str, float]:
#     return {
#         "mean": sum(numbers) / len(numbers),
#         "min": min(numbers),
#         "max": max(numbers)
#     }
# print(list_stats([10.5, 20.3, 15.7, 8.2, 25.1]))
#
# Exercise 5:
# def retry(func, attempts=3):
#     for i in range(attempts):
#         try:
#             return func()
#         except Exception as e:
#             print(f"Attempt {i+1} failed: {e}")
#     print("All attempts failed")
#     return None


# === KEY TAKEAWAYS ============================================================
#
# - Parameters are in the definition; arguments are in the call
# - Positional arguments match by order; keyword arguments match by name
# - Default values make parameters optional (use None for mutable defaults!)
# - *args collects extra positional arguments into a tuple
# - **kwargs collects extra keyword arguments into a dictionary
# - Type hints document expected types but do not enforce them
# - Unpack lists with * and dicts with ** when calling functions
# - Order: regular, *args, keyword-only, **kwargs


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (14_functions_return_values.py), you will learn how
# functions give back results with the return statement -- the mechanism
# that lets you chain functions together and build complex pipelines.
