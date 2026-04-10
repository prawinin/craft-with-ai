# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 17: Working with Data
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - Introduction to pandas (the data analysis powerhouse)
    - Creating and inspecting DataFrames
    - Reading CSV/JSON files
    - Selecting, filtering, and transforming data
    - Basic data analysis (groupby, aggregation, statistics)
    - Creating charts with matplotlib
    - Saving data and plots

  Why this matters for AI:
    Before any model training, you need to UNDERSTAND your data. pandas
    is how you load, explore, clean, and transform datasets. matplotlib
    is how you visualize patterns. These two libraries are used in literally
    every data science and AI project.

  Estimated time: 35 minutes

  Prerequisites: pip install pandas matplotlib

===============================================================================
"""


# === WHAT IS PANDAS? ==========================================================
#
# pandas is a Python library for working with tabular data (think Excel or
# Google Sheets, but programmable). Its main data structure is the DataFrame:
# a 2D table with rows and columns.
#
# Real-world analogy:
#   pandas is like Excel on steroids. You can do everything Excel does
#   (filter, sort, pivot, chart), but with code instead of clicks. This
#   means it is repeatable, automatable, and can handle millions of rows.

import pandas as pd

# === CREATING DATAFRAMES =====================================================

# From a dictionary (most common):
data = {
    "name": ["Alice", "Bob", "Charlie", "Dave", "Eve"],
    "age": [25, 30, 35, 28, 32],
    "city": ["NYC", "London", "Paris", "Tokyo", "Sydney"],
    "salary": [70000, 85000, 92000, 78000, 88000]
}

df = pd.DataFrame(data)
print(df)
print()

# From a list of dictionaries (common with API responses):
records = [
    {"name": "Alice", "score": 92},
    {"name": "Bob", "score": 85},
    {"name": "Charlie", "score": 78}
]
df_records = pd.DataFrame(records)
print(df_records)
print()


# === INSPECTING DATA ==========================================================
#
# When you get a new dataset, always inspect it first.

print("--- DataFrame Info ---")
print(f"Shape: {df.shape}")          # (rows, columns)
print(f"Columns: {list(df.columns)}")
print(f"\nFirst 3 rows:")
print(df.head(3))                    # First n rows
print(f"\nData types:")
print(df.dtypes)                     # Type of each column
print(f"\nBasic statistics:")
print(df.describe())                 # Mean, std, min, max, etc.
print(f"\nAny missing values?")
print(df.isnull().sum())             # Count of missing values per column


# === SELECTING DATA ===========================================================

# Single column (returns a Series):
print(df["name"])
# print(df.name)    # Also works, but square brackets are preferred

# Multiple columns (returns a DataFrame):
print(df[["name", "salary"]])

# Single row by index:
print(df.iloc[0])       # First row (by position)
print(df.iloc[-1])      # Last row

# Slice of rows:
print(df.iloc[1:4])     # Rows 1, 2, 3

# Specific cell:
print(df.iloc[0, 1])    # Row 0, column 1 (age of Alice)
print(df.loc[0, "name"])  # Row 0, column "name" -- same thing by label


# === FILTERING DATA ===========================================================
#
# This is where pandas shines. Filter rows based on conditions.

# Single condition:
high_salary = df[df["salary"] > 80000]
print("\nSalary > 80k:")
print(high_salary)

# Multiple conditions (use & for AND, | for OR, wrap each in parentheses):
experienced_and_rich = df[(df["age"] > 28) & (df["salary"] > 80000)]
print("\nAge > 28 AND salary > 80k:")
print(experienced_and_rich)

# Filter with isin():
target_cities = ["NYC", "London"]
filtered = df[df["city"].isin(target_cities)]
print(f"\nIn NYC or London:")
print(filtered)

# Filter strings:
# df[df["name"].str.contains("li")]  # Names containing "li"
# df[df["name"].str.startswith("A")] # Names starting with "A"


# === ADDING AND MODIFYING COLUMNS ============================================

# Add a new column:
df["bonus"] = df["salary"] * 0.1
print("\nWith bonus column:")
print(df)

# Apply a function to a column:
df["name_upper"] = df["name"].apply(str.upper)
print(df[["name", "name_upper"]])

# Conditional column:
df["level"] = df["salary"].apply(lambda x: "Senior" if x > 85000 else "Junior")
print(df[["name", "salary", "level"]])

# Drop columns:
df = df.drop(columns=["name_upper"])


# === SORTING ==================================================================

# Sort by one column:
print("\nSorted by salary (descending):")
print(df.sort_values("salary", ascending=False))

# Sort by multiple columns:
print("\nSorted by city then salary:")
print(df.sort_values(["city", "salary"]))


# === GROUPBY AND AGGREGATION =================================================
#
# GroupBy is one of the most powerful pandas features. It splits data into
# groups, applies a function to each group, and combines the results.

# Create sample data with departments:
employees = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank"],
    "dept": ["Engineering", "Marketing", "Engineering", "Marketing", "Engineering", "Marketing"],
    "salary": [95000, 70000, 88000, 75000, 92000, 68000]
})

# Average salary by department:
print("\nAverage salary by department:")
print(employees.groupby("dept")["salary"].mean())

# Multiple aggregations:
print("\nDepartment statistics:")
print(employees.groupby("dept")["salary"].agg(["mean", "min", "max", "count"]))

# Group by and count:
print(f"\nEmployees per department:")
print(employees["dept"].value_counts())


# === HANDLING MISSING DATA ====================================================

# Create data with missing values:
df_missing = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Dave"],
    "age": [25, None, 35, 28],
    "score": [85, 90, None, 78]
})

print("\nData with missing values:")
print(df_missing)
print(f"\nMissing counts:\n{df_missing.isnull().sum()}")

# Fill missing values:
df_filled = df_missing.fillna({"age": df_missing["age"].mean(), "score": 0})
print(f"\nAfter filling:\n{df_filled}")

# Drop rows with any missing value:
df_clean = df_missing.dropna()
print(f"\nAfter dropping:{df_clean}")


# === READING AND WRITING FILES ================================================

# --- CSV Files ---
# Write to CSV:
df.to_csv("sample_data.csv", index=False)
print("\nSaved sample_data.csv")

# Read from CSV:
df_loaded = pd.read_csv("sample_data.csv")
print(f"Loaded {len(df_loaded)} rows from CSV")
print(df_loaded.head())

# --- JSON Files ---
# Write to JSON:
df.to_json("sample_data.json", orient="records", indent=2)

# Read from JSON:
# df_json = pd.read_json("sample_data.json")


# === VISUALIZATION WITH MATPLOTLIB ==========================================

import matplotlib.pyplot as plt

# --- Bar Chart ---
plt.figure(figsize=(8, 5))
plt.bar(df["name"], df["salary"], color=["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336"])
plt.title("Employee Salaries")
plt.xlabel("Employee")
plt.ylabel("Salary ($)")
plt.tight_layout()
plt.savefig("salary_chart.png", dpi=100)
plt.close()
print("\nSaved salary_chart.png")


# --- Line Chart (using weather-like data) ---
import numpy as np

# Generate sample time series data:
dates = pd.date_range("2026-01-01", periods=30, freq="D")
temperatures = 20 + 5 * np.sin(np.linspace(0, 2 * np.pi, 30)) + np.random.normal(0, 1, 30)

weather_df = pd.DataFrame({"date": dates, "temperature": temperatures})

plt.figure(figsize=(10, 5))
plt.plot(weather_df["date"], weather_df["temperature"], marker="o", markersize=4,
         linewidth=2, color="#2196F3", label="Temperature")
plt.fill_between(weather_df["date"], weather_df["temperature"],
                 alpha=0.1, color="#2196F3")
plt.title("Temperature Over 30 Days")
plt.xlabel("Date")
plt.ylabel("Temperature (C)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("temperature_chart.png", dpi=100)
plt.close()
print("Saved temperature_chart.png")


# --- Histogram ---
np.random.seed(42)
scores = np.random.normal(75, 10, 200)   # 200 scores, mean=75, std=10

plt.figure(figsize=(8, 5))
plt.hist(scores, bins=20, color="#4CAF50", edgecolor="white", alpha=0.8)
plt.axvline(np.mean(scores), color="red", linestyle="--", label=f"Mean: {np.mean(scores):.1f}")
plt.title("Distribution of Test Scores")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig("scores_histogram.png", dpi=100)
plt.close()
print("Saved scores_histogram.png")


# --- Scatter Plot ---
np.random.seed(42)
study_hours = np.random.uniform(1, 10, 50)
exam_scores = 40 + 5 * study_hours + np.random.normal(0, 5, 50)

plt.figure(figsize=(8, 5))
plt.scatter(study_hours, exam_scores, c=exam_scores, cmap="viridis",
            alpha=0.7, edgecolors="white", s=80)
plt.colorbar(label="Score")
plt.title("Study Hours vs Exam Score")
plt.xlabel("Hours Studied")
plt.ylabel("Exam Score")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("scatter_plot.png", dpi=100)
plt.close()
print("Saved scatter_plot.png")


# === REAL-WORLD EXAMPLE: COMPLETE DATA ANALYSIS ==============================

print("\n" + "=" * 50)
print("  COMPLETE DATA ANALYSIS EXAMPLE")
print("=" * 50)

# Create a realistic dataset:
np.random.seed(42)
n = 100
dataset = pd.DataFrame({
    "student_id": range(1, n + 1),
    "study_hours": np.random.uniform(1, 12, n).round(1),
    "sleep_hours": np.random.uniform(4, 10, n).round(1),
    "attendance": np.random.uniform(50, 100, n).round(1),
    "exam_score": np.zeros(n)  # We will calculate this
})

# Simulate exam scores based on study habits:
dataset["exam_score"] = (
    30
    + 3 * dataset["study_hours"]
    + 2 * dataset["sleep_hours"]
    + 0.2 * dataset["attendance"]
    + np.random.normal(0, 5, n)
).round(1)

# Clip scores to 0-100:
dataset["exam_score"] = dataset["exam_score"].clip(0, 100)

# Analyze:
print(f"\nDataset shape: {dataset.shape}")
print(f"\nSample rows:")
print(dataset.head())
print(f"\nStatistics:")
print(dataset.describe().round(2))

# Correlations:
print(f"\nCorrelation with exam score:")
numeric_cols = ["study_hours", "sleep_hours", "attendance", "exam_score"]
correlations = dataset[numeric_cols].corr()["exam_score"].drop("exam_score")
print(correlations.sort_values(ascending=False).round(3))

# Add a grade column:
def assign_grade(score):
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"

dataset["grade"] = dataset["exam_score"].apply(assign_grade)

# Grade distribution:
print(f"\nGrade distribution:")
print(dataset["grade"].value_counts().sort_index())

# Save the analysis:
dataset.to_csv("student_analysis.csv", index=False)
print("\nSaved student_analysis.csv")

# Clean up generated files:
import os
for f in ["sample_data.csv", "sample_data.json"]:
    if os.path.exists(f):
        os.remove(f)


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Chained indexing
# Wrong:
#   df[df["age"] > 25]["salary"] = 100000   # May not modify original df
# Right:
#   df.loc[df["age"] > 25, "salary"] = 100000

# MISTAKE 2: Forgetting axis in drop
# df.drop("name")          # Tries to drop ROW named "name"
# df.drop("name", axis=1)  # Drops COLUMN named "name"
# df.drop(columns=["name"])  # Clearer way to drop a column

# MISTAKE 3: Modifying a copy vs the original
# filtered = df[df["age"] > 25]
# filtered["new_col"] = 1    # Warning! This modifies a copy
# Use .copy(): filtered = df[df["age"] > 25].copy()

# MISTAKE 4: Not closing matplotlib figures
# plt.show() displays the figure
# plt.close() closes it (frees memory)
# plt.savefig() saves to a file
# In scripts, use savefig + close. In notebooks, use show.


# === EXERCISES ================================================================
#
# Exercise 1: Load the student_analysis.csv file. Find the top 5 students
#             by exam score and print their study hours and grades.
#
# Exercise 2: Using the student dataset, create a grouped analysis:
#             for each grade (A, B, C, D, F), calculate the average
#             study hours, sleep hours, and attendance.
#
# Exercise 3: Create a matplotlib figure with 2 subplots side by side:
#             one showing a histogram of exam scores, and one showing
#             a scatter plot of study hours vs exam scores.
#
# Exercise 4: Write a function that takes a pandas DataFrame and returns
#             a "data quality report" dictionary with: column names,
#             data types, missing value counts, and unique value counts
#             for each column.


# === SOLUTIONS ================================================================
#
# Exercise 1:
# df = pd.read_csv("student_analysis.csv")
# top5 = df.nlargest(5, "exam_score")
# print(top5[["student_id", "exam_score", "study_hours", "grade"]])
#
# Exercise 2:
# df = pd.read_csv("student_analysis.csv")
# grouped = df.groupby("grade")[["study_hours", "sleep_hours", "attendance"]].mean()
# print(grouped.round(1).sort_index())
#
# Exercise 3:
# df = pd.read_csv("student_analysis.csv")
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
# ax1.hist(df["exam_score"], bins=15, color="#4CAF50", edgecolor="white")
# ax1.set_title("Exam Score Distribution")
# ax1.set_xlabel("Score")
# ax2.scatter(df["study_hours"], df["exam_score"], alpha=0.5, c="#2196F3")
# ax2.set_title("Study Hours vs Score")
# ax2.set_xlabel("Study Hours")
# ax2.set_ylabel("Exam Score")
# plt.tight_layout()
# plt.savefig("analysis_plots.png")
# plt.close()
#
# Exercise 4:
# def data_quality_report(df):
#     report = {}
#     for col in df.columns:
#         report[col] = {
#             "dtype": str(df[col].dtype),
#             "missing": int(df[col].isnull().sum()),
#             "unique": int(df[col].nunique()),
#         }
#     return report
# import json
# print(json.dumps(data_quality_report(dataset), indent=2))


# === KEY TAKEAWAYS ============================================================
#
# - pandas is the standard library for tabular data in Python
# - DataFrames are 2D tables with labeled rows and columns
# - Select columns with df["col"], rows with df.iloc[] or df.loc[]
# - Filter with boolean conditions: df[df["col"] > value]
# - GroupBy is essential for aggregating data by categories
# - Handle missing data with fillna() or dropna()
# - matplotlib creates static charts: bar, line, scatter, histogram
# - Always inspect data first: shape, dtypes, describe(), isnull()
# - Save results with to_csv() and plt.savefig()


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (18_practical_python.py), you will learn how to organize
# all of these skills into real projects: project structure, file paths,
# reading and writing files, and splitting code into modules. This is what
# separates scripts from production-ready code.
