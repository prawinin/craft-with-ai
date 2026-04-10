# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 11: Sets
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - What sets are and how they differ from lists
    - Creating sets and adding/removing elements
    - Set operations: union, intersection, difference, symmetric difference
    - Practical uses of sets (deduplication, membership testing, comparisons)
    - Frozen sets

  Why this matters for AI:
    Sets are used for deduplication (removing duplicate data points),
    vocabulary building in NLP (collecting unique words), feature selection
    (finding common features between datasets), and efficient membership
    testing. When you need to check "is this item in my collection?",
    sets are orders of magnitude faster than lists.

  Estimated time: 20 minutes

===============================================================================
"""


# === WHAT IS A SET? ===========================================================
#
# A set is an UNORDERED collection of UNIQUE items. No duplicates allowed.
# No guaranteed order.
#
# Real-world analogy:
#   A set of playing cards. Each card appears only once. You do not care
#   about the order they are in -- you care about WHICH cards you have.
#
# Key properties:
#   - Items are unique (duplicates are automatically removed)
#   - Items are unordered (no indexing, no slicing)
#   - Very fast membership testing (O(1) on average vs O(n) for lists)
#   - Items must be immutable (strings, numbers, tuples -- not lists or dicts)


# === CREATING SETS ============================================================

# Empty set (CAREFUL: {} creates an empty DICT, not a set!)
empty_set = set()           # Correct way to make an empty set
empty_dict = {}             # This is a dictionary, not a set!

# Set with values:
numbers = {1, 2, 3, 4, 5}
fruits = {"apple", "banana", "orange"}

# From a list (removes duplicates automatically):
scores = [85, 90, 85, 92, 90, 88, 85]
unique_scores = set(scores)
print(unique_scores)         # {85, 88, 90, 92} (order may vary)

# From a string (unique characters):
unique_chars = set("hello")
print(unique_chars)          # {'h', 'e', 'l', 'o'} (only one 'l')

# How Python tells sets and dicts apart:
my_set = {1, 2, 3}              # No colons -> SET
my_dict = {"one": 1, "two": 2}  # Has colons -> DICTIONARY


# === ADDING AND REMOVING ELEMENTS =============================================

colors = {"red", "green", "blue"}

# Add one item:
colors.add("yellow")
print(colors)

# Add multiple items:
colors.update(["purple", "orange"])
print(colors)

# Adding a duplicate does nothing (no error, just ignored):
colors.add("red")
print(colors)     # 'red' still appears only once

# Remove an item:
colors.remove("yellow")     # Raises KeyError if not found
colors.discard("yellow")    # Does nothing if not found (safer)
print(colors)

# Remove and return an arbitrary item:
popped = colors.pop()
print(f"Removed: {popped}")

# Remove all items:
# colors.clear()


# === SET OPERATIONS ===========================================================
#
# Sets support mathematical set operations. These are extremely useful for
# comparing collections of data.

python_students = {"Alice", "Bob", "Charlie", "Dave"}
java_students = {"Charlie", "Dave", "Eve", "Frank"}

# UNION: all students (in either set)
all_students = python_students | java_students
# Or: python_students.union(java_students)
print(f"All students: {all_students}")
# {'Alice', 'Bob', 'Charlie', 'Dave', 'Eve', 'Frank'}

# INTERSECTION: students in BOTH sets
both = python_students & java_students
# Or: python_students.intersection(java_students)
print(f"In both: {both}")
# {'Charlie', 'Dave'}

# DIFFERENCE: in Python but NOT in Java
python_only = python_students - java_students
# Or: python_students.difference(java_students)
print(f"Python only: {python_only}")
# {'Alice', 'Bob'}

java_only = java_students - python_students
print(f"Java only: {java_only}")
# {'Eve', 'Frank'}

# SYMMETRIC DIFFERENCE: in one OR the other, but NOT both
exclusive = python_students ^ java_students
# Or: python_students.symmetric_difference(java_students)
print(f"Exclusive: {exclusive}")
# {'Alice', 'Bob', 'Eve', 'Frank'}


# === SET COMPARISONS ==========================================================

a = {1, 2, 3}
b = {1, 2, 3, 4, 5}
c = {1, 2, 3}

# Subset: is every element of a also in b?
print(a.issubset(b))      # True (all of a's items are in b)
print(a <= b)              # True (same thing)

# Superset: does b contain all elements of a?
print(b.issuperset(a))    # True
print(b >= a)              # True

# Equality:
print(a == c)              # True (same elements)

# Disjoint: no elements in common?
print({1, 2}.isdisjoint({3, 4}))  # True
print({1, 2}.isdisjoint({2, 3}))  # False (2 is in both)


# === PRACTICAL USE: DEDUPLICATION =============================================
#
# The fastest way to remove duplicates from a list:

names = ["Alice", "Bob", "Alice", "Charlie", "Bob", "Dave", "Alice"]
unique_names = list(set(names))
print(unique_names)
# Note: order is NOT preserved!

# To preserve order:
seen = set()
unique_ordered = []
for name in names:
    if name not in seen:
        seen.add(name)
        unique_ordered.append(name)
print(unique_ordered)  # ['Alice', 'Bob', 'Charlie', 'Dave']

# Or in Python 3.7+ using dict.fromkeys():
unique_ordered = list(dict.fromkeys(names))  # dict.fromkeys() creates a dict with these keys
print(unique_ordered)  # ['Alice', 'Bob', 'Charlie', 'Dave']


# === PRACTICAL USE: FAST MEMBERSHIP TESTING ===================================
#
# Checking "is X in this collection?" is much faster with sets than lists.
# For a list of 1 million items, "in" checks each one (slow).
# For a set of 1 million items, "in" uses a hash (nearly instant).

# Simulating a word filter:
banned_words = {"spam", "scam", "fraud", "fake"}   # Use a set for speed

message = "This is a totally legitimate offer, not a scam at all"
words = message.lower().split()
flagged = [word for word in words if word in banned_words]
print(f"Flagged words: {flagged}")


# === FROZEN SETS ==============================================================
#
# A frozenset is an immutable set. You cannot add or remove items.
# Since it is immutable, it can be used as a dictionary key or inside
# another set.

immutable = frozenset([1, 2, 3])
print(immutable)

# immutable.add(4)     # AttributeError! Cannot modify frozen set

# Use as dictionary key:
permissions = {
    frozenset(["read"]): "viewer",
    frozenset(["read", "write"]): "editor",
    frozenset(["read", "write", "admin"]): "admin"
}


# === REAL-WORLD EXAMPLE: NLP VOCABULARY BUILDING ==============================

text = """Python is great for AI. Python is used in machine learning.
Machine learning uses Python extensively. AI and machine learning
are transforming the world."""

# Step 1: Tokenize (split into words)
words = text.lower().replace(".", "").split()

# Step 2: Build vocabulary (unique words)
vocabulary = set(words)
print(f"Total words: {len(words)}")
print(f"Unique words (vocabulary size): {len(vocabulary)}")
print(f"Vocabulary: {sorted(vocabulary)}")

# Step 3: Find common words between two texts
text2 = "Java is also popular for software development and AI applications"
words2 = set(text2.lower().replace(".", "").split())

common = vocabulary & words2
print(f"\nCommon words: {common}")

unique_to_text1 = vocabulary - words2
print(f"Only in text 1: {sorted(unique_to_text1)}")


# === REAL-WORLD EXAMPLE: FEATURE COMPARISON ===================================

model_a_features = {"age", "income", "education", "location", "credit_score"}
model_b_features = {"age", "income", "employment", "debt_ratio", "credit_score"}

print(f"Common features: {model_a_features & model_b_features}")
print(f"Only in Model A: {model_a_features - model_b_features}")
print(f"Only in Model B: {model_b_features - model_a_features}")
print(f"All features: {model_a_features | model_b_features}")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Creating an empty set with {}
empty = {}            # This is a DICT, not a set!
print(type(empty))    # <class 'dict'>
empty = set()         # This is a set
print(type(empty))    # <class 'set'>

# MISTAKE 2: Trying to put mutable items in a set
# Wrong:
#   bad_set = {[1, 2], [3, 4]}  # TypeError: unhashable type: 'list'
# Right:
good_set = {(1, 2), (3, 4)}    # Tuples are immutable, so they work

# MISTAKE 3: Expecting sets to be ordered
numbers = {3, 1, 4, 1, 5, 9}
print(numbers)   # Could be {1, 3, 4, 5, 9} -- order is not guaranteed
# If you need order, use a list

# MISTAKE 4: Trying to index a set
# Wrong:
#   print(numbers[0])   # TypeError: 'set' object is not subscriptable
# Right: convert to a list first or iterate
for num in numbers:
    print(num, end=" ")
print()


# === EXERCISES ================================================================
#
# Exercise 1: Given two lists, find all elements that appear in both.
#             list_a = [1, 2, 3, 4, 5, 6]
#             list_b = [4, 5, 6, 7, 8, 9]
#
# Exercise 2: Write code that takes a sentence and counts the number
#             of unique words (case-insensitive).
#
# Exercise 3: Given a list of email addresses, find which domains are used:
#             emails = ["a@gmail.com", "b@yahoo.com", "c@gmail.com",
#                       "d@outlook.com", "e@yahoo.com"]
#
# Exercise 4: Two teams played a quiz with multiple rounds. Find:
#             a) Questions both teams got right
#             b) Questions only team A got right
#             c) All questions answered correctly by at least one team
#             team_a_correct = {1, 3, 5, 7, 9, 10}
#             team_b_correct = {2, 3, 5, 6, 8, 10}


# === SOLUTIONS ================================================================
#
# Exercise 1:
# list_a = [1, 2, 3, 4, 5, 6]
# list_b = [4, 5, 6, 7, 8, 9]
# common = set(list_a) & set(list_b)
# print(f"Common: {common}")  # {4, 5, 6}
#
# Exercise 2:
# sentence = "The cat sat on the mat and the cat purred"
# words = sentence.lower().split()
# unique = set(words)
# print(f"Unique words: {len(unique)}")  # 7
#
# Exercise 3:
# emails = ["a@gmail.com", "b@yahoo.com", "c@gmail.com",
#           "d@outlook.com", "e@yahoo.com"]
# domains = {email.split("@")[1] for email in emails}
# print(f"Domains: {domains}")  # {'gmail.com', 'yahoo.com', 'outlook.com'}
#
# Exercise 4:
# team_a = {1, 3, 5, 7, 9, 10}
# team_b = {2, 3, 5, 6, 8, 10}
# print(f"Both got right: {team_a & team_b}")
# print(f"Only team A: {team_a - team_b}")
# print(f"At least one team: {team_a | team_b}")


# === KEY TAKEAWAYS ============================================================
#
# - Sets store unique, unordered items in curly braces {}
# - Empty set: set(), NOT {} (that creates a dict)
# - Set operations: | (union), & (intersection), - (difference), ^ (symmetric)
# - Membership testing ("in") is very fast for sets
# - Items must be immutable (no lists or dicts inside sets)
# - frozenset is an immutable set (can be used as a dict key)
# - Sets are ideal for deduplication, vocabulary building, and comparisons


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (12_functions_basics.py), you will learn how to write
# your own reusable blocks of code. Functions are the building blocks of
# any real program -- and every AI system is built from functions.
