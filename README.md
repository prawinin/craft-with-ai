# 🐍 Python for AI — The Complete Beginner Course

A hands-on, file-by-file Python course designed to take you from **zero programming
experience** to writing real AI-ready code. Every lesson is a runnable `.py` file
with an interactive tutor that guides you through concepts, runs code live, and
gives you hands-on practice.

---

## 🚀 Quick Start (Absolute Beginners)

**No setup knowledge required!** Just download this project and run the starter
script for your operating system. It handles everything automatically.

### Linux
```bash
# Make it executable (only needed once)
chmod +x start_linux.sh

# Run it!
./start_linux.sh
```

### macOS
```bash
# Make it executable (only needed once)
chmod +x start_mac.sh

# Run it!
./start_mac.sh
```

### Windows
```
Double-click start_windows.bat
```

> **That's it!** The starter script will automatically check for Python, create
> an isolated environment, install dependencies, and launch the interactive
> course tutor. You don't need to know what any of that means — just run it.

---

## 🎓 The Interactive Course Tutor

This course comes with a **professional interactive tutor** that runs in your
terminal. It's not just a script — it's a complete learning environment:

- **📖 Beautiful lesson rendering** — Theory sections displayed in styled panels
- **💻 Syntax-highlighted code** — Every code example shown with colors and line numbers
- **▶️ Live code execution** — Watch code run and see output in real time
- **🐍 Interactive Python shell** — Practice writing code yourself at any point
- **📊 Progress tracking** — Your completion is saved between sessions
- **🏋️ Guided exercises** — Practice problems with hidden solutions
- **💡 Encouragement** — Your tutor cheers you on as you learn!

To launch the tutor directly (if you already have Python + dependencies):
```bash
python course_runner.py
```

---

## 👋 Who This Is For

- **Complete beginners** who have never written a line of code.
- People who know another language and want to learn Python fast.
- Anyone preparing to work with **AI, machine learning, or data science**.

No prior programming knowledge is assumed. Every concept is explained from scratch
with real-world analogies before any code is shown.

---

## 📚 Table of Contents

| # | File | Topic | What You Will Learn |
|---|------|-------|---------------------|
| 00 | `00_getting_started.py` | 🚀 Getting Started | What Python is, how code runs, your first mental model |
| 01 | `01_hello_world.py` | 👋 Hello World | The print function, running code, basic output |
| 02 | `02_variables.py` | 📦 Variables & Comments | Storing data, naming rules, writing comments |
| 03 | `03_data_types.py` | 🔢 Data Types | Numbers, strings, booleans, type checking, type conversion |
| 04 | `04_operators.py` | ➕ Operators | Arithmetic, comparison, logical, assignment operators |
| 05 | `05_string_manipulation.py` | 📝 String Manipulation | f-strings, methods, slicing, searching, formatting |
| 06 | `06_if_statements.py` | 🔀 If Statements | Conditions, elif chains, nested logic, real decision-making |
| 07 | `07_loops.py` | 🔁 Loops | for loops, while loops, range, break, continue, enumerate |
| 08 | `08_lists.py` | 📋 Lists | Creating, indexing, slicing, modifying, list comprehensions |
| 09 | `09_dictionaries.py` | 🗂️ Dictionaries | Key-value pairs, nesting, iteration, real-world modeling |
| 10 | `10_tuples.py` | 🔒 Tuples | Immutability, unpacking, when to use tuples vs lists |
| 11 | `11_sets.py` | 🎯 Sets | Uniqueness, set operations, practical deduplication |
| 12 | `12_functions_basics.py` | ⚙️ Functions — Basics | Defining, calling, scope, why functions exist |
| 13 | `13_functions_parameters.py` | 🎛️ Functions — Parameters | Positional, keyword, default, flexible argument patterns |
| 14 | `14_functions_return_values.py` | ↩️ Functions — Return Values | return vs print, multiple returns, building reusable tools |
| 15 | `15_packages_and_modules.py` | 📦 Packages & Modules | import, pip, standard library, third-party packages |
| 16 | `16_working_with_apis.py` | 🌐 Working with APIs | HTTP requests, JSON, building a weather dashboard |
| 17 | `17_working_with_data.py` | 📊 Working with Data | pandas DataFrames, matplotlib charts, CSV files |
| 18 | `18_practical_python.py` | 🏗️ Practical Python | Project structure, file paths, reading/writing files |

