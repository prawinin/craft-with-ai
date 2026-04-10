# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 10: Tuples
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - What tuples are and how they differ from lists
    - Creating tuples and accessing elements
    - Tuple unpacking (one of Python's most useful features)
    - When and why to use tuples instead of lists
    - Named tuples for self-documenting code

  Why this matters for AI:
    Tuples appear everywhere in AI code, often without you noticing.
    The shape of a NumPy array is a tuple: (100, 784). Function return
    values with multiple outputs use tuples. Dictionary .items() returns
    tuples. Image dimensions are tuples: (height, width, channels).
    Understanding tuples helps you read and write AI code fluently.

  Estimated time: 20 minutes

===============================================================================
"""


# === WHAT IS A TUPLE? =========================================================
#
# A tuple is an IMMUTABLE ordered collection. It is like a list that you
# cannot change after creating it. No adding, removing, or modifying items.
#
# Real-world analogy:
#   A list is a whiteboard (you can erase and rewrite).
#   A tuple is a printed certificate (permanent once created).
#
# Use tuples when:
#   - Data should not change (coordinates, dates, RGB colors)
#   - You want to use it as a dictionary key (lists can not be keys)
#   - Returning multiple values from a function
#   - Slightly more memory-efficient than lists


# === CREATING TUPLES =========================================================

# With parentheses:
point = (3, 5)
colors = ("red", "green", "blue")
empty = ()

# Without parentheses (implicit tuple):
coordinates = 10, 20
print(type(coordinates))   # <class 'tuple'>

# GOTCHA: Single-item tuple needs a trailing comma!
single = (42,)       # This IS a tuple
not_tuple = (42)     # This is just the number 42 in parentheses

print(type(single))     # <class 'tuple'>
print(type(not_tuple))  # <class 'int'>

# From other sequences:
from_list = tuple([1, 2, 3])
from_string = tuple("hello")
from_range = tuple(range(5))
print(from_list)     # (1, 2, 3)
print(from_string)   # ('h', 'e', 'l', 'l', 'o')
print(from_range)    # (0, 1, 2, 3, 4)


# === ACCESSING ELEMENTS ======================================================
#
# Indexing and slicing work exactly like lists.

point = (3, 5, 7)
colors = ("red", "green", "blue", "yellow")

print(point[0])       # 3
print(point[-1])      # 7
print(colors[1:3])    # ('green', 'blue')
print(colors[::-1])   # ('yellow', 'blue', 'green', 'red')

# Length, count, and index:
print(len(colors))           # 4
print(colors.count("red"))   # 1
print(colors.index("blue"))  # 2

# Check membership:
print("green" in colors)     # True


# === TUPLES ARE IMMUTABLE ====================================================

point = (3, 5)

# You CANNOT modify a tuple:
# point[0] = 4           # TypeError: 'tuple' object does not support item assignment
# point.append(7)        # AttributeError: 'tuple' object has no attribute 'append'

# If you need to change it, create a new tuple:
point = (4, point[1])
print(point)  # (4, 5)

# Or convert to list, modify, convert back:
temp = list(point)
temp[0] = 10
point = tuple(temp)
print(point)  # (10, 5)


# === TUPLE UNPACKING ==========================================================
#
# This is one of Python's most elegant features. You can assign each element
# of a tuple to a separate variable in one line.

point = (3, 5)
x, y = point          # x = 3, y = 5
print(f"x={x}, y={y}")

# Works with any number of values:
name, age, city = ("Alice", 30, "NYC")
print(f"{name}, {age}, {city}")

# Multiple assignment (same thing, parentheses optional):
a, b, c = 1, 2, 3

# Swap variables (uses tuple unpacking behind the scenes):
x, y = 10, 20
x, y = y, x
print(f"x={x}, y={y}")  # x=20, y=10

# Ignore some values with underscore:
name, _, city = ("Alice", 30, "NYC")  # We don't need age
print(f"{name} from {city}")

# Collect remaining items with *:
first, *rest = (1, 2, 3, 4, 5)
print(first)   # 1
print(rest)    # [2, 3, 4, 5] (note: rest is a list, not tuple)

first, *middle, last = (1, 2, 3, 4, 5)
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5


# === TUPLES IN FUNCTIONS =====================================================
#
# When a function returns multiple values, Python actually returns a tuple.

def get_user_info():
    name = "Alice"
    age = 30
    city = "NYC"
    return name, age, city    # Returns a tuple: ("Alice", 30, "NYC")

# Unpack the return value:
user_name, user_age, user_city = get_user_info()
print(f"{user_name}, {user_age}, from {user_city}")

# Or keep it as a tuple:
result = get_user_info()
print(result)           # ('Alice', 30, 'NYC')
print(type(result))     # <class 'tuple'>


def get_min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([5, 2, 8, 1, 9])
print(f"Min: {minimum}, Max: {maximum}")


# === TUPLES AS DICTIONARY KEYS ================================================
#
# Since tuples are immutable, they can be used as dictionary keys.
# Lists cannot (they are mutable).

# Mapping coordinates to city names:
locations = {
    (48.85, 2.35): "Paris",
    (51.50, -0.12): "London",
    (35.68, 139.69): "Tokyo"
}

print(locations[(48.85, 2.35)])  # "Paris"

# Mapping (row, col) to values in a sparse matrix:
sparse_matrix = {
    (0, 0): 5,
    (1, 3): 8,
    (2, 1): 3
}


# === TUPLE vs LIST: WHEN TO USE WHICH =========================================
#
# Use a TUPLE when:
#   - Data is fixed and should not change (coordinates, RGB, config)
#   - You need a hashable type (dictionary key, set member)
#   - Returning multiple values from a function
#   - The "shape" of data matters (a 2D point is always exactly 2 values)
#
# Use a LIST when:
#   - Data will change (adding, removing, updating)
#   - The number of items is variable
#   - You need methods like sort(), append(), etc.
#
# Rule of thumb:
#   List = collection of SIMILAR things (a list of names, a list of scores)
#   Tuple = collection of DIFFERENT things grouped together (name, age, city)

# Lists: collections of the same kind of thing
student_names = ["Alice", "Bob", "Charlie"]
test_scores = [92, 85, 78]

# Tuples: structure has meaning -- position determines what the data IS
student_record = ("Alice", 20, "Engineering", 3.8)  # (name, age, major, gpa)
rgb_color = (255, 128, 0)                            # (red, green, blue)
image_shape = (224, 224, 3)                           # (height, width, channels)


# === NAMED TUPLES ============================================================
#
# Regular tuples use numeric indices. Named tuples let you access fields
# by name, making code much more readable.

from collections import namedtuple

# Define a named tuple type:
Point = namedtuple("Point", ["x", "y"])
Student = namedtuple("Student", ["name", "age", "grade"])

# Create instances:
p = Point(3, 5)
s = Student("Alice", 20, "A")

# Access by name OR index:
print(p.x, p.y)          # 3 5
print(p[0], p[1])        # 3 5
print(s.name, s.grade)   # Alice A

# Still immutable (like regular tuples):
# p.x = 10               # AttributeError

# Create a new one with a modified value:
p2 = p._replace(x=10)
print(p2)                # Point(x=10, y=5)

# In AI, named tuples are great for storing model results:
ModelResult = namedtuple("ModelResult", ["prediction", "confidence", "model_name"])
result = ModelResult(prediction="cat", confidence=0.95, model_name="ResNet50")
print(f"{result.model_name}: {result.prediction} ({result.confidence:.0%})")


# === REAL-WORLD EXAMPLE: IMAGE PROCESSING =====================================

# In computer vision, image dimensions are always tuples:
image_shape = (224, 224, 3)  # height x width x channels (RGB)
height, width, channels = image_shape

print(f"Image: {width}x{height} pixels, {channels} color channels")
print(f"Total pixels: {width * height:,}")
print(f"Total values: {width * height * channels:,}")

# Batch of images:
batch_shape = (32, 224, 224, 3)  # (batch_size, height, width, channels)
batch_size, h, w, c = batch_shape
print(f"Batch: {batch_size} images of {w}x{h}")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Forgetting the comma for single-item tuples
single = (42)       # Just the number 42, NOT a tuple
single = (42,)      # THIS is a tuple with one element
single = 42,        # Also a tuple (comma is what matters, not parentheses)

# MISTAKE 2: Trying to modify a tuple
point = (3, 5)
# point[0] = 4      # TypeError!
# SOLUTION: create a new tuple
point = (4, point[1])

# MISTAKE 3: Unpacking wrong number of values
data = (1, 2, 3)
# a, b = data       # ValueError: too many values to unpack
a, b, c = data      # Correct: match the count


# === EXERCISES ================================================================
#
# Exercise 1: Create a tuple with your (latitude, longitude). Use unpacking
#             to assign each to a separate variable and print them.
#
# Exercise 2: Write a function that takes a list of numbers and returns
#             a tuple of (minimum, maximum, average).
#
# Exercise 3: Create a named tuple called "Book" with fields:
#             title, author, year, rating. Create 3 books and find
#             the highest-rated one.
#
# Exercise 4: Given a list of (x, y) coordinate tuples, find the point
#             closest to the origin (0, 0).
#             points = [(3, 4), (1, 1), (5, 2), (2, 3)]
#             Hint: distance = (x**2 + y**2) ** 0.5


# === SOLUTIONS ================================================================
#
# Exercise 1:
# location = (23.79, 86.43)
# lat, lon = location
# print(f"Latitude: {lat}, Longitude: {lon}")
#
# Exercise 2:
# def stats(numbers):
#     return min(numbers), max(numbers), sum(numbers) / len(numbers)
# lo, hi, avg = stats([10, 20, 30, 40, 50])
# print(f"Min: {lo}, Max: {hi}, Avg: {avg}")
#
# Exercise 3:
# from collections import namedtuple
# Book = namedtuple("Book", ["title", "author", "year", "rating"])
# books = [
#     Book("Deep Learning", "Goodfellow", 2016, 4.5),
#     Book("Python Crash Course", "Matthes", 2019, 4.7),
#     Book("AIML", "Mitchell", 1997, 4.2),
# ]
# best = max(books, key=lambda b: b.rating)  # lambdas are covered in 12_functions_basics.py
# print(f"Best: {best.title} ({best.rating})")
#
# Exercise 4:
# points = [(3, 4), (1, 1), (5, 2), (2, 3)]
# closest = min(points, key=lambda p: (p[0]**2 + p[1]**2) ** 0.5)
# print(f"Closest to origin: {closest}")


# === KEY TAKEAWAYS ============================================================
#
# - Tuples are immutable ordered collections using parentheses ()
# - Single-item tuples need a trailing comma: (42,)
# - Unpacking: a, b, c = (1, 2, 3) assigns each value
# - Functions returning multiple values return tuples
# - Tuples can be dictionary keys (lists cannot)
# - Use tuples for fixed structures; lists for variable collections
# - Named tuples add readability by letting you access fields by name
# - AI uses tuples for: shapes, coordinates, return values, configs


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (11_sets.py), you will learn about sets -- the data
# structure for working with unique values and performing mathematical set
# operations like union, intersection, and difference.
