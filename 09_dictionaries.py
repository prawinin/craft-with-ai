# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 09: Dictionaries
  Difficulty: Beginner to Intermediate
===============================================================================

  What you will learn:
    - Creating dictionaries and accessing values
    - Adding, updating, and removing key-value pairs
    - Dictionary methods (get, keys, values, items, update)
    - Looping over dictionaries
    - Nested dictionaries
    - Dictionary comprehensions
    - When to use dictionaries vs lists

  Why this matters for AI:
    Dictionaries are everywhere in AI. API responses are dictionaries (JSON).
    Model configurations are dictionaries. Hyperparameter tuning results
    are stored in dictionaries. Feature engineering often involves mapping
    values through dictionaries. If lists are how you store sequences,
    dictionaries are how you store structured, labeled data.

  Estimated time: 30 minutes

===============================================================================
"""


# === WHAT IS A DICTIONARY? ====================================================
#
# A dictionary stores data as KEY-VALUE pairs. Instead of accessing items by
# position (like lists), you access them by a unique name (the key).
#
# Real-world analogy:
#   A real dictionary maps WORDS (keys) to DEFINITIONS (values).
#   A phone book maps NAMES (keys) to PHONE NUMBERS (values).
#   A student record maps FIELDS (keys) to DATA (values).

# Empty dictionary:
my_dict = {}

# Dictionary with data:
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Alternative creation using dict():
scores = dict(math=95, english=87, science=92)

print(person)
print(scores)


# === ACCESSING VALUES =========================================================

person = {"name": "Alice", "age": 30, "city": "New York"}

# Method 1: Square bracket notation (raises KeyError if key missing)
print(person["name"])       # "Alice"
print(person["age"])        # 30

# Method 2: get() (returns None if key missing -- safer)
print(person.get("name"))          # "Alice"
print(person.get("job"))           # None (no error)
print(person.get("job", "Unknown"))  # "Unknown" (default value)

# When to use each:
# Use [] when you are SURE the key exists (or want an error if it does not)
# Use .get() when the key might be missing and you want a fallback value


# === ADDING AND UPDATING VALUES ===============================================

person = {"name": "Alice", "age": 30}

# Add a new key-value pair:
person["email"] = "alice@email.com"
print(person)  # {'name': 'Alice', 'age': 30, 'email': 'alice@email.com'}

# Update an existing value:
person["age"] = 31
print(person)  # {'name': 'Alice', 'age': 31, 'email': 'alice@email.com'}

# Update multiple values at once:
person.update({"age": 32, "job": "Engineer", "city": "San Francisco"})
print(person)

# The syntax is the same for adding and updating. If the key exists, it
# updates. If it does not exist, it creates.


# === REMOVING VALUES ==========================================================

person = {"name": "Alice", "age": 30, "city": "New York", "email": "a@b.com"}

# Remove by key and get the value:
email = person.pop("email")
print(f"Removed: {email}")
print(person)

# Remove by key (no return value):
del person["city"]
print(person)

# Remove last inserted item:
last = person.popitem()
print(f"Last item: {last}")   # ('age', 30) -- returns a tuple

# Remove all items:
# person.clear()


# === DICTIONARY METHODS =======================================================

person = {"name": "Alice", "age": 30, "city": "New York"}

# Get all keys:
print(person.keys())      # dict_keys(['name', 'age', 'city'])

# Get all values:
print(person.values())    # dict_values(['Alice', 30, 'New York'])

# Get all key-value pairs (as tuples):
print(person.items())     # dict_items([('name', 'Alice'), ('age', 30), ...])

# Check if a key exists:
print("name" in person)   # True
print("Alice" in person)  # False -- checks keys, NOT values
print("email" in person)  # False

# setdefault: get value if key exists, otherwise set a default and return it
person.setdefault("country", "USA")
print(person["country"])   # "USA" (was added because it did not exist)
person.setdefault("name", "Bob")
print(person["name"])      # "Alice" (was NOT changed because it already existed)


# === LOOPING OVER DICTIONARIES ================================================

person = {"name": "Alice", "age": 30, "city": "New York"}

# Loop over keys (default behavior):
print("\n--- Keys ---")
for key in person:
    print(key)

# Loop over values:
print("\n--- Values ---")
for value in person.values():
    print(value)

# Loop over key-value pairs (most common):
print("\n--- Key-Value Pairs ---")
for key, value in person.items():
    print(f"{key}: {value}")


# === NESTED DICTIONARIES ======================================================
#
# Dictionaries can contain other dictionaries. This is how complex,
# structured data is represented.

students = {
    "alice": {"age": 20, "grade": "A", "courses": ["Math", "CS"]},
    "bob": {"age": 21, "grade": "B", "courses": ["English", "History"]},
    "charlie": {"age": 19, "grade": "A", "courses": ["CS", "Physics"]}
}

# Access nested data:
print(students["alice"]["grade"])           # "A"
print(students["bob"]["courses"][0])        # "English"

# Add data to a nested dict:
students["alice"]["email"] = "alice@uni.edu"

# Loop through nested data:
print("\n--- Student Report ---")
for name, info in students.items():
    print(f"{name.title()}: Grade {info['grade']}, Age {info['age']}")


# === DICTIONARY COMPREHENSIONS ================================================
#
# Like list comprehensions, but create dictionaries.
# Syntax: {key_expr: value_expr for variable in iterable if condition}

# Create a dict of squares:
squares = {x: x**2 for x in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Filter a dictionary:
scores = {"alice": 92, "bob": 65, "charlie": 78, "dave": 85}
high_scores = {name: score for name, score in scores.items() if score >= 80}
print(high_scores)  # {'alice': 92, 'dave': 85}

# Swap keys and values:
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(swapped)  # {1: 'a', 2: 'b', 3: 'c'}

# Create from two lists:
keys = ["name", "age", "city"]
values = ["Alice", 30, "NYC"]
combined = dict(zip(keys, values))  # zip() was covered in 07_loops.py
print(combined)  # {'name': 'Alice', 'age': 30, 'city': 'NYC'}


# === DICTIONARY ORDERING =====================================================
#
# Since Python 3.7, dictionaries maintain INSERTION ORDER.
# Items come out in the same order you put them in.

ordered = {}
ordered["first"] = 1
ordered["second"] = 2
ordered["third"] = 3
print(list(ordered.keys()))  # ['first', 'second', 'third'] (always this order)


# === VALID DICTIONARY KEYS ====================================================
#
# Keys must be IMMUTABLE (hashable) types:
#   Allowed: strings, numbers, tuples, booleans, frozensets
#   Not allowed: lists, dicts, sets (they are mutable)

valid_dict = {
    "string_key": 1,
    42: "number key",
    (1, 2): "tuple key",
    True: "bool key"
}

# Wrong:
# bad_dict = {[1, 2]: "value"}     # TypeError: unhashable type: 'list'

# Right (use a tuple instead):
good_dict = {(1, 2): "value"}


# === MERGING DICTIONARIES =====================================================

dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}

# Method 1: update() -- modifies dict1 in place
# dict1.update(dict2)

# Method 2: Unpacking (Python 3.5+) -- creates new dict
merged = {**dict1, **dict2}
print(merged)  # {'a': 1, 'b': 3, 'c': 4}  (dict2's 'b' wins)

# Method 3: Union operator (Python 3.9+)
merged = dict1 | dict2
print(merged)  # {'a': 1, 'b': 3, 'c': 4}


# === COUNTING WITH DICTIONARIES ===============================================
#
# A very common pattern: counting occurrences of items.

# Manual counting:
text = "hello world hello python hello"
word_counts = {}
for word in text.split():
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1
print(word_counts)  # {'hello': 3, 'world': 1, 'python': 1}

# Using get() (cleaner):
word_counts = {}
for word in text.split():
    word_counts[word] = word_counts.get(word, 0) + 1
print(word_counts)

# Using Counter from collections (best way):
from collections import Counter
word_counts = Counter(text.split())
print(word_counts)
print(word_counts.most_common(2))  # [('hello', 3), ('world', 1)]


# === REAL-WORLD EXAMPLE: API RESPONSE PARSING ================================
#
# When you call an AI API, the response is typically a JSON object
# (which Python reads as a dictionary).

api_response = {
    "model": "gpt-4",
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Python is a great language for AI development."
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 15,
        "completion_tokens": 42,
        "total_tokens": 57
    }
}

# Extract the response text:
ai_message = api_response["choices"][0]["message"]["content"]
print(f"AI says: {ai_message}")

# Extract usage information:
tokens_used = api_response["usage"]["total_tokens"]
print(f"Tokens used: {tokens_used}")

# Safely access with get():
model = api_response.get("model", "unknown")
temperature = api_response.get("temperature", "not specified")
print(f"Model: {model}, Temperature: {temperature}")


# === REAL-WORLD EXAMPLE: MODEL CONFIGURATION =================================

# This is how you might configure an AI model:
config = {
    "model_name": "bert-base-uncased",
    "learning_rate": 2e-5,
    "batch_size": 32,
    "num_epochs": 3,
    "max_seq_length": 512,
    "warmup_steps": 100,
    "weight_decay": 0.01,
    "output_dir": "./results",
    "seed": 42
}

# Easy to iterate and print all settings:
print("\n--- Model Configuration ---")
for param, value in config.items():
    print(f"  {param}: {value}")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Accessing a key that does not exist
person = {"name": "Alice"}
# Wrong:
#   print(person["age"])     # KeyError!
# Right:
print(person.get("age", 0))  # Returns 0 if "age" is missing

# MISTAKE 2: Using mutable types as keys
# Wrong:
#   bad = {[1, 2]: "value"}  # TypeError: unhashable type: 'list'
# Right:
good = {(1, 2): "value"}     # Tuples are immutable, so they work

# MISTAKE 3: Modifying dict while iterating
# Wrong:
#   for key in my_dict:
#       if some_condition:
#           del my_dict[key]   # RuntimeError!
# Right:
#   keys_to_delete = [k for k in my_dict if some_condition]
#   for key in keys_to_delete:
#       del my_dict[key]

# MISTAKE 4: Expecting "in" to check values
person = {"name": "Alice"}
print("Alice" in person)      # False -- checks KEYS, not values
print("Alice" in person.values())  # True -- checks values


# === EXERCISES ================================================================
#
# Exercise 1: Create a dictionary representing a book:
#             title, author, year, genres (list), rating (float).
#             Print a formatted summary.
#
# Exercise 2: Given two dictionaries of student scores:
#             midterm = {"alice": 80, "bob": 75, "charlie": 92}
#             final = {"alice": 85, "bob": 82, "charlie": 88}
#             Create a new dict with each student's average score.
#
# Exercise 3: Count the frequency of each character in a string.
#             text = "abracadabra"
#             Expected output: {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}
#
# Exercise 4: Write a function that "inverts" a dictionary (swaps keys
#             and values). Handle the case where values are not unique.
#             Example: {"a": 1, "b": 2, "c": 1} -> {1: ["a", "c"], 2: ["b"]}
#
# Exercise 5: Given a list of dictionaries (simulating a dataset):
#             data = [
#                 {"name": "Alice", "dept": "Engineering", "salary": 95000},
#                 {"name": "Bob", "dept": "Marketing", "salary": 70000},
#                 {"name": "Charlie", "dept": "Engineering", "salary": 88000},
#                 {"name": "Dave", "dept": "Marketing", "salary": 75000},
#             ]
#             Calculate the average salary per department.


# === SOLUTIONS ================================================================
#
# Exercise 1:
# book = {
#     "title": "Deep Learning",
#     "author": "Ian Goodfellow",
#     "year": 2016,
#     "genres": ["AI", "Machine Learning", "Computer Science"],
#     "rating": 4.5
# }
# print(f'"{book["title"]}" by {book["author"]} ({book["year"]})')
# print(f"Rating: {book['rating']}/5")
# print(f"Genres: {', '.join(book['genres'])}")
#
# Exercise 2:
# midterm = {"alice": 80, "bob": 75, "charlie": 92}
# final = {"alice": 85, "bob": 82, "charlie": 88}
# averages = {name: (midterm[name] + final[name]) / 2 for name in midterm}
# print(averages)  # {'alice': 82.5, 'bob': 78.5, 'charlie': 90.0}
#
# Exercise 3:
# text = "abracadabra"
# freq = {}
# for char in text:
#     freq[char] = freq.get(char, 0) + 1
# print(freq)
#
# Exercise 4:
# def invert_dict(d):
#     inverted = {}
#     for key, value in d.items():
#         if value not in inverted:
#             inverted[value] = []
#         inverted[value].append(key)
#     return inverted
# print(invert_dict({"a": 1, "b": 2, "c": 1}))
#
# Exercise 5:
# data = [
#     {"name": "Alice", "dept": "Engineering", "salary": 95000},
#     {"name": "Bob", "dept": "Marketing", "salary": 70000},
#     {"name": "Charlie", "dept": "Engineering", "salary": 88000},
#     {"name": "Dave", "dept": "Marketing", "salary": 75000},
# ]
# dept_salaries = {}
# for emp in data:
#     dept = emp["dept"]
#     dept_salaries.setdefault(dept, []).append(emp["salary"])
# for dept, salaries in dept_salaries.items():
#     avg = sum(salaries) / len(salaries)
#     print(f"{dept}: ${avg:,.0f}")


# === KEY TAKEAWAYS ============================================================
#
# - Dictionaries store key-value pairs in curly braces {}
# - Access with dict[key] or dict.get(key, default)
# - Keys must be immutable (strings, numbers, tuples)
# - Use .items() to loop over key-value pairs
# - Nested dicts represent complex structured data (like JSON/API responses)
# - Dict comprehensions: {k: v for k, v in iterable}
# - Counter from collections is the best way to count things
# - "in" checks keys, not values (use "in dict.values()" for values)


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (10_tuples.py), you will learn about tuples -- the
# immutable cousin of lists. Tuples are used when data should not change,
# like coordinates, database records, and function return values.