---

## 📖 Two Ways to Learn

### Option A: Interactive Tutor (Recommended for Beginners)

Use the course runner — it walks you through each lesson step by step, executes
code for you, and provides an interactive shell for practice:

```bash
# Use a starter script (handles everything):
./start_linux.sh     # Linux
./start_mac.sh       # macOS
start_windows.bat    # Windows

# Or run directly (if Python is set up):
python course_runner.py
```

### Option B: VS Code Interactive Window (For Developers)

If you prefer VS Code, you can open any `.py` file and step through it manually
using the Interactive Window:

1. Open a `.py` file in VS Code
2. Select a block of code (or place your cursor on a line)
3. Press `Shift+Enter`
4. See the result in the Interactive Window panel

This requires the Python extension and `ipykernel` (see **Manual Setup** below).

---

## 🛠️ Manual Setup (Advanced)

If you prefer to set things up yourself rather than using the starter scripts:

### Step 1: Install Python

#### Linux (Ubuntu / Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### Linux (Fedora / RHEL)
```bash
sudo dnf install python3 python3-pip
```

#### Windows
1. Go to https://www.python.org/downloads/
2. Download the latest Python 3.x installer.
3. **CRITICAL**: Check the box **"Add Python to PATH"** during installation.
4. Click "Install Now".

#### macOS
```bash
# Using Homebrew (recommended):
brew install python3

# Or download the .pkg installer from https://www.python.org/downloads/
```

### Step 2: Install VS Code (Optional)

1. Download from https://code.visualstudio.com/
2. Install the **Python extension** (search "Python" in Extensions, by Microsoft).

### Step 3: Set Up the Project

```bash
# Clone or download this repository, then:

# Create a virtual environment (reuses globally installed packages):
python3 -m venv --system-site-packages .venv    # Linux / macOS
python -m venv --system-site-packages .venv     # Windows

# Activate it:
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\activate          # Windows

# Install dependencies:
pip install -r requirements.txt
```

### Step 4: Run the Course

```bash
python course_runner.py
```

---

## 🤖 Why Python for AI?

Python is the dominant language in artificial intelligence, machine learning,
and data science. Not because it is the fastest language, but because:

- **Massive ecosystem**: NumPy, pandas, scikit-learn, TensorFlow, PyTorch,
  LangChain — all Python-first.
- **Readable syntax**: Python reads almost like English, so you focus on
  the problem, not the language.
- **Community**: The largest AI/ML developer community. Every tutorial, every
  paper implementation, every API wrapper — Python first.
- **Rapid prototyping**: Go from idea to working prototype in hours, not days.

Every concept in this course is taught with AI applications in mind.

---

## 📋 Requirements

- Python 3.8 or higher
- Terminal/Command Prompt
- Dependencies (auto-installed by starter scripts):
  ```
  rich          — Beautiful terminal UI
  requests      — HTTP requests (lesson 16)
  pandas        — Data manipulation (lesson 17)
  matplotlib    — Charts and plots (lesson 17)
  ipykernel     — VS Code Interactive Window (optional)
  ```

---

## 🙏 Credits

This course was originally inspired by the excellent
[Python for AI Beginner Course](https://python.datalumina.com/) by
[Dave Ebbelaar](https://www.youtube.com/@daveebbelaar) at Data Lumina.
Video lecture: https://youtu.be/ygXn5nV5qFc

The material has been significantly expanded with additional explanations,
real-world examples, exercises, and topics beyond the original curriculum
to create a comprehensive, standalone learning resource.

---

## 📄 License

**CC BY-NC-ND 4.0** © 2026 [Prawin Kumar](https://github.com/prawinin)

- ✅ **Learn freely** — use this for personal education
- ✅ **Share** — redistribute the original, unmodified material
- 🚫 **No commercial use** — do not sell, monetize, or use in paid courses
- 🚫 **No derivatives** — do not rebrand or claim as your own

See [LICENSE](LICENSE) for full terms.
