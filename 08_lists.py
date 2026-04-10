# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 08: Lists
  Difficulty: Beginner to Intermediate
===============================================================================

  What you will learn:
    - Creating lists and accessing elements
    - Indexing, slicing, and negative indices
    - Modifying lists (add, remove, update)
    - List methods (sort, reverse, count, index, copy)
    - List comprehensions
    - Nested lists (2D data)
    - Common list patterns in AI

  Why this matters for AI:
    Lists are the backbone of data in Python. A dataset is a list of samples.
    Model predictions come back as a list. Feature vectors are lists of
    numbers. Before you touch NumPy arrays or pandas DataFrames, you need
    to master plain Python lists.

  Estimated time: 30 minutes

===============================================================================
"""


# === CREATING LISTS ===========================================================
#
# A list is an ordered, mutable collection of items. It can hold any type
# of data, and items can be different types within the same list.
#
# Real-world analogy:
#   A list is like a shopping list. Items have an order (first, second, third).
#   You can add items, remove items, or change items. The list can hold
#   different things (bread, milk, 3 apples).

# Empty list:
my_list = []

# List with items:
fruits = ["apple", "banana", "orange"]
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, True, 3.14]       # Different types are fine

# Creating from other sequences:
letters = list("Python")                 # ['P', 'y', 't', 'h', 'o', 'n']
numbers = list(range(1, 6))              # [1, 2, 3, 4, 5]

print(fruits)
print(letters)
print(numbers)


# === ACCESSING ELEMENTS (INDEXING) ============================================
#
# Each item has a position number (index), starting from 0.
#
#   Index:    0        1        2
#   Value: "apple"  "banana"  "orange"
#
#   Negative: -3       -2       -1

fruits = ["apple", "banana", "orange"]

print(fruits[0])     # "apple" (first item)
print(fruits[1])     # "banana" (second item)
print(fruits[-1])    # "orange" (last item)
print(fruits[-2])    # "banana" (second to last)

# Why does indexing start at 0?
# It is about offsets: the first item is 0 positions from the start.
# This is a convention in most programming languages.


# === SLICING ==================================================================
#
# Extract a portion of a list using [start:end] or [start:end:step].
# start is INCLUDED, end is EXCLUDED.

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[2:5])     # [2, 3, 4]
print(numbers[:3])      # [0, 1, 2] (start from beginning)
print(numbers[7:])      # [7, 8, 9] (go to end)
print(numbers[-3:])     # [7, 8, 9] (last 3 items)
print(numbers[::2])     # [0, 2, 4, 6, 8] (every 2nd item)
print(numbers[::-1])    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] (reversed)

# Slicing NEVER raises an IndexError, even if indices are out of range:
print(numbers[5:100])   # [5, 6, 7, 8, 9] (just goes to the end)
print(numbers[100:])    # [] (empty list, no error)


# === MODIFYING LISTS ==========================================================

fruits = ["apple", "banana", "orange"]

# --- Change an item ---
fruits[0] = "mango"
print(fruits)  # ['mango', 'banana', 'orange']

# --- Add items ---
fruits.append("grape")           # Add to end
print(fruits)  # ['mango', 'banana', 'orange', 'grape']

fruits.insert(1, "kiwi")        # Insert at specific position
print(fruits)  # ['mango', 'kiwi', 'banana', 'orange', 'grape']

fruits.extend(["melon", "pear"])  # Add multiple items from another list
print(fruits)

# --- Remove items ---
fruits.remove("banana")         # Remove FIRST occurrence by value
print(fruits)

last = fruits.pop()              # Remove and RETURN last item
print(f"Removed: {last}")

specific = fruits.pop(1)         # Remove and RETURN item at index
print(f"Removed: {specific}")

del fruits[0]                    # Remove by index (no return value)
print(fruits)

# fruits.clear()                 # Remove ALL items (empty the list)


# === LIST METHODS: INFORMATION ================================================

numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]

print(len(numbers))              # 9 (how many items)
print(numbers.count(1))          # 2 (how many times 1 appears)
print(numbers.index(5))          # 4 (position of first 5)
print(min(numbers))              # 1 (built-in function for smallest value)
print(max(numbers))              # 9 (built-in function for largest value)
print(sum(numbers))              # 36 (built-in function for total of all values)

# Check if item exists:
print(5 in numbers)              # True
print(7 in numbers)              # False
print(7 not in numbers)          # True


# === LIST METHODS: SORTING ====================================================

numbers = [3, 1, 4, 1, 5, 9]

# sort() modifies the list IN PLACE (returns None):
numbers.sort()
print(numbers)          # [1, 1, 3, 4, 5, 9]

numbers.sort(reverse=True)
print(numbers)          # [9, 5, 4, 3, 1, 1]

# sorted() returns a NEW list (original unchanged):
original = [3, 1, 4, 1, 5]
sorted_copy = sorted(original)
print(original)         # [3, 1, 4, 1, 5] (unchanged)
print(sorted_copy)      # [1, 1, 3, 4, 5] (new list)

# Sorting strings:
names = ["Charlie", "Alice", "Bob"]
names.sort()
print(names)            # ['Alice', 'Bob', 'Charlie'] (alphabetical)

# Sort by custom criteria (sort by string length):
words = ["python", "ai", "data", "learning"]
words.sort(key=len)
print(words)            # ['ai', 'data', 'python', 'learning']

# reverse() reverses the list in place:
numbers = [1, 2, 3, 4, 5]
numbers.reverse()
print(numbers)          # [5, 4, 3, 2, 1]


# === COPYING LISTS (IMPORTANT!) ===============================================
#
# This is one of the most common sources of bugs in Python.

# WRONG: Both variables point to the same list
list1 = [1, 2, 3]
list2 = list1            # list2 is NOT a copy -- it is the SAME list
list2.append(4)
print(list1)             # [1, 2, 3, 4] -- list1 changed too!

# RIGHT: Make a proper copy
list1 = [1, 2, 3]
list2 = list1.copy()     # Method 1: .copy()
# list2 = list(list1)    # Method 2: list() constructor
# list2 = list1[:]       # Method 3: slice the whole list
list2.append(4)
print(list1)             # [1, 2, 3] -- unchanged
print(list2)             # [1, 2, 3, 4]

# For nested lists, use deepcopy:
import copy  # (Imports are covered in 15_packages_and_modules.py)
nested = [[1, 2], [3, 4]]
shallow = nested.copy()          # Shallow copy: inner lists still shared
deep = copy.deepcopy(nested)     # Deep copy: completely independent


# === LIST COMPREHENSIONS ======================================================
#
# A concise way to create lists. This is one of the most powerful and commonly
# used features in Python.
#
# Syntax: [expression FOR variable IN iterable IF condition]

# Basic: transform each item
squares = [x ** 2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition (filter):
even_numbers = [x for x in range(20) if x % 2 == 0]
print(even_numbers)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Transform and filter:
names = ["alice", "BOB", "Charlie", "dave"]
capitalized = [name.title() for name in names if len(name) > 3]
print(capitalized)  # ['Alice', 'Charlie', 'Dave']

# Equivalent to:
# result = []
# for name in names:
#     if len(name) > 3:
#         result.append(name.title())

# With if-else (note: the if-else goes BEFORE the for):
numbers = [1, 2, 3, 4, 5, 6]
labels = ["even" if x % 2 == 0 else "odd" for x in numbers]
print(labels)  # ['odd', 'even', 'odd', 'even', 'odd', 'even']

# CAUTION: Do not make comprehensions too complex. If you need multiple
# lines of logic, use a regular for loop instead.


# === NESTED LISTS (2D DATA) ===================================================
#
# Lists can contain other lists. This is how you represent 2D data:
# tables, matrices, grids, and images.

# A 3x3 grid (like a tic-tac-toe board):
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Access elements: grid[row][column]
print(grid[0][0])    # 1 (top-left)
print(grid[1][2])    # 6 (middle row, right column)
print(grid[2][1])    # 8 (bottom row, middle column)

# Loop through a 2D list:
for row in grid:
    for value in row:
        print(f"{value:3}", end="")
    print()
# Output:
#   1  2  3
#   4  5  6
#   7  8  9

# In AI, 2D lists represent:
# - A dataset (each inner list is one sample)
# - An image (each inner list is one row of pixels)
# - A matrix of weights in a neural network


# === USEFUL LIST PATTERNS =====================================================

# --- Flatten a 2D list ---
nested = [[1, 2], [3, 4], [5, 6]]
flat = [item for sublist in nested for item in sublist]
print(flat)  # [1, 2, 3, 4, 5, 6]

# --- Create a list of zeros (initialize) ---
zeros = [0] * 10
print(zeros)  # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# --- Find unique values while preserving order ---
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
seen = set()
unique = []
for item in items:
    if item not in seen:
        seen.add(item)
        unique.append(item)
print(unique)  # [3, 1, 4, 5, 9, 2, 6]

# --- Split a list into chunks ---
data = list(range(10))
chunk_size = 3
chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
print(chunks)  # [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

# This pattern is used in AI for creating "batches" of training data.


# === REAL-WORLD EXAMPLE: PROCESSING MODEL PREDICTIONS =========================

# Simulated predictions from a classification model
predictions = [0.92, 0.15, 0.78, 0.03, 0.67, 0.95, 0.44, 0.88, 0.11, 0.73]
threshold = 0.5

# Classify as positive (1) or negative (0)
classes = [1 if p >= threshold else 0 for p in predictions]
print(f"Predictions: {predictions}")
print(f"Classes:     {classes}")

# Count positive and negative
positives = classes.count(1)
negatives = classes.count(0)
print(f"Positive: {positives}, Negative: {negatives}")

# Get the high-confidence predictions
high_conf = [p for p in predictions if p > 0.8]
print(f"High confidence: {high_conf}")

# Find the most confident prediction
max_pred = max(predictions)
max_index = predictions.index(max_pred)
print(f"Most confident: {max_pred} at index {max_index}")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Index out of range
fruits = ["apple", "banana"]
# Wrong:
#   print(fruits[2])     # IndexError! Only indices 0 and 1 exist
# Right: check length first
if len(fruits) > 2:
    print(fruits[2])

# MISTAKE 2: Modifying list during iteration
numbers = [1, 2, 3, 4, 5]
# Wrong:
#   for num in numbers:
#       if num == 3:
#           numbers.remove(num)  # Dangerous!
# Right: use a comprehension
numbers = [n for n in numbers if n != 3]

# MISTAKE 3: Using = instead of .copy()
original = [1, 2, 3]
# Wrong:
#   backup = original    # Same list, not a copy!
# Right:
backup = original.copy()

# MISTAKE 4: Confusing append and extend
a = [1, 2]
a.append([3, 4])     # Adds the list AS ONE ITEM: [1, 2, [3, 4]]
print(a)

b = [1, 2]
b.extend([3, 4])     # Adds each item individually: [1, 2, 3, 4]
print(b)


# === EXERCISES ================================================================
#
# Exercise 1: Given a list of numbers, create a new list containing only
#             the numbers greater than the average.
#             numbers = [23, 45, 12, 67, 34, 89, 11, 56]
#
# Exercise 2: Write code to remove all duplicate values from a list while
#             preserving the original order.
#             items = [4, 2, 7, 2, 4, 1, 7, 9, 1]
#
# Exercise 3: Given two lists of equal length, create a list of their
#             element-wise sums.
#             list_a = [1, 2, 3, 4, 5]
#             list_b = [10, 20, 30, 40, 50]
#             Expected: [11, 22, 33, 44, 55]
#
# Exercise 4: Flatten this nested list: [[1, [2, 3]], [4, 5], [6, [7, 8, [9]]]]
#             into [1, 2, 3, 4, 5, 6, 7, 8, 9]
#             Hint: write a recursive function, or use a while loop that
#             checks if any element is still a list.
#
# Exercise 5: Write a function that splits a list into n roughly equal parts.
#             split_list([1,2,3,4,5,6,7], 3) -> [[1,2,3], [4,5], [6,7]]


# === SOLUTIONS ================================================================
#
# Exercise 1:
# numbers = [23, 45, 12, 67, 34, 89, 11, 56]
# avg = sum(numbers) / len(numbers)
# above_avg = [n for n in numbers if n > avg]
# print(f"Average: {avg:.1f}, Above: {above_avg}")
#
# Exercise 2:
# items = [4, 2, 7, 2, 4, 1, 7, 9, 1]
# seen = set()
# unique = []
# for item in items:
#     if item not in seen:
#         seen.add(item)
#         unique.append(item)
# print(unique)  # [4, 2, 7, 1, 9]
#
# Exercise 3:
# list_a = [1, 2, 3, 4, 5]
# list_b = [10, 20, 30, 40, 50]
# sums = [a + b for a, b in zip(list_a, list_b)]
# print(sums)  # [11, 22, 33, 44, 55]
#
# Exercise 4:
# def flatten(lst):
#     result = []
#     for item in lst:
#         if isinstance(item, list):
#             result.extend(flatten(item))
#         else:
#             result.append(item)
#     return result
# print(flatten([[1, [2, 3]], [4, 5], [6, [7, 8, [9]]]]))
#
# Exercise 5:
# def split_list(lst, n):
#     k, remainder = divmod(len(lst), n)  # divmod() returns (quotient, remainder)
#     result = []
#     start = 0
#     for i in range(n):
#         size = k + (1 if i < remainder else 0)
#         result.append(lst[start:start + size])
#         start += size
#     return result
# print(split_list([1,2,3,4,5,6,7], 3))


# === KEY TAKEAWAYS ============================================================
#
# - Lists are ordered, mutable collections (square brackets [])
# - Indexing starts at 0; negative indices count from the end
# - Slicing: list[start:end:step] (end is excluded)
# - append() adds one item; extend() adds multiple; insert() adds at a position
# - remove() deletes by value; pop() by index; del by index
# - sort() modifies in place; sorted() returns a new list
# - Copy with .copy(), not =
# - List comprehensions: [expr for var in iterable if condition]
# - Nested lists represent 2D data (tables, matrices, images)


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (09_dictionaries.py), you will learn about dictionaries --
# Python's key-value data structure. While lists store items by position,
# dictionaries store items by name. This is how you represent structured data
# like JSON responses from APIs, model configurations, and database records.
