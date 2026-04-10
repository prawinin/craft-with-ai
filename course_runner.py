# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

#!/usr/bin/env python3
"""
===============================================================================
  PYTHON FOR AI — Interactive Course Runner
  A professional terminal-based tutor powered by the Rich library.
===============================================================================

  This is a self-contained interactive tutor that reads through each lesson
  file, renders explanations as beautifully formatted text, syntax-highlights
  code, executes it live, and provides an interactive REPL for practice.

  Just run:  python course_runner.py

  The starter scripts (start_linux.sh, start_mac.sh, start_windows.bat)
  handle all setup automatically.

===============================================================================
"""

import os
import sys
import glob
import json
import time
import textwrap
import re
import shutil

# ---------------------------------------------------------------------------
# Dependency check — install Rich automatically if missing
# ---------------------------------------------------------------------------
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.syntax import Syntax
    from rich.text import Text
    from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
    from rich.markdown import Markdown
    from rich.align import Align
    from rich.columns import Columns
    from rich.rule import Rule
    from rich.live import Live
    from rich.style import Style
    from rich import box
except ImportError:
    print("\n⏳  Installing the Rich library for beautiful terminal output...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "-q"])
    print("✅  Rich installed!\n")
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.syntax import Syntax
    from rich.text import Text
    from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
    from rich.markdown import Markdown
    from rich.align import Align
    from rich.columns import Columns
    from rich.rule import Rule
    from rich.live import Live
    from rich.style import Style
    from rich import box

# ---------------------------------------------------------------------------
# Console Setup
# ---------------------------------------------------------------------------
console = Console()
TERM_WIDTH = shutil.get_terminal_size().columns

# ---------------------------------------------------------------------------
# Color Palette — Deep, vibrant, modern
# ---------------------------------------------------------------------------
ACCENT       = "#6C63FF"   # Purple accent (primary)
ACCENT2      = "#00D9FF"   # Cyan accent (secondary)
SUCCESS      = "#00E676"   # Green
WARNING      = "#FFD740"   # Amber
DANGER       = "#FF5252"   # Red
MUTED        = "#6B7280"   # Gray
TEXT_PRIMARY  = "#F1F5F9"  # Almost white
TEXT_SECONDARY= "#94A3B8"  # Slate gray
BG_PANEL     = "#1E293B"   # Dark slate for panels

# Section-specific colors
THEORY_COLOR   = "#00D9FF"  # Cyan panels for theory
CODE_COLOR     = "#A78BFA"  # Purple for code
EXERCISE_COLOR = "#FFD740"  # Amber for exercises
SOLUTION_COLOR = "#00E676"  # Green for solutions
TAKEAWAY_COLOR = "#6C63FF"  # Purple accent for takeaways

# ---------------------------------------------------------------------------
# Paths & Constants
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRESS_FILE = os.path.join(BASE_DIR, ".course_progress.json")

# ---------------------------------------------------------------------------
# Course integrity & attribution verification
# ---------------------------------------------------------------------------
_WATERMARK = [80, 114, 97, 119, 105, 110]  # author identity
_SIG_FILE = [76, 73, 67, 69, 78, 83, 69]   # license file
_SIG_HDR = [67, 111, 112, 121, 114, 105, 103, 104, 116]  # copyright marker

def _resolve(seq):
    return ''.join(chr(c) for c in seq)

def _verify_course_files(lesson_paths):
    """Internal validation of course material attribution.
    
    This ensures the educational content maintains proper credit to the
    original author as required by the CC BY-NC-ND 4.0 license.
    """
    _author = _resolve(_WATERMARK)
    _lic = _resolve(_SIG_FILE)
    _hdr = _resolve(_SIG_HDR)
    
    # Check 1: License file exists and attributes the author
    _lpath = os.path.join(BASE_DIR, _lic)
    if not os.path.exists(_lpath):
        return False, "license"
    try:
        with open(_lpath, 'r', encoding='utf-8') as _f:
            _lc = _f.read()
        if _author not in _lc:
            return False, "license"
    except Exception:
        return False, "license"
    
    # Check 2: Lesson files maintain attribution headers
    _checked = 0
    for _fp in lesson_paths:
        try:
            with open(_fp, 'r', encoding='utf-8') as _f:
                _head = _f.read(400)
            if _hdr.lower() in _head.lower() and _author in _head:
                _checked += 1
        except Exception:
            continue
    
    if _checked < max(1, len(lesson_paths) // 2):
        return False, "headers"
    
    # Check 3: Course runner itself has attribution
    try:
        with open(__file__, 'r', encoding='utf-8') as _f:
            _self = _f.read(500)
        if _author not in _self:
            return False, "runner"
    except Exception:
        return False, "runner"
    
    return True, "ok"

def _on_integrity_failure(_reason):
    """Handle integrity verification failure."""
    _a = _resolve(_WATERMARK)
    console.print()
    console.print(
        Panel(
            Align.center(
                Text.from_markup(
                    f"[bold {DANGER}]⚠️  Course Integrity Check Failed[/]\n\n"
                    f"[{TEXT_PRIMARY}]This course was created by [bold]{_a} Kumar[/] and is\n"
                    f"licensed under CC BY-NC-ND 4.0.\n\n"
                    f"The course files appear to have been modified in a way\n"
                    f"that removes or alters the original attribution.\n\n"
                    f"[{WARNING}]To use this course, please download the original\n"
                    f"unmodified version from the author's repository.[/]\n\n"
                    f"[dim]Reason: {_reason} verification failed[/]"
                )
            ),
            border_style=DANGER,
            padding=(1, 4),
            title=f"[bold {DANGER}]🔒 Attribution Required[/]",
        )
    )
    console.print()
    sys.exit(1)


# Lesson metadata (difficulty, estimated time)
LESSON_META = {
    "00_getting_started.py":        {"difficulty": "Beginner",      "time": "15 min", "emoji": "🚀"},
    "01_hello_world.py":            {"difficulty": "Beginner",      "time": "15 min", "emoji": "👋"},
    "02_variables.py":              {"difficulty": "Beginner",      "time": "20 min", "emoji": "📦"},
    "03_data_types.py":             {"difficulty": "Beginner",      "time": "25 min", "emoji": "🔢"},
    "04_operators.py":              {"difficulty": "Beginner",      "time": "25 min", "emoji": "➕"},
    "05_string_manipulation.py":    {"difficulty": "Beginner",      "time": "25 min", "emoji": "📝"},
    "06_if_statements.py":          {"difficulty": "Beginner",      "time": "25 min", "emoji": "🔀"},
    "07_loops.py":                  {"difficulty": "Beginner",      "time": "25 min", "emoji": "🔁"},
    "08_lists.py":                  {"difficulty": "Intermediate",  "time": "25 min", "emoji": "📋"},
    "09_dictionaries.py":           {"difficulty": "Intermediate",  "time": "25 min", "emoji": "🗂️"},
    "10_tuples.py":                 {"difficulty": "Intermediate",  "time": "20 min", "emoji": "🔒"},
    "11_sets.py":                   {"difficulty": "Intermediate",  "time": "20 min", "emoji": "🎯"},
    "12_functions_basics.py":       {"difficulty": "Intermediate",  "time": "25 min", "emoji": "⚙️"},
    "13_functions_parameters.py":   {"difficulty": "Intermediate",  "time": "25 min", "emoji": "🎛️"},
    "14_functions_return_values.py": {"difficulty": "Intermediate", "time": "25 min", "emoji": "↩️"},
    "15_packages_and_modules.py":   {"difficulty": "Intermediate",  "time": "25 min", "emoji": "📦"},
    "16_working_with_apis.py":      {"difficulty": "Advanced",      "time": "30 min", "emoji": "🌐"},
    "17_working_with_data.py":      {"difficulty": "Advanced",      "time": "30 min", "emoji": "📊"},
    "18_practical_python.py":       {"difficulty": "Advanced",      "time": "30 min", "emoji": "🏗️"},
}

DIFFICULTY_COLORS = {
    "Beginner":     SUCCESS,
    "Intermediate": WARNING,
    "Advanced":     DANGER,
}

# Encouraging messages shown randomly
ENCOURAGEMENTS = [
    "You're doing great! Keep going! 💪",
    "Every expert was once a beginner. 🌱",
    "This is how programmers learn — one step at a time. 🚶",
    "You're building real skills right now. 🔧",
    "Coffee break? You've earned it! ☕",
    "Fun fact: Python was named after Monty Python, not the snake! 🐍",
    "AI engineers write code just like this. You're on your way! 🤖",
    "The best way to learn is by doing. Keep experimenting! 🧪",
    "Mistakes are not failures — they're lessons. 🎓",
    "You're further than you were yesterday! 📈",
]

# ---------------------------------------------------------------------------
# ASCII Art Logo
# ---------------------------------------------------------------------------
LOGO = r"""
[bold #6C63FF]
    ____        __  __                     ____              ___    ____
   / __ \__  __/ /_/ /_  ____  ____       / __/___  _____   /   |  /  _/
  / /_/ / / / / __/ __ \/ __ \/ __ \     / /_/ __ \/ ___/  / /| |  / /
 / ____/ /_/ / /_/ / / / /_/ / / / /    / __/ /_/ / /     / ___ |_/ /
/_/    \__, /\__/_/ /_/\____/_/ /_/    /_/  \____/_/     /_/  |_/___/
      /____/
[/]
"""

LOGO_SMALL = r"""[bold #6C63FF]
 ╔═══════════════════════════════════════╗
 ║     🐍  Python for AI  🤖            ║
 ║     The Complete Beginner Course      ║
 ╚═══════════════════════════════════════╝[/]"""


# ==========================================================================
# PROGRESS MANAGEMENT
# ==========================================================================

def load_progress() -> dict:
    """Load progress from disk. Returns a dict with completed lessons, student name, stats."""
    default = {
        "student_name": "",
        "completed": [],
        "current_streak": 0,
        "total_time_minutes": 0,
        "last_session": "",
        "sessions_count": 0,
    }
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                data = json.load(f)
                # Handle old format (list)
                if isinstance(data, list):
                    default["completed"] = data
                    return default
                # Merge with defaults for new fields
                for key in default:
                    if key not in data:
                        data[key] = default[key]
                return data
        except (json.JSONDecodeError, KeyError):
            return default
    return default


def save_progress(progress: dict):
    """Persist progress to disk."""
    progress["last_session"] = time.strftime("%Y-%m-%d %H:%M")
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


# ==========================================================================
# LESSON DISCOVERY
# ==========================================================================

def discover_lessons() -> list:
    """Find all numbered lesson files, sorted by number."""
    pattern = os.path.join(BASE_DIR, "[0-1][0-9]_*.py")
    lessons = sorted(glob.glob(pattern))
    return lessons


# ==========================================================================
# LESSON PARSER
# ==========================================================================

def extract_lesson_title(filepath: str) -> str:
    """Pull the lesson title from the docstring header."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read(1000)
    match = re.search(r'Lesson \d+:\s*(.+)', content)
    if match:
        return match.group(1).strip()
    # Fallback: derive from filename
    name = os.path.basename(filepath).replace('.py', '')
    parts = name.split('_', 1)
    if len(parts) == 2:
        return parts[1].replace('_', ' ').title()
    return name


def parse_lesson(filepath: str) -> dict:
    """Parse a lesson file into structured sections.

    Returns a dict with:
        - intro: str (the docstring content)
        - sections: list of dicts, each with:
            - title: str
            - type: str (theory, exercise, solution, takeaway, next)
            - comments: list[str] (reading material)
            - code: str (executable code)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by the section delimiter
    raw_sections = content.split('# ===')

    # First section is the docstring intro
    intro_raw = raw_sections[0].strip()
    intro = intro_raw.replace('"""', '').strip()

    sections = []
    for raw in raw_sections[1:]:
        lines = raw.split('\n')
        # Title is the first line after the delimiter, stripped of '=' and whitespace
        title = lines[0].replace('=', '').strip()

        # Determine section type
        title_upper = title.upper()
        if "EXERCISE" in title_upper:
            sec_type = "exercise"
        elif "SOLUTION" in title_upper:
            sec_type = "solution"
        elif "TAKEAWAY" in title_upper or "KEY CONCEPT" in title_upper:
            sec_type = "takeaway"
        elif "NEXT" in title_upper or "WHAT'S NEXT" in title_upper:
            sec_type = "next"
        elif "COMMON MISTAKE" in title_upper:
            sec_type = "warning"
        elif "REAL-WORLD" in title_upper or "REAL WORLD" in title_upper:
            sec_type = "realworld"
        else:
            sec_type = "theory"

        comments = []
        code_lines = []

        # Separate comments (reading material) from code
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith('#'):
                text = line.lstrip()[1:]  # Remove the leading #
                if text.startswith(' '):
                    text = text[1:]  # Remove the space after #
                comments.append(text)
            else:
                if stripped or code_lines:
                    code_lines.append(line)

        code_str = '\n'.join(code_lines).strip()

        sections.append({
            "title": title,
            "type": sec_type,
            "comments": comments,
            "code": code_str,
        })

    return {
        "intro": intro,
        "sections": sections,
    }


# ==========================================================================
# SAFE INTERACTIVE REPL
# ==========================================================================

def safe_repl(env: dict, banner: str = ""):
    """Run an interactive Python REPL that won't crash the tutor on exit().

    The built-in code.interact() uses SystemExit to leave, which can
    propagate and kill the entire course runner. This custom REPL
    catches exit()/quit() gracefully.
    """
    import code as code_module
    import codeop

    if banner:
        print(banner)

    compiler = codeop.CommandCompiler()
    buffer = []

    while True:
        try:
            prompt = "... " if buffer else ">>> "
            try:
                line = input(prompt)
            except EOFError:
                print()
                break

            # Check for exit commands
            stripped = line.strip()
            if stripped in ('exit()', 'quit()', 'exit', 'quit'):
                print("  Returning to lesson...\n")
                break

            buffer.append(line)
            source = "\n".join(buffer)

            try:
                compiled = compiler(source, "<interactive>")
            except (SyntaxError, OverflowError, ValueError) as e:
                buffer = []
                # Display the error like a normal Python REPL
                import traceback
                traceback.print_exception(type(e), e, None)
                continue

            if compiled is None:
                # Incomplete input — need more lines
                continue

            # Complete input — execute it
            buffer = []
            try:
                exec(compiled, env)
            except SystemExit:
                print("  Returning to lesson...\n")
                break
            except Exception:
                import traceback
                traceback.print_exc()

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            buffer = []


# ==========================================================================
# DISPLAY HELPERS
# ==========================================================================

def clear_screen():
    """Clear the terminal for a clean experience."""
    os.system('cls' if os.name == 'nt' else 'clear')


def typing_effect(text: str, style: str = "", delay: float = 0.008):
    """Print text with a subtle typing animation. Press Enter to skip."""
    # Use Rich for styled text but character-by-character
    styled = Text(text, style=style)
    try:
        for i in range(len(text)):
            console.print(Text(text[i], style=style), end="")
            time.sleep(delay)
        console.print()  # newline at end
    except KeyboardInterrupt:
        # User wants to skip — print the rest immediately
        console.print(Text(text[i:], style=style))


def render_section_header(title: str, sec_type: str):
    """Render a beautiful section header based on type."""
    type_config = {
        "theory":    {"emoji": "📖", "color": THEORY_COLOR,   "label": "CONCEPT"},
        "exercise":  {"emoji": "🏋️",  "color": EXERCISE_COLOR, "label": "EXERCISE"},
        "solution":  {"emoji": "💡", "color": SOLUTION_COLOR, "label": "SOLUTION"},
        "takeaway":  {"emoji": "🧠", "color": TAKEAWAY_COLOR, "label": "KEY TAKEAWAYS"},
        "next":      {"emoji": "➡️",  "color": ACCENT2,        "label": "UP NEXT"},
        "warning":   {"emoji": "⚠️",  "color": WARNING,        "label": "WATCH OUT"},
        "realworld": {"emoji": "🌍", "color": ACCENT,         "label": "REAL WORLD"},
    }

    config = type_config.get(sec_type, type_config["theory"])
    emoji = config["emoji"]
    color = config["color"]
    label = config["label"]

    header_text = f"{emoji}  {title}"
    console.print()
    console.print(
        Rule(header_text, style=color, align="center"),
    )
    console.print(
        Align.center(Text(f"[ {label} ]", style=f"dim {color}")),
    )
    console.print()


def render_reading_material(comments: list, sec_type: str):
    """Render the reading/comment material as a styled panel."""
    if not comments:
        return

    text = '\n'.join(comments).strip()
    if not text:
        return

    type_colors = {
        "theory":    THEORY_COLOR,
        "exercise":  EXERCISE_COLOR,
        "solution":  SOLUTION_COLOR,
        "takeaway":  TAKEAWAY_COLOR,
        "next":      ACCENT2,
        "warning":   WARNING,
        "realworld": ACCENT,
    }

    color = type_colors.get(sec_type, THEORY_COLOR)

    # For long reading material, wrap in a panel
    panel = Panel(
        Text(text, style=TEXT_PRIMARY),
        border_style=color,
        padding=(1, 2),
        expand=True,
    )
    console.print(panel)


def render_code_block(code_str: str):
    """Display code with beautiful syntax highlighting."""
    if not code_str:
        return

    syntax = Syntax(
        code_str,
        "python",
        theme="monokai",
        line_numbers=True,
        padding=1,
        word_wrap=True,
    )

    panel = Panel(
        syntax,
        title="[bold #A78BFA]💻 Code[/]",
        border_style="#A78BFA",
        expand=True,
    )
    console.print(panel)


def render_output(output_text: str):
    """Display execution output in a styled panel."""
    panel = Panel(
        Text(output_text, style="white"),
        title=f"[bold {SUCCESS}]▶ Output[/]",
        border_style=SUCCESS,
        padding=(0, 2),
        expand=True,
    )
    console.print(panel)


def wait_for_enter(message: str = "Press [bold cyan]ENTER[/] to continue..."):
    """Display a styled prompt and wait for Enter."""
    console.print()
    console.input(f"  [dim]{message}[/] ")


def get_encouragement() -> str:
    """Return a random encouragement message."""
    import random
    return random.choice(ENCOURAGEMENTS)


# ==========================================================================
# WELCOME SCREEN
# ==========================================================================

def show_welcome_screen(progress: dict, lessons: list):
    """Display the beautiful welcome/landing screen."""
    clear_screen()

    # Logo
    term_cols = shutil.get_terminal_size().columns
    if term_cols >= 75:
        console.print(LOGO)
    else:
        console.print(LOGO_SMALL)

    # Tagline
    console.print(
        Align.center(
            Text("Master Python. Build AI. Change the World.", style=f"italic {TEXT_SECONDARY}")
        )
    )
    console.print()

    # Student greeting
    name = progress.get("student_name", "")
    completed_count = len(progress.get("completed", []))
    total_lessons = len(lessons)
    pct = int((completed_count / total_lessons) * 100) if total_lessons > 0 else 0

    if name:
        greeting = f"Welcome back, [bold {ACCENT}]{name}[/]! 👋"
    else:
        greeting = f"Welcome, [bold {ACCENT}]learner[/]! 👋"

    console.print(Align.center(Text.from_markup(greeting)))
    console.print()

    # Stats row
    stats_table = Table(show_header=False, box=None, padding=(0, 3), expand=False)
    stats_table.add_column(justify="center")
    stats_table.add_column(justify="center")
    stats_table.add_column(justify="center")
    stats_table.add_column(justify="center")

    stats_table.add_row(
        f"[bold {SUCCESS}]{completed_count}[/]\n[dim]Completed[/]",
        f"[bold {WARNING}]{total_lessons - completed_count}[/]\n[dim]Remaining[/]",
        f"[bold {ACCENT}]{pct}%[/]\n[dim]Progress[/]",
        f"[bold {ACCENT2}]{progress.get('sessions_count', 0)}[/]\n[dim]Sessions[/]",
    )
    console.print(Align.center(stats_table))

    # Progress bar
    console.print()
    filled = int((pct / 100) * 40)
    empty = 40 - filled
    bar = f"[{SUCCESS}]{'█' * filled}[/][dim]{'░' * empty}[/]"
    console.print(Align.center(Text.from_markup(f"  {bar}  {pct}%")))
    console.print()


# ==========================================================================
# ONBOARDING (First Run)
# ==========================================================================

def onboarding() -> dict:
    """First-run experience — ask for the student's name."""
    clear_screen()

    term_cols = shutil.get_terminal_size().columns
    if term_cols >= 75:
        console.print(LOGO)
    else:
        console.print(LOGO_SMALL)

    console.print()
    console.print(
        Panel(
            Align.center(
                Text.from_markup(
                    f"[bold {ACCENT}]Welcome to Python for AI![/]\n\n"
                    f"[{TEXT_PRIMARY}]This is an interactive course that will take you from\n"
                    f"absolute zero to writing real AI-ready Python code.\n\n"
                    f"Every lesson is taught step-by-step with explanations,\n"
                    f"live code execution, and hands-on exercises.\n\n"
                    f"[{TEXT_SECONDARY}]No prior programming experience needed.[/]"
                )
            ),
            border_style=ACCENT,
            padding=(1, 4),
            title=f"[bold {ACCENT2}]🎓 Your Journey Starts Here[/]",
        )
    )

    console.print()
    name = console.input(
        f"  [{ACCENT2}]What's your name? (so I can address you personally): [/]"
    ).strip()

    if not name:
        name = "Learner"

    console.print()
    console.print(
        Align.center(
            Text.from_markup(
                f"[bold {SUCCESS}]Awesome, {name}! Let's begin your Python journey! 🚀[/]"
            )
        )
    )
    time.sleep(1.5)

    progress = load_progress()
    progress["student_name"] = name
    progress["sessions_count"] = 1
    save_progress(progress)
    return progress


# ==========================================================================
# MAIN MENU
# ==========================================================================

def show_main_menu(lessons: list, progress: dict) -> str:
    """Display the lesson selection menu. Returns user choice."""
    completed = set(progress.get("completed", []))
    name = progress.get("student_name", "Learner")

    show_welcome_screen(progress, lessons)

    # Build lesson table
    table = Table(
        title=f"[bold {ACCENT}]📚 Course Lessons[/]",
        box=box.ROUNDED,
        border_style=ACCENT,
        show_lines=False,
        padding=(0, 1),
        expand=True,
        header_style=f"bold {ACCENT2}",
    )

    table.add_column("#", justify="center", width=4, style=f"bold {ACCENT}")
    table.add_column("", width=3)  # Status
    table.add_column("Lesson", min_width=35, ratio=1)
    table.add_column("Difficulty", justify="center", width=16)
    table.add_column("Time", justify="center", width=10, style=TEXT_SECONDARY)

    for i, filepath in enumerate(lessons):
        filename = os.path.basename(filepath)
        title = extract_lesson_title(filepath)
        meta = LESSON_META.get(filename, {"difficulty": "Beginner", "time": "20 min", "emoji": "📖"})

        is_completed = filename in completed
        status = f"[{SUCCESS}]✅[/]" if is_completed else f"[dim]◯[/]"

        diff = meta["difficulty"]
        diff_color = DIFFICULTY_COLORS.get(diff, TEXT_SECONDARY)
        diff_text = f"[{diff_color}]{diff}[/]"

        emoji = meta.get("emoji", "📖")
        lesson_style = f"dim" if is_completed else f"bold {TEXT_PRIMARY}"
        lesson_text = f"[{lesson_style}]{emoji}  {title}[/]"

        table.add_row(
            str(i),
            status,
            lesson_text,
            diff_text,
            meta["time"],
        )

    console.print(table)

    # Bottom navigation
    console.print()
    console.print(
        Align.center(
            Text.from_markup(
                f"[dim]Enter a lesson number to begin  •  "
                f"[bold]r[/] = Reset progress  •  "
                f"[bold]q[/] = Quit[/]"
            )
        )
    )
    console.print()

    choice = console.input(f"  [{ACCENT2}]Select lesson ▸ [/]").strip()
    return choice


# ==========================================================================
# LESSON PLAYER
# ==========================================================================

def play_lesson(filepath: str, progress: dict) -> str:
    """Play through a complete lesson interactively.

    Returns: 'next', 'menu', or 'quit'
    """
    filename = os.path.basename(filepath)
    lesson_data = parse_lesson(filepath)
    name = progress.get("student_name", "Learner")

    # Shared execution environment so variables persist across sections
    env = {"__name__": "__lesson__"}

    total_sections = len(lesson_data["sections"])

    # ----- INTRO SCREEN -----
    clear_screen()

    title = extract_lesson_title(filepath)
    meta = LESSON_META.get(filename, {"difficulty": "Beginner", "time": "20 min", "emoji": "📖"})

    console.print()
    console.print(
        Panel(
            Align.center(
                Text.from_markup(
                    f"[bold {ACCENT} size=20]{meta.get('emoji', '📖')}  {title}[/]\n\n"
                    f"[{TEXT_SECONDARY}]Difficulty: [{DIFFICULTY_COLORS.get(meta['difficulty'], TEXT_SECONDARY)}]{meta['difficulty']}[/]  •  "
                    f"Estimated time: {meta['time']}  •  "
                    f"Sections: {total_sections}[/]"
                )
            ),
            border_style=ACCENT,
            padding=(1, 3),
        )
    )

    # Show intro text
    if lesson_data["intro"]:
        intro_text = lesson_data["intro"]
        # Clean up the intro formatting
        intro_lines = intro_text.split('\n')
        cleaned = []
        for line in intro_lines:
            stripped = line.strip()
            if stripped and not all(c == '=' for c in stripped):
                cleaned.append(stripped)
        display_intro = '\n'.join(cleaned)

        console.print()
        console.print(
            Panel(
                Text(display_intro, style=TEXT_PRIMARY),
                border_style=ACCENT2,
                title=f"[bold {ACCENT2}]About This Lesson[/]",
                padding=(1, 2),
                expand=True,
            )
        )

    wait_for_enter(f"Ready to start, {name}? Press [bold cyan]ENTER[/]...")

    # ----- PLAY SECTIONS -----
    for sec_idx, section in enumerate(lesson_data["sections"]):
        clear_screen()

        # Progress indicator at top
        sec_num = sec_idx + 1
        progress_pct = int((sec_num / total_sections) * 100)
        filled = int((progress_pct / 100) * 30)
        empty = 30 - filled
        progress_bar = f"[{ACCENT}]{'━' * filled}[/][dim]{'╌' * empty}[/]"

        console.print(
            Text.from_markup(
                f"  [{MUTED}]{filename}  [{ACCENT}]Section {sec_num}/{total_sections}[/]  "
                f"{progress_bar}  {progress_pct}%[/]"
            )
        )

        # Section header
        render_section_header(section["title"], section["type"])

        # Handle SOLUTION sections — require confirmation
        if section["type"] == "solution":
            console.print(
                Panel(
                    Align.center(
                        Text.from_markup(
                            f"[bold {WARNING}]⚠️  Spoiler Alert![/]\n\n"
                            f"[{TEXT_SECONDARY}]Make sure you've tried the exercises\n"
                            f"before looking at the solutions.[/]"
                        )
                    ),
                    border_style=WARNING,
                    padding=(1, 2),
                )
            )
            console.print()
            reveal = console.input(
                f"  [{WARNING}]Type [bold]show[/] to reveal solutions, or press [bold]ENTER[/] to skip: [/]"
            ).strip().lower()
            if reveal != "show":
                continue
            clear_screen()
            # Re-render the progress bar and header after clear
            console.print(
                Text.from_markup(
                    f"  [{MUTED}]{filename}  [{ACCENT}]Section {sec_num}/{total_sections}[/]  "
                    f"{progress_bar}  {progress_pct}%[/]"
                )
            )
            render_section_header(section["title"], section["type"])

        # Render reading material
        render_reading_material(section["comments"], section["type"])

        # Render code (if any)
        if section["code"]:
            console.print()
            wait_for_enter("Press [bold cyan]ENTER[/] to see the code...")
            console.print()
            render_code_block(section["code"])
            console.print()

            # Action prompt based on section type
            if section["type"] == "exercise":
                console.print(
                    f"  [{EXERCISE_COLOR}]💡 Try writing the solution yourself![/]"
                )
                console.print()
                action = console.input(
                    f"  [{ACCENT2}]Type [bold]try[/] to open an interactive Python shell, "
                    f"or press [bold]ENTER[/] to continue: [/]"
                ).strip().lower()
            else:
                action = console.input(
                    f"  [{ACCENT2}]Press [bold]ENTER[/] to run this code, "
                    f"type [bold]try[/] for interactive shell, "
                    f"or [bold]skip[/] to skip: [/]"
                ).strip().lower()

            # Execute code
            if action not in ('try', 'skip') and section["type"] != "exercise":
                console.print()
                # Capture output
                import io
                from contextlib import redirect_stdout, redirect_stderr
                stdout_capture = io.StringIO()
                stderr_capture = io.StringIO()
                try:
                    with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                        exec(section["code"], env)
                    output = stdout_capture.getvalue()
                    if output.strip():
                        render_output(output.rstrip())
                    else:
                        console.print(
                            f"  [{MUTED}](Code executed successfully — no visible output)[/]"
                        )
                except Exception as e:
                    error_text = f"Error: {type(e).__name__}: {e}"
                    console.print(
                        Panel(
                            Text(error_text, style="bold red"),
                            title=f"[bold {DANGER}]❌ Error[/]",
                            border_style=DANGER,
                            padding=(0, 2),
                        )
                    )
                console.print()

            # Interactive REPL
            if action == 'try':
                console.print()
                console.print(
                    Panel(
                        Text.from_markup(
                            f"[bold {ACCENT2}]🐍 Interactive Python Shell[/]\n\n"
                            f"[{TEXT_SECONDARY}]All variables from previous sections are available.\n"
                            f"Experiment freely! Type [bold]exit()[/] when you're done.[/]"
                        ),
                        border_style=ACCENT2,
                        padding=(1, 2),
                    )
                )
                console.print()
                safe_repl(
                    env,
                    banner=f"  Python {sys.version.split()[0]} — Interactive Mode\n"
                           f"  Type exit() to return to the lesson.\n"
                )
        else:
            # Section with no code — just reading
            if section["type"] == "exercise":
                console.print()
                action = console.input(
                    f"  [{EXERCISE_COLOR}]Type [bold]try[/] to open a Python shell and practice, "
                    f"or press [bold]ENTER[/] to continue: [/]"
                ).strip().lower()
                if action == 'try':
                    console.print()
                    console.print(
                        Panel(
                            Text.from_markup(
                                f"[bold {ACCENT2}]🐍 Interactive Python Shell[/]\n\n"
                                f"[{TEXT_SECONDARY}]Practice away! Type [bold]exit()[/] when done.[/]"
                            ),
                            border_style=ACCENT2,
                            padding=(1, 2),
                        )
                    )
                    safe_repl(
                        env,
                        banner=f"  Python {sys.version.split()[0]} — Interactive Mode\n"
                    )
            else:
                wait_for_enter()

        # Quick navigation between sections (except last)
        if sec_idx < total_sections - 1:
            console.print()
            nav = console.input(
                f"  [{MUTED}]Press [bold]ENTER[/] for next section, "
                f"[bold]m[/] = menu, [bold]q[/] = quit: [/]"
            ).strip().lower()
            if nav == 'm':
                return 'menu'
            elif nav == 'q':
                return 'quit'

    # ----- LESSON COMPLETE -----
    clear_screen()
    console.print()
    console.print(
        Panel(
            Align.center(
                Text.from_markup(
                    f"[bold {SUCCESS}]🎉  Lesson Complete!  🎉[/]\n\n"
                    f"[{TEXT_PRIMARY}]You have finished:[/]\n"
                    f"[bold {ACCENT}]{meta.get('emoji', '📖')}  {title}[/]\n\n"
                    f"[{TEXT_SECONDARY}]{get_encouragement()}[/]"
                )
            ),
            border_style=SUCCESS,
            padding=(2, 4),
        )
    )

    # Mark as completed
    if filename not in progress.get("completed", []):
        progress.setdefault("completed", []).append(filename)

    completed_count = len(progress.get("completed", []))
    total = len(discover_lessons())
    pct = int((completed_count / total) * 100) if total > 0 else 0

    console.print()
    console.print(
        Align.center(
            Text.from_markup(
                f"  [{SUCCESS}]Course Progress: {completed_count}/{total} lessons ({pct}%)[/]"
            )
        )
    )

    # Progress bar
    filled = int((pct / 100) * 40)
    empty = 40 - filled
    bar = f"[{SUCCESS}]{'█' * filled}[/][dim]{'░' * empty}[/]"
    console.print(Align.center(Text.from_markup(f"  {bar}")))

    save_progress(progress)

    # Navigation
    console.print()
    console.print(
        Panel(
            Align.center(
                Text.from_markup(
                    f"[bold]n[/] → Next lesson  •  "
                    f"[bold]m[/] → Back to menu  •  "
                    f"[bold]q[/] → Quit course"
                )
            ),
            border_style=MUTED,
            padding=(0, 2),
        )
    )
    console.print()

    choice = console.input(f"  [{ACCENT2}]What's next? [bold][n][/]: [/]").strip().lower()
    if choice == 'q':
        return 'quit'
    elif choice == 'm':
        return 'menu'
    return 'next'


# ==========================================================================
# RESET PROGRESS
# ==========================================================================

def reset_progress(progress: dict) -> dict:
    """Reset all progress after confirmation."""
    console.print()
    confirm = console.input(
        f"  [{DANGER}]Are you sure you want to reset ALL progress? "
        f"Type [bold]yes[/] to confirm: [/]"
    ).strip().lower()

    if confirm == "yes":
        name = progress.get("student_name", "")
        progress = load_progress.__wrapped__() if hasattr(load_progress, '__wrapped__') else {
            "student_name": name,
            "completed": [],
            "current_streak": 0,
            "total_time_minutes": 0,
            "last_session": "",
            "sessions_count": progress.get("sessions_count", 0),
        }
        save_progress(progress)
        console.print(f"  [{SUCCESS}]✅ Progress has been reset.[/]")
        time.sleep(1)
    else:
        console.print(f"  [{MUTED}]Reset cancelled.[/]")
        time.sleep(0.5)

    return progress


# ==========================================================================
# FAREWELL
# ==========================================================================

def show_farewell(progress: dict):
    """Display a goodbye message."""
    name = progress.get("student_name", "Learner")
    completed = len(progress.get("completed", []))
    total = len(discover_lessons())

    clear_screen()
    console.print()
    console.print(
        Panel(
            Align.center(
                Text.from_markup(
                    f"[bold {ACCENT}]See you next time, {name}! 👋[/]\n\n"
                    f"[{TEXT_SECONDARY}]Progress saved: {completed}/{total} lessons completed.\n"
                    f"Keep practicing and you'll be writing AI code in no time![/]\n\n"
                    f"[dim italic]\"The only way to learn a new programming language\n"
                    f"is by writing programs in it.\" — Dennis Ritchie[/]"
                )
            ),
            border_style=ACCENT,
            padding=(1, 4),
        )
    )
    console.print()


# ==========================================================================
# COURSE COMPLETE CELEBRATION
# ==========================================================================

def show_course_complete(progress: dict):
    """Celebrate completing the entire course!"""
    name = progress.get("student_name", "Learner")
    clear_screen()

    celebration = r"""
[bold #FFD740]
    ⭐  ⭐  ⭐  ⭐  ⭐  ⭐  ⭐  ⭐  ⭐  ⭐

       🏆  COURSE COMPLETED!  🏆

    ⭐  ⭐  ⭐  ⭐  ⭐  ⭐  ⭐  ⭐  ⭐  ⭐
[/]"""

    console.print(celebration)
    console.print()
    console.print(
        Panel(
            Align.center(
                Text.from_markup(
                    f"[bold {SUCCESS}]Congratulations, {name}! 🎓[/]\n\n"
                    f"[{TEXT_PRIMARY}]You have completed the entire\n"
                    f"[bold]Python for AI[/] course!\n\n"
                    f"You now have the foundation to:\n"
                    f"  • Build AI applications with Python\n"
                    f"  • Work with data using pandas & matplotlib\n"
                    f"  • Use APIs to connect to AI services\n"
                    f"  • Write clean, professional Python code\n\n"
                    f"[{TEXT_SECONDARY}]Your next steps:\n"
                    f"  1. Explore NumPy and scikit-learn\n"
                    f"  2. Build a small AI project\n"
                    f"  3. Learn about neural networks with PyTorch or TensorFlow\n\n"
                    f"  [{ACCENT}]The world of AI is waiting for you![/]"
                )
            ),
            border_style=SUCCESS,
            padding=(2, 4),
            title="[bold #FFD740]🌟 Achievement Unlocked 🌟[/]",
        )
    )
    wait_for_enter()


# ==========================================================================
# MAIN
# ==========================================================================

def main():
    """Main entry point for the course runner."""
    lessons = discover_lessons()

    if not lessons:
        console.print(f"[bold {DANGER}]❌ No lesson files found![/]")
        console.print(f"[{TEXT_SECONDARY}]Make sure the lesson files (00_getting_started.py, etc.) "
                      f"are in the same directory as course_runner.py.[/]")
        sys.exit(1)

    # Load or create progress
    progress = load_progress()

    # Verify course integrity
    _valid, _reason = _verify_course_files(lessons)
    if not _valid:
        _on_integrity_failure(_reason)

    # First-run onboarding
    if not progress.get("student_name"):
        progress = onboarding()
    else:
        # Increment session count
        progress["sessions_count"] = progress.get("sessions_count", 0) + 1
        save_progress(progress)

    # Main loop
    while True:
        choice = show_main_menu(lessons, progress)

        if choice.lower() == 'q':
            show_farewell(progress)
            break
        elif choice.lower() == 'r':
            progress = reset_progress(progress)
            continue

        try:
            lesson_idx = int(choice)
            if lesson_idx < 0 or lesson_idx >= len(lessons):
                console.print(f"  [{WARNING}]Please enter a number between 0 and {len(lessons) - 1}.[/]")
                time.sleep(1)
                continue

            # Play lessons sequentially from chosen index
            while lesson_idx < len(lessons):
                action = play_lesson(lessons[lesson_idx], progress)

                if action == 'menu':
                    break
                elif action == 'quit':
                    show_farewell(progress)
                    return
                elif action == 'next':
                    lesson_idx += 1
                    if lesson_idx >= len(lessons):
                        # Check if all lessons are completed
                        if len(progress.get("completed", [])) >= len(lessons):
                            show_course_complete(progress)
                        else:
                            console.print(
                                f"\n  [{SUCCESS}]That was the last lesson! "
                                f"Return to the menu to revisit any lesson.[/]"
                            )
                            wait_for_enter()
                        break

        except ValueError:
            console.print(f"  [{WARNING}]Please enter a valid lesson number or command.[/]")
            time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n\n  [{MUTED}]Course interrupted. Progress saved. See you next time! 👋[/]\n")
        sys.exit(0)