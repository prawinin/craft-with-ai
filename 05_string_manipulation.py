# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 05: String Manipulation
  Difficulty: Beginner
===============================================================================

  What you will learn:
    - Creating strings (single, double, triple quotes, raw strings)
    - f-strings and string formatting
    - String indexing and slicing
    - Common string methods (upper, lower, strip, split, join, replace, find)
    - String searching and checking
    - Escape characters and raw strings
    - String immutability

  Why this matters for AI:
    All Natural Language Processing starts with strings. Before text reaches
    a language model, it goes through preprocessing: lowercasing, stripping
    whitespace, tokenizing (splitting into words), removing punctuation,
    and more. Every one of these operations uses string methods.

  Estimated time: 30 minutes

===============================================================================
"""


# === CREATING STRINGS =========================================================

# Single and double quotes are equivalent:
name = "Alice"
name = 'Alice'

# Triple quotes for multi-line strings:
bio = """Alice is a data scientist
who specializes in natural language processing.
She has been coding in Python for 5 years."""
print(bio)

# Raw strings (ignore escape characters) -- useful for file paths and regex:
path = r"C:\Users\Documents\new_file.txt"
print(path)  # C:\Users\Documents\new_file.txt (backslashes are literal)


# === STRING CONCATENATION =====================================================
#
# Joining strings together.

first_name = "Jane"
last_name = "Doe"

# Method 1: Using + (basic, but can get messy)
full_name = first_name + " " + last_name  # "Jane Doe"
print(full_name)

# Method 2: Using f-strings (the modern Python way -- USE THIS)
greeting = f"Hello, {first_name}!"
print(greeting)  # Hello, Jane!

# f-strings can contain any expression:
age = 25
intro = f"I'm {first_name} and I'm {age} years old"
print(intro)

# f-strings can do math:
price = 49.99
tax_rate = 0.08
print(f"Total: ${price * (1 + tax_rate):.2f}")  # Total: $53.99

# f-strings can call functions:
print(f"Name in caps: {first_name.upper()}")
print(f"Name length: {len(first_name)}")

# Method 3: String repetition with *
star = "*"
stars = star * 10  # "**********"
print(stars)

separator = "-" * 50
print(separator)


# === STRING FORMATTING WITH f-strings =========================================
#
# f-strings support powerful formatting options after a colon:

# --- Decimal places ---
pi = 3.14159265358979
print(f"Pi: {pi}")           # Pi: 3.14159265358979
print(f"Pi: {pi:.2f}")       # Pi: 3.14 (2 decimal places)
print(f"Pi: {pi:.4f}")       # Pi: 3.1416 (4 decimal places, rounded)

# --- Percentages ---
accuracy = 0.9234
print(f"Accuracy: {accuracy:.1%}")   # Accuracy: 92.3%
print(f"Accuracy: {accuracy:.2%}")   # Accuracy: 92.34%

# --- Padding and alignment ---
for item in ["Apple", "Banana", "Kiwi"]:
    print(f"{item:<15} ${1.99:.2f}")    # Left-aligned in 15 chars
# Output:
# Apple           $1.99
# Banana          $1.99
# Kiwi            $1.99

# --- Thousands separator ---
population = 8000000000
print(f"Population: {population:,}")     # Population: 8,000,000,000
print(f"Population: {population:_}")     # Population: 8_000_000_000


# === STRING INDEXING ===========================================================
#
# Every character in a string has a position (index), starting from 0.
#
#   P  y  t  h  o  n
#   0  1  2  3  4  5     (positive index)
#  -6 -5 -4 -3 -2 -1    (negative index)

text = "Python"

print(text[0])     # P (first character)
print(text[1])     # y (second character)
print(text[-1])    # n (last character)
print(text[-2])    # o (second to last)

# Strings are IMMUTABLE -- you cannot change a character in place:
# text[0] = "J"    # TypeError: 'str' object does not support item assignment
# You have to create a new string:
new_text = "J" + text[1:]
print(new_text)    # Jython


# === STRING SLICING ===========================================================
#
# Extract a portion of a string using [start:end] or [start:end:step].
# The start index is INCLUDED, the end index is EXCLUDED.
#
# Think of it like cutting a piece from a loaf of bread:
#   You say "from position 2 to position 5" and you get characters at 2, 3, 4.

text = "Python Programming"

print(text[0:6])     # "Python"     (characters 0-5)
print(text[7:])      # "Programming" (character 7 to end)
print(text[:6])      # "Python"     (start to character 5)
print(text[-11:])    # "Programming" (last 11 characters)

# With step:
print(text[::2])     # "Pto rgamn" (every 2nd character)
print(text[::-1])    # "gnimmargorP nohtyP" (reversed!)

# Reversing a string:
name = "Alice"
print(name[::-1])    # ecilA


# === STRING METHODS: CASE CHANGES =============================================

text = "Python Programming"

print(text.lower())      # "python programming"
print(text.upper())      # "PYTHON PROGRAMMING"
print(text.title())      # "Python Programming" (capitalize each word)
print(text.capitalize())  # "Python programming" (only first char)
print(text.swapcase())   # "pYTHON pROGRAMMING"

# Real-world use: normalizing user input
user_input = "  YES  "
cleaned = user_input.strip().lower()
print(cleaned == "yes")  # True (regardless of case or spaces)


# === STRING METHODS: STRIPPING WHITESPACE =====================================

messy = "   hello world   "
print(messy.strip())      # "hello world" (both sides)
print(messy.lstrip())     # "hello world   " (left only)
print(messy.rstrip())     # "   hello world" (right only)

# Strip specific characters:
price = "$19.99"
print(price.strip("$"))   # "19.99"

filename = "report.csv..."
print(filename.rstrip("."))  # "report.csv"


# === STRING METHODS: SPLITTING AND JOINING ====================================
#
# split() breaks a string into a list of parts.
# join() combines a list of strings into a single string.
# These two are inverses of each other.

# --- split() -----------------------------------------------------------------
sentence = "Python is great for AI"
words = sentence.split()           # Split on whitespace (default)
print(words)  # ['Python', 'is', 'great', 'for', 'AI']

csv_data = "Alice,30,Engineer"
fields = csv_data.split(",")       # Split on comma
print(fields)  # ['Alice', '30', 'Engineer']

path = "/home/user/documents/file.txt"
parts = path.split("/")
print(parts)   # ['', 'home', 'user', 'documents', 'file.txt']

# Split with a limit:
text = "one-two-three-four"
print(text.split("-", 2))  # ['one', 'two', 'three-four'] (max 2 splits)

# --- join() ------------------------------------------------------------------
words = ["Python", "is", "great"]
sentence = " ".join(words)
print(sentence)  # "Python is great"

# Join with different separators:
path_parts = ["home", "user", "documents"]
print("/".join(path_parts))    # home/user/documents
print(", ".join(words))        # Python, is, great
print("-".join(["2026", "04", "10"]))  # 2026-04-10


# === STRING METHODS: SEARCHING AND CHECKING ===================================

message = "I love Python programming with Python"

# --- Check if something exists ---
print("Python" in message)           # True
print("Java" in message)             # False

# --- Check start and end ---
print(message.startswith("I"))        # True
print(message.endswith("Python"))     # True

# --- Find position ---
print(message.find("Python"))         # 7 (first occurrence, 0-indexed)
print(message.find("Java"))           # -1 (not found)

# --- Count occurrences ---
print(message.count("Python"))        # 2

# --- Check string content ---
print("hello".isalpha())      # True (only letters)
print("12345".isdigit())      # True (only digits)
print("hello123".isalnum())   # True (letters and/or digits)
print("   ".isspace())        # True (only whitespace)
print("Hello World".istitle()) # True (title case)


# === STRING METHODS: REPLACING ================================================

message = "I love Python programming with Python"

new_message = message.replace("Python", "JavaScript")
print(new_message)  # "I love JavaScript programming with JavaScript"

# Replace with a limit:
new_message = message.replace("Python", "JavaScript", 1)
print(new_message)  # "I love JavaScript programming with Python" (only first)

# Chaining replacements:
dirty = "Hello...World!!!...Python!!!"
clean = dirty.replace("...", " ").replace("!!!", "")
print(clean)  # "Hello World Python"


# === STRING METHODS: SPLITTING LINES ==========================================

multiline = """Line one
Line two
Line three"""

lines = multiline.splitlines()
print(lines)  # ['Line one', 'Line two', 'Line three']

# Useful for processing text files, log files, or multi-line AI outputs.


# === STRING METHODS: PADDING AND CENTERING ====================================

text = "Python"
print(text.center(20, "="))   # =======Python=======
print(text.ljust(20, "-"))    # Python--------------
print(text.rjust(20, "-"))    # --------------Python
print("42".zfill(5))          # 00042 (pad with zeros)


# === REAL-WORLD EXAMPLE: TEXT PREPROCESSING FOR AI ============================
#
# Before feeding text to an AI model, you typically clean it up:

raw_text = "  Hello, World! This is a TEST... Can you clean ME up?  "

# Step 1: Strip leading/trailing whitespace
cleaned = raw_text.strip()

# Step 2: Convert to lowercase (most NLP models prefer lowercase)
cleaned = cleaned.lower()

# Step 3: Remove punctuation
import string  # (Modules and imports are covered in 15_packages_and_modules.py)
cleaned = cleaned.translate(str.maketrans("", "", string.punctuation))

# Step 4: Split into words (tokenization)
tokens = cleaned.split()

# Step 5: Remove short words (often not meaningful)
tokens = [word for word in tokens if len(word) > 2]

print("Original:", raw_text)
print("Cleaned:", cleaned)
print("Tokens:", tokens)
# Tokens: ['hello', 'world', 'this', 'test', 'can', 'you', 'clean']


# === ESCAPE CHARACTERS (REVIEW) ===============================================

print("Line 1\nLine 2")       # \n = newline
print("Col1\tCol2\tCol3")     # \t = tab
print("She said \"hello\"")   # \" = double quote
print('It\'s done')           # \' = single quote
print("Path: C:\\Users")      # \\ = literal backslash

# To avoid escaping, use raw strings:
print(r"No \n newline here")   # Prints the literal \n


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Mismatched quotes
# Wrong:
#   text = 'It's Python'    # SyntaxError!
# Right:
text = "It's Python"        # Use double quotes outside
text = 'It\'s Python'       # Or escape the apostrophe

# MISTAKE 2: Trying to modify a string in place
text = "Hello"
# Wrong:
#   text[0] = "J"           # TypeError! Strings are immutable
# Right:
text = "J" + text[1:]       # Create a new string

# MISTAKE 3: Forgetting that find() returns -1 (not False) when not found
text = "Hello World"
pos = text.find("Python")
# Wrong:
#   if text.find("Python"):     # -1 is truthy! This evaluates to True
# Right:
if text.find("Python") != -1:
    print("Found")
# Even better:
if "Python" in text:
    print("Found")

# MISTAKE 4: Splitting and getting empty strings
path = "/home/user/"
parts = path.split("/")
print(parts)  # ['', 'home', 'user', '']  (empty strings at edges!)
# Fix: filter them out
parts = [p for p in path.split("/") if p]
print(parts)  # ['home', 'user']


# === EXERCISES ================================================================
#
# Exercise 1: Given the string "Hello, World!", extract just "World" using
#             slicing.
#
# Exercise 2: Write code that takes a full name like "john doe" and converts
#             it to "John Doe" (title case). Then extract just the last name.
#
# Exercise 3: Given an email "user@example.com", extract the username
#             and domain separately.
#
# Exercise 4: Count how many words are in this sentence:
#             "The quick brown fox jumps over the lazy dog"
#
# Exercise 5: Write code to clean up a phone number.
#             Input:  "  (555) 123-4567  "
#             Output: "5551234567" (digits only)
#             Hint: use replace() multiple times or use a loop with isdigit()
#
# Exercise 6: Build a simple text preprocessor that takes any string and:
#             - Strips whitespace
#             - Converts to lowercase
#             - Replaces multiple spaces with a single space
#             - Returns the word count


# === SOLUTIONS ================================================================
#
# Exercise 1:
# text = "Hello, World!"
# print(text[7:12])   # "World"
#
# Exercise 2:
# name = "john doe"
# proper = name.title()
# last_name = proper.split()[-1]
# print(proper, "|", last_name)
#
# Exercise 3:
# email = "user@example.com"
# username, domain = email.split("@")
# print(f"Username: {username}, Domain: {domain}")
#
# Exercise 4:
# sentence = "The quick brown fox jumps over the lazy dog"
# word_count = len(sentence.split())
# print(f"Word count: {word_count}")  # 9
#
# Exercise 5:
# phone = "  (555) 123-4567  "
# clean = ""
# for char in phone:
#     if char.isdigit():
#         clean += char
# print(clean)  # 5551234567
#
# Exercise 6:
# def preprocess(text):
#     text = text.strip()
#     text = text.lower()
#     while "  " in text:
#         text = text.replace("  ", " ")
#     word_count = len(text.split())
#     return text, word_count
# result, count = preprocess("  Hello   World   Python  ")
# print(f"Text: '{result}', Words: {count}")


# === KEY TAKEAWAYS ============================================================
#
# - Strings are immutable sequences of characters
# - f-strings (f"...{var}...") are the best way to format strings
# - Slicing: text[start:end:step] extracts portions
# - split() breaks strings into lists, join() combines lists into strings
# - strip() removes whitespace (or specified characters)
# - find() returns position (-1 if not found), "in" checks membership
# - replace() creates a new string with substitutions
# - String preprocessing is a critical first step in NLP/AI work


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (06_if_statements.py), you will learn how to make your
# programs make decisions. If statements let your code choose different paths
# based on conditions -- essential for AI systems that need to react differently
# to different inputs.
