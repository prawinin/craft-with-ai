# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 07: Loops
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - for loops (iterating over sequences)
    - range() function
    - while loops (repeating until a condition changes)
    - break, continue, and else in loops
    - enumerate() and zip()
    - Nested loops
    - List comprehensions (preview)

  Why this matters for AI:
    Machine learning IS looping. Training a model means looping over data
    thousands of times (epochs). Processing a dataset means looping over
    every row. Generating AI output means looping token by token. Without
    loops, there is no AI.

  Estimated time: 30 minutes

===============================================================================
"""


# === FOR LOOPS: THE BASICS ====================================================
#
# A for loop repeats a block of code ONCE for each item in a sequence.
#
# Real-world analogy:
#   You have a stack of exam papers. "For each paper in the stack, grade it."
#   You pick up one paper, grade it, pick up the next, grade it, and so on
#   until the stack is empty.

# Looping over a list:
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"I like {fruit}")
# Output:
# I like apple
# I like banana
# I like orange

# The variable "fruit" takes on each value in the list, one at a time.
# You can name this variable anything -- "fruit" is just descriptive.

# Looping over a string:
name = "Python"
for letter in name:
    print(letter)
# Output: P, y, t, h, o, n (each on a new line)


# === range(): GENERATING NUMBER SEQUENCES =====================================
#
# range() creates a sequence of numbers. It is the most common way to run
# a loop a specific number of times.

# range(n) -> 0, 1, 2, ..., n-1
for i in range(5):
    print(i)
# Output: 0, 1, 2, 3, 4

# range(start, stop) -> start, start+1, ..., stop-1
for i in range(1, 6):
    print(i)
# Output: 1, 2, 3, 4, 5

# range(start, stop, step) -> start, start+step, start+2*step, ...
for i in range(0, 10, 2):
    print(i)
# Output: 0, 2, 4, 6, 8

# Count backwards:
for i in range(5, 0, -1):
    print(i)
# Output: 5, 4, 3, 2, 1

# KEY POINT: The stop value is NEVER included. range(1, 6) gives 1-5, not 1-6.
# Think of it as: "stop BEFORE reaching this number."


# === WHILE LOOPS: REPEAT UNTIL A CONDITION CHANGES ============================
#
# A while loop keeps running as long as a condition is True.
#
# Real-world analogy:
#   "While the pot is not boiling, keep the heat on."
#   You keep checking. Once it boils, you stop.

count = 0
while count < 5:
    print(f"Count is {count}")
    count += 1          # CRITICAL: must update the condition variable!
# Output: Count is 0, Count is 1, ... Count is 4

# WARNING: If you forget to update the condition variable, you get an
# INFINITE LOOP. Your program will run forever (or until you kill it).
# Wrong:
#   while True:
#       print("Forever!")   # Never stops!

# while True with a break (a common pattern):
import random  # (Packages and modules are covered in 15_packages_and_modules.py)
attempts = 0
while True:
    number = random.randint(1, 10)
    attempts += 1
    if number == 7:
        print(f"Found 7 after {attempts} attempts!")
        break       # Exit the loop


# === WHEN TO USE for vs while =================================================
#
# Use FOR when:
#   - You know how many times to loop (or you are iterating over a collection)
#   - Examples: loop 10 times, loop over each item in a list
#
# Use WHILE when:
#   - You do NOT know how many times to loop
#   - You loop until some condition changes
#   - Examples: keep asking for input until valid, keep training until
#     the model converges


# === break AND continue =======================================================
#
# break:    Immediately exit the loop entirely.
# continue: Skip the rest of THIS iteration and jump to the next one.

# --- break example ---
print("\n--- break example ---")
for i in range(10):
    if i == 5:
        print("Found 5, stopping!")
        break
    print(i)
# Output: 0, 1, 2, 3, 4, Found 5, stopping!

# --- continue example ---
print("\n--- continue example ---")
for i in range(10):
    if i % 2 == 0:      # Skip even numbers
        continue
    print(i)
# Output: 1, 3, 5, 7, 9


# === ELSE CLAUSE ON LOOPS ====================================================
#
# Python has a unique feature: you can put else on a loop.
# The else block runs if the loop completed WITHOUT hitting a break.
# Think of it as "if the loop finished normally."

# Looking for a specific value:
numbers = [1, 3, 5, 7, 9]
target = 4

for num in numbers:
    if num == target:
        print(f"Found {target}!")
        break
else:
    print(f"{target} was not found in the list")
# Output: 4 was not found in the list

# This is cleaner than using a flag variable:
# found = False
# for num in numbers:
#     if num == target:
#         found = True
#         break
# if not found:
#     print("Not found")


# === enumerate(): LOOP WITH INDEX =============================================
#
# When you need BOTH the index and the value, use enumerate().

fruits = ["apple", "banana", "orange", "grape"]

# Without enumerate (works but verbose):
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")

# With enumerate (clean and Pythonic):
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# Start counting from 1 instead of 0:
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}. {fruit}")
# Output:
# 1. apple
# 2. banana
# 3. orange
# 4. grape


# === zip(): LOOP OVER MULTIPLE SEQUENCES =====================================
#
# zip() pairs up items from two (or more) sequences:

names = ["Alice", "Bob", "Charlie"]
scores = [92, 85, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
# Output:
# Alice: 92
# Bob: 85
# Charlie: 78

# With three sequences:
subjects = ["Math", "English", "Science"]
for name, score, subject in zip(names, scores, subjects):
    print(f"{name} got {score} in {subject}")

# NOTE: zip stops at the shortest sequence. If one list is longer,
# the extra items are silently ignored.


# === NESTED LOOPS =============================================================
#
# A loop inside a loop. The inner loop runs completely for EACH iteration
# of the outer loop.
#
# Real-world analogy:
#   "For each row in the classroom, for each seat in that row, check
#   if a student is present."

# Multiplication table:
print("\nMultiplication Table:")
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:4}", end="")  # :4 pads to 4 characters wide
    print()  # New line after each row

# Output:
#    1   2   3   4   5
#    2   4   6   8  10
#    3   6   9  12  15
#    4   8  12  16  20
#    5  10  15  20  25


# === LOOPING OVER DICTIONARIES ================================================

person = {"name": "Alice", "age": 30, "city": "New York"}

# Loop over keys (default):
for key in person:
    print(key)

# Loop over values:
for value in person.values():
    print(value)

# Loop over key-value pairs:
for key, value in person.items():
    print(f"{key}: {value}")


# === LIST COMPREHENSIONS (PREVIEW) ============================================
#
# A compact way to create lists using a loop. This is VERY common in Python
# and AI code. We will use this heavily in later lessons.

# Traditional loop:
squares = []
for x in range(10):
    squares.append(x ** 2)
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# List comprehension (same result, one line):
squares = [x ** 2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With a condition (filter):
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
print(even_squares)  # [0, 4, 16, 36, 64]

# In AI, list comprehensions are used constantly:
# Clean text: [word.lower() for word in words if len(word) > 2]
# Filter data: [x for x in data if x is not None]
# Transform:  [preprocess(sample) for sample in dataset]


# === REAL-WORLD EXAMPLE: TRAINING LOOP ========================================
#
# This is a simplified version of what an AI training loop looks like.
# Do not worry about understanding every detail -- focus on the loop structure.

# Simulated training data and model
training_data = [
    {"input": [1, 2], "target": 3},
    {"input": [4, 5], "target": 9},
    {"input": [2, 3], "target": 5},
]

n_epochs = 3        # How many times to go through ALL data
learning_rate = 0.1

print("\n--- Simulated Training Loop ---")
for epoch in range(n_epochs):
    total_loss = 0
    for batch in training_data:
        # Simulate: predict, calculate loss, update model
        prediction = sum(batch["input"])     # Simple "model" (sum() adds all numbers, covered in 08_lists.py)
        loss = abs(prediction - batch["target"])  # abs() gives absolute/positive value
        total_loss += loss

    avg_loss = total_loss / len(training_data)
    print(f"Epoch {epoch + 1}/{n_epochs}, Average Loss: {avg_loss:.4f}")

print("Training complete!")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Missing colon after for/while
# Wrong:
#   for i in range(5)
#       print(i)
# Right:
for i in range(5):
    print(i, end=" ")
print()

# MISTAKE 2: Wrong indentation
# Wrong:
#   for i in range(3):
#   print(i)            # IndentationError!
# Right:
for i in range(3):
    print(i, end=" ")
print()

# MISTAKE 3: Off-by-one with range
# Want to print 1 through 5:
# Wrong:
#   for i in range(5):     # Gives 0, 1, 2, 3, 4
# Right:
for i in range(1, 6):      # Gives 1, 2, 3, 4, 5
    print(i, end=" ")
print()

# MISTAKE 4: Infinite while loop (forgetting to update condition)
# Wrong:
#   count = 0
#   while count < 5:
#       print(count)     # count never changes -> infinite loop!
# Right:
count = 0
while count < 5:
    print(count, end=" ")
    count += 1
print()

# MISTAKE 5: Modifying a list while iterating over it
# Wrong:
#   numbers = [1, 2, 3, 4, 5]
#   for num in numbers:
#       if num == 3:
#           numbers.remove(num)  # Dangerous! Changes list during loop
# Right (use list comprehension):
numbers = [1, 2, 3, 4, 5]
numbers = [num for num in numbers if num != 3]
print(numbers)  # [1, 2, 4, 5]


# === EXERCISES ================================================================
#
# Exercise 1: Print all even numbers from 1 to 50 using a for loop.
#
# Exercise 2: Write a while loop that keeps generating random numbers
#             between 1 and 100 until it gets a number greater than 90.
#             Print how many attempts it took.
#             Hint: import random, random.randint(1, 100)
#
# Exercise 3: Given a list of words, use a loop to find the longest word.
#             words = ["python", "artificial", "intelligence", "data", "learning"]
#
# Exercise 4: Use enumerate and zip together to print this output:
#             Given: subjects = ["Math", "Science", "English"]
#                    grades = ["A", "B+", "A-"]
#             Output:
#             1. Math: A
#             2. Science: B+
#             3. English: A-
#
# Exercise 5: Write a list comprehension that takes a list of mixed-case words
#             and produces a list of only the words that start with a vowel,
#             all in lowercase.
#             words = ["Apple", "banana", "Orange", "grape", "Umbrella"]
#
# Exercise 6: Write a program that prints the FizzBuzz sequence from 1 to 30:
#             - "Fizz" if divisible by 3
#             - "Buzz" if divisible by 5
#             - "FizzBuzz" if divisible by both
#             - The number itself otherwise


# === SOLUTIONS ================================================================
#
# Exercise 1:
# for i in range(2, 51, 2):
#     print(i, end=" ")
# print()
#
# Exercise 2:
# import random
# attempts = 0
# while True:
#     number = random.randint(1, 100)
#     attempts += 1
#     if number > 90:
#         print(f"Got {number} after {attempts} attempts")
#         break
#
# Exercise 3:
# words = ["python", "artificial", "intelligence", "data", "learning"]
# longest = words[0]
# for word in words:
#     if len(word) > len(longest):
#         longest = word
# print(f"Longest word: {longest}")
#
# Exercise 4:
# subjects = ["Math", "Science", "English"]
# grades = ["A", "B+", "A-"]
# for i, (subject, grade) in enumerate(zip(subjects, grades), start=1):
#     print(f"{i}. {subject}: {grade}")
#
# Exercise 5:
# words = ["Apple", "banana", "Orange", "grape", "Umbrella"]
# vowel_words = [w.lower() for w in words if w[0].lower() in "aeiou"]
# print(vowel_words)  # ['apple', 'orange', 'umbrella']
#
# Exercise 6:
# for i in range(1, 31):
#     if i % 3 == 0 and i % 5 == 0:
#         print("FizzBuzz")
#     elif i % 3 == 0:
#         print("Fizz")
#     elif i % 5 == 0:
#         print("Buzz")
#     else:
#         print(i)


# === KEY TAKEAWAYS ============================================================
#
# - for loops iterate over sequences (lists, strings, range, etc.)
# - while loops repeat until a condition becomes False
# - range(start, stop, step) generates number sequences (stop is excluded)
# - break exits the loop; continue skips to the next iteration
# - enumerate() gives you (index, value) pairs
# - zip() pairs up items from multiple sequences
# - List comprehensions are a concise one-line alternative to simple loops
# - Always make sure while loops have a way to terminate
# - Do not modify a list while iterating over it


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (08_lists.py), you will take a deep dive into Python's
# most versatile data structure: the list. Lists are how you store collections
# of data -- training samples, model predictions, feature vectors. Mastering
# lists is essential for any AI work.
