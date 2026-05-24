# Copyright (c) 2026 Prawin Kumar

# -----------------------------------------------------------------------------
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 - learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# -----------------------------------------------------------------------------

#!/usr/bin/env python3
"""
Craft with AI - Browser Course Runner

This runner launches a local web app and opens it in the default browser.
The browser experience is now the primary learning interface:
- guided syllabus navigation
- beginner-friendly section explanations
- real-life analogies
- search across lessons
- day/night mode
- local progress tracking
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import socket
import subprocess
import sys
import threading
import tempfile
import webbrowser
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Optional
from urllib.parse import parse_qs, urlparse


BASE_DIR = Path(__file__).resolve().parent
PROGRESS_FILE = BASE_DIR / ".course_progress.json"
HOST = "127.0.0.1"
START_PORT = 8765

LESSON_FILE_RE = re.compile(r"^(?P<number>\d{2})_(?P<name>[a-z0-9_]+)\.py$")
SECTION_HEADER_RE = re.compile(r"^#\s*===\s*(.+?)\s*=+\s*$", re.MULTILINE)

LEGACY_HINT_PATTERNS = [
    re.compile(r"shift\+enter", re.IGNORECASE),
    re.compile(r"interactive window", re.IGNORECASE),
    re.compile(r"select code blocks", re.IGNORECASE),
]

RUNNER_FORBIDDEN_NAMES = {
    "__import__",
    "breakpoint",
    "compile",
    "delattr",
    "dir",
    "eval",
    "exec",
    "getattr",
    "globals",
    "help",
    "input",
    "locals",
    "memoryview",
    "open",
    "setattr",
    "vars",
}

RUNNER_SAFE_BUILTINS = {
    "abs",
    "all",
    "any",
    "bool",
    "dict",
    "enumerate",
    "Exception",
    "False",
    "filter",
    "float",
    "int",
    "isinstance",
    "len",
    "list",
    "map",
    "max",
    "min",
    "None",
    "print",
    "range",
    "reversed",
    "round",
    "set",
    "sorted",
    "str",
    "sum",
    "True",
    "tuple",
    "type",
    "ValueError",
    "zip",
}

RUNNER_FORBIDDEN_MODULES = {
    "os",
    "pathlib",
    "requests",
    "shutil",
    "socket",
    "subprocess",
    "sys",
    "tempfile",
    "time",
    "urllib",
}

RUNNER_MAX_SOURCE_CHARS = 8_000
RUNNER_TIMEOUT_SECONDS = 4


LESSON_DEFAULT_META: dict[str, dict[str, str]] = {
    "00_getting_started.py": {"difficulty": "Beginner", "time": "15 min"},
    "01_hello_world.py": {"difficulty": "Beginner", "time": "15 min"},
    "02_variables.py": {"difficulty": "Beginner", "time": "20 min"},
    "03_data_types.py": {"difficulty": "Beginner", "time": "25 min"},
    "04_operators.py": {"difficulty": "Beginner", "time": "25 min"},
    "05_string_manipulation.py": {"difficulty": "Beginner", "time": "25 min"},
    "06_if_statements.py": {"difficulty": "Beginner", "time": "25 min"},
    "07_loops.py": {"difficulty": "Beginner", "time": "25 min"},
    "08_lists.py": {"difficulty": "Intermediate", "time": "25 min"},
    "09_dictionaries.py": {"difficulty": "Intermediate", "time": "25 min"},
    "10_tuples.py": {"difficulty": "Intermediate", "time": "20 min"},
    "11_sets.py": {"difficulty": "Intermediate", "time": "20 min"},
    "12_functions_basics.py": {"difficulty": "Intermediate", "time": "25 min"},
    "13_functions_parameters.py": {"difficulty": "Intermediate", "time": "25 min"},
    "14_functions_return_values.py": {"difficulty": "Intermediate", "time": "25 min"},
    "15_packages_and_modules.py": {"difficulty": "Intermediate", "time": "25 min"},
    "16_working_with_apis.py": {"difficulty": "Advanced", "time": "30 min"},
    "17_working_with_data.py": {"difficulty": "Advanced", "time": "30 min"},
    "18_practical_python.py": {"difficulty": "Advanced", "time": "30 min"},
}

UI_BENCHMARKS = [
    {
        "name": "Codecademy",
        "source": "https://www.codecademy.com/learn/learn-python-3",
        "best_parts": [
            "small guided steps",
            "clear syllabus progression",
            "practice-oriented structure",
        ],
    },
    {
        "name": "Coursera",
        "source": "https://www.coursera.org/specializations/python",
        "best_parts": [
            "outcomes-first course framing",
            "time and difficulty clarity",
            "structured multi-course roadmap",
        ],
    },
    {
        "name": "DataCamp",
        "source": "https://www.datacamp.com/courses/intro-to-python-for-data-science",
        "best_parts": [
            "micro-learning chapters",
            "fast progress feedback",
            "beginner confidence language",
        ],
    },
]

REAL_LIFE_MAP: list[tuple[tuple[str, ...], str]] = [
    (("variables", "data types"), "Like labeling kitchen jars: one jar says rice, one says sugar. Variables are labels, data types are what each jar can hold."),
    (("operators", "math", "calculator", "arithmetic"), "Like using a calculator while budgeting household expenses. Operators tell Python which operation to perform."),
    (("string", "text"), "Like editing a text message before sending it. String methods help you clean, reshape, and check text."),
    (("if", "condition", "control flow"), "Like deciding whether to carry an umbrella: if it might rain, you take it; otherwise, you do not."),
    (("loop", "iteration"), "Like checking attendance for every student in a class, one by one, until everyone is covered."),
    (("list", "array"), "Like a shopping basket where order matters. You can add, remove, and pick items by position."),
    (("dictionary", "key value"), "Like a contacts app: each name (key) maps to a phone number (value)."),
    (("tuple",), "Like a passport number: fixed once created. Tuples store values that should not change."),
    (("set",), "Like a guest list where duplicate names are removed automatically."),
    (("function",), "Like a reusable kitchen recipe. You follow the same steps with different ingredients."),
    (("module", "package"), "Like organizing tools into labeled drawers so you can quickly reuse them in many projects."),
    (("api",), "Like ordering from a restaurant menu: you send a request, and the kitchen returns a response."),
    (("data", "pandas", "csv"), "Like organizing messy paper records into a spreadsheet so patterns become obvious."),
    (("file", "path", "json", "practical"), "Like keeping documents in well-named folders: easy to find, update, and share."),
]


# -----------------------------------------------------------------------------
# Attribution / integrity verification
# -----------------------------------------------------------------------------

_WATERMARK = [80, 114, 97, 119, 105, 110]
_SIG_FILE = [76, 73, 67, 69, 78, 83, 69]
_SIG_HDR = [67, 111, 112, 121, 114, 105, 103, 104, 116]


def _resolve(seq: list[int]) -> str:
    return "".join(chr(c) for c in seq)


def verify_course_integrity(lesson_paths: list[Path]) -> tuple[bool, str]:
    author = _resolve(_WATERMARK)
    lic = _resolve(_SIG_FILE)
    hdr = _resolve(_SIG_HDR)

    lic_path = BASE_DIR / lic
    if not lic_path.exists():
        return False, "license"

    try:
        lic_content = lic_path.read_text(encoding="utf-8")
    except Exception:
        return False, "license"

    if author not in lic_content:
        return False, "license"

    checked = 0
    for lesson_path in lesson_paths:
        try:
            head = lesson_path.read_text(encoding="utf-8")[:500]
        except Exception:
            continue
        if hdr.lower() in head.lower() and author in head:
            checked += 1

    if checked < max(1, len(lesson_paths) // 2):
        return False, "headers"

    try:
        self_head = Path(__file__).read_text(encoding="utf-8")[:500]
    except Exception:
        return False, "runner"

    if author not in self_head:
        return False, "runner"

    return True, "ok"


def print_integrity_failure(reason: str) -> None:
    author = _resolve(_WATERMARK)
    print()
    print("=" * 72)
    print("Course Integrity Check Failed")
    print("=" * 72)
    print(f"This course was created by {author} Kumar and is licensed under CC BY-NC-ND 4.0.")
    print("The files appear to have been modified in a way that removes attribution.")
    print(f"Reason: {reason} verification failed")
    print("Please use the original unmodified course version.")
    print()


# -----------------------------------------------------------------------------
# Lesson parsing
# -----------------------------------------------------------------------------

def discover_lessons() -> list[Path]:
    paths = []
    # Sort module directories: e.g. 01_python_programming, 02_dev_workspace, etc.
    module_dirs = sorted([d for d in BASE_DIR.glob("[0-9][0-9]_[a-zA-Z0-9_]*") if d.is_dir()])
    for module_dir in module_dirs:
        # Sort lesson files inside: 00_*.py, 01_*.py, etc.
        paths.extend(sorted(module_dir.glob("[0-9][0-9]_*.py")))
    # Backwards compatibility fallback to root
    if not paths:
        paths = sorted(BASE_DIR.glob("[0-9][0-9]_*.py"))
    return paths


def slug_from_filename(filename: str) -> str:
    match = LESSON_FILE_RE.match(filename)
    if match:
        number = match.group("number")
        slug_tail = match.group("name").replace("_", "-")
        return f"{number}-{slug_tail}"
    return filename.replace(".py", "").replace("_", "-")


def fallback_title_from_filename(filename: str) -> str:
    stem = filename.replace(".py", "")
    if "_" in stem:
        _, tail = stem.split("_", 1)
    else:
        tail = stem
    return tail.replace("_", " ").title()


def classify_section(title: str) -> str:
    t = title.lower()
    if "exercise" in t:
        return "exercise"
    if "solution" in t:
        return "solution"
    if "takeaway" in t or "key concept" in t:
        return "takeaway"
    if "common mistake" in t or "watch out" in t:
        return "warning"
    if "real-world" in t or "real world" in t:
        return "realworld"
    if "next" in t:
        return "next"
    return "theory"


def should_skip_legacy_line(line: str) -> bool:
    lowered = line.strip().lower()
    return any(pattern.search(lowered) for pattern in LEGACY_HINT_PATTERNS)


def dedupe_text_lines(lines: list[str]) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()

    for raw in lines:
        line = raw.rstrip()
        compact = re.sub(r"\s+", " ", line.strip()).lower()

        if should_skip_legacy_line(compact):
            continue

        if not compact:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue

        if compact in seen and len(compact) > 24:
            continue

        if cleaned:
            prev = re.sub(r"\s+", " ", cleaned[-1].strip()).lower()
            if compact == prev:
                continue

        cleaned.append(line.strip())
        seen.add(compact)

    while cleaned and cleaned[-1] == "":
        cleaned.pop()

    return cleaned


def normalize_code_lines(lines: list[str]) -> list[str]:
    output: list[str] = []
    blank_run = 0

    for line in lines:
        if line.strip():
            output.append(line.rstrip())
            blank_run = 0
        else:
            blank_run += 1
            if blank_run == 1:
                output.append("")

    while output and output[0] == "":
        output.pop(0)
    while output and output[-1] == "":
        output.pop()

    return output


def code_block_id(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:20]


def collect_bound_names(node: ast.AST) -> set[str]:
    names: set[str] = set()

    def visit_target(target: ast.AST) -> None:
        if isinstance(target, ast.Name):
            names.add(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for item in target.elts:
                visit_target(item)

    for child in ast.walk(node):
        if isinstance(child, ast.Assign):
            for target in child.targets:
                visit_target(target)
        elif isinstance(child, ast.AnnAssign):
            visit_target(child.target)
        elif isinstance(child, ast.AugAssign):
            visit_target(child.target)
        elif isinstance(child, ast.For):
            visit_target(child.target)
        elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(child.name)
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in child.args.posonlyargs + child.args.args + child.args.kwonlyargs:
                    names.add(arg.arg)
                if child.args.vararg:
                    names.add(child.args.vararg.arg)
                if child.args.kwarg:
                    names.add(child.args.kwarg.arg)
        elif isinstance(child, ast.ExceptHandler) and child.name:
            names.add(child.name)
        elif isinstance(child, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            for generator in child.generators:
                visit_target(generator.target)
        elif isinstance(child, ast.Import):
            for alias in child.names:
                names.add(alias.asname or alias.name.split(".", 1)[0])
        elif isinstance(child, ast.ImportFrom):
            for alias in child.names:
                names.add(alias.asname or alias.name)

    return names


def find_unbound_reads(tree: ast.AST) -> set[str]:
    bound = collect_bound_names(tree)
    unbound: set[str] = set()

    for node in ast.walk(tree):
        if not isinstance(node, ast.Name) or not isinstance(node.ctx, ast.Load):
            continue
        if node.id in bound or node.id in RUNNER_SAFE_BUILTINS:
            continue
        unbound.add(node.id)

    return unbound


def expression_load_names(node: ast.AST) -> set[str]:
    return {
        child.id
        for child in ast.walk(node)
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load)
    }


def top_level_load_names(node: ast.AST) -> set[str]:
    names: set[str] = set()

    class TopLevelLoadVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            for decorator in node.decorator_list:
                self.visit(decorator)
            for default in node.args.defaults + node.args.kw_defaults:
                if default:
                    self.visit(default)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self.visit_FunctionDef(node)

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            for base in node.bases:
                self.visit(base)
            for keyword in node.keywords:
                self.visit(keyword)
            for decorator in node.decorator_list:
                self.visit(decorator)

        def visit_Name(self, node: ast.Name) -> None:
            if isinstance(node.ctx, ast.Load):
                names.add(node.id)

    TopLevelLoadVisitor().visit(node)
    return names


def has_top_level_return(tree: ast.AST) -> bool:
    return isinstance(tree, ast.Module) and any(isinstance(stmt, ast.Return) for stmt in tree.body)


def has_forward_unbound_top_level_read(tree: ast.AST) -> bool:
    if not isinstance(tree, ast.Module):
        return False

    defined = set(RUNNER_SAFE_BUILTINS)
    for stmt in tree.body:
        reads = top_level_load_names(stmt)
        if any(name not in defined for name in reads):
            return True
        defined.update(collect_bound_names(stmt))

    return False


def has_self_referential_assignment(tree: ast.AST) -> bool:
    assigned: set[str] = set()
    if not isinstance(tree, ast.Module):
        return False

    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            target_names = collect_bound_names(stmt)
            reads = expression_load_names(stmt.value)
            if any(name in reads and name not in assigned for name in target_names):
                return True
            assigned.update(target_names)
        elif isinstance(stmt, ast.AnnAssign):
            target_names = collect_bound_names(stmt)
            reads = expression_load_names(stmt.value) if stmt.value else set()
            if any(name in reads and name not in assigned for name in target_names):
                return True
            assigned.update(target_names)
        elif isinstance(stmt, ast.AugAssign):
            target_names = collect_bound_names(stmt)
            if any(name not in assigned for name in target_names):
                return True
        else:
            assigned.update(collect_bound_names(stmt))

    return False


_SECTION_DIVIDER_PRINT_RE = re.compile(r'^print\s*\(\s*["\'][\s\-–=]+(?:\d+\.)?[A-Z].*["\'][\s\)]*$')


def _is_section_divider_block(source: str) -> bool:
    """Returns True if the block is only print statements acting as section headers or
    ASCII-art pipeline diagrams — pure visual labels with no real computational logic."""
    lines = [l.strip() for l in source.strip().splitlines() if l.strip()]
    if not lines:
        return False
    # All lines must be print calls
    if not all(l.startswith("print(") for l in lines):
        return False
    # All print args must be plain string literals (no variables or expressions)
    all_strings = True
    for l in lines:
        try:
            tree = ast.parse(l)
            for call_node in ast.walk(tree):
                if isinstance(call_node, ast.Call):
                    for arg in call_node.args:
                        if not isinstance(arg, ast.Constant):
                            all_strings = False
                    for kw in call_node.keywords:
                        # sep= and end= keywords are fine (string literal values)
                        if kw.arg not in ("sep", "end") and not isinstance(kw.value, ast.Constant):
                            all_strings = False
        except SyntaxError:
            return False
    if not all_strings:
        return False
    # Qualify as a section divider if any line:
    #  a) Has --- or === section header
    #  b) Has ASCII pipeline arrows (──►, ->, =>)
    #  c) Is a single print of plain text with no meaningful output (e.g. single-line labels)
    has_divider = any(_SECTION_DIVIDER_PRINT_RE.match(l) for l in lines)
    has_pipeline = any(("──►" in l or "-> " in l or "=>" in l) for l in lines)
    # A single isolated print with only a label-like string (no punctuation, no data)
    is_single_label = (
        len(lines) == 1
        and "──►" not in lines[0]
        and _SECTION_DIVIDER_PRINT_RE.match(lines[0])
    )
    return has_divider or has_pipeline or is_single_label


def analyze_runnable_code(source: str) -> tuple[bool, str]:
    stripped = source.strip()
    if not stripped:
        return False, "empty"
    if len(stripped) > RUNNER_MAX_SOURCE_CHARS:
        return False, "large example"

    # Suppress Run button on pure section-divider/pipeline-diagram print blocks
    if _is_section_divider_block(stripped):
        return False, "visual section divider — no interactive logic to run"

    try:
        tree = ast.parse(stripped)
    except SyntaxError:
        return False, "syntax error"

    if has_top_level_return(tree):
        return False, "contains return outside a standalone function example"

    if has_forward_unbound_top_level_read(tree):
        return False, "depends on a variable created earlier in the lesson"

    if has_self_referential_assignment(tree):
        return False, "depends on a variable created earlier in the lesson"

    unbound = find_unbound_reads(tree)
    if unbound:
        names = ", ".join(sorted(unbound)[:4])
        return False, f"depends on earlier lesson state: {names}"

    has_statement = False
    for node in ast.walk(tree):
        if isinstance(node, ast.stmt):
            has_statement = True

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imported = []
            if isinstance(node, ast.Import):
                imported = [alias.name.split(".", 1)[0] for alias in node.names]
            elif node.module:
                imported = [node.module.split(".", 1)[0]]
            if any(name in RUNNER_FORBIDDEN_MODULES for name in imported):
                return False, "uses imports that are better reviewed outside the browser runner"
            return False, "imports are shown as setup, not run inline"

        if isinstance(node, (ast.While, ast.AsyncFunctionDef, ast.Await, ast.Yield, ast.YieldFrom)):
            return False, "uses control flow that can pause or run indefinitely"

        if isinstance(node, ast.Name):
            if node.id in RUNNER_FORBIDDEN_NAMES or "__" in node.id:
                return False, "uses restricted runtime access"

        if isinstance(node, ast.Attribute):
            if node.attr.startswith("_") or "__" in node.attr:
                return False, "uses restricted runtime access"

        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in RUNNER_FORBIDDEN_NAMES:
                return False, "uses restricted runtime access"
            if isinstance(func, ast.Attribute) and func.attr in RUNNER_FORBIDDEN_NAMES:
                return False, "uses restricted runtime access"

    if not has_statement:
        return False, "no runnable statements"

    return True, "safe standalone example"


def extract_prelude_code(module_text: str, first_section_start: int) -> str:
    prelude = module_text[:first_section_start]
    doc_end_line = 0

    try:
        tree = ast.parse(module_text)
    except SyntaxError:
        tree = None

    if tree and tree.body:
        first = tree.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
            doc_end_line = getattr(first, "end_lineno", first.lineno)

    lines = prelude.splitlines()
    setup_lines: list[str] = []
    for idx, raw in enumerate(lines, start=1):
        if idx <= doc_end_line:
            continue

        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue

        setup_lines.append(raw.rstrip())

    return "\n".join(normalize_code_lines(setup_lines)).strip()


def parse_content_blocks(section_body: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    current_text: list[str] = []
    current_code: list[str] = []

    def flush_text() -> None:
        if not current_text:
            return
        content_lines = dedupe_text_lines(current_text)
        text = "\n".join(content_lines).strip()
        if text:
            blocks.append({"type": "text", "content": text})
        current_text.clear()

    def flush_code() -> None:
        if not current_code:
            return
        code_lines = normalize_code_lines(current_code)
        code = "\n".join(code_lines).strip()
        if code:
            blocks.append({"type": "code", "content": code, "is_repeated": False})
        current_code.clear()

    for raw_line in section_body.splitlines():
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("#"):
            flush_code()
            comment = stripped[1:].lstrip()
            current_text.append(comment)
        elif stripped:
            flush_text()
            current_code.append(line.rstrip())
        else:
            if current_code:
                current_code.append("")
            elif current_text:
                current_text.append("")

    flush_text()
    flush_code()

    # Post-process: merge isolated section-divider code blocks into adjacent code blocks.
    # Pattern A: divider → code block → merge divider as header of next code block
    # Pattern B: prev code block → divider → text → merge divider as tail of previous code block
    merged: list[dict[str, Any]] = []
    pending_divider: str | None = None
    for block in blocks:
        if block["type"] == "code" and _is_section_divider_block(block["content"]):
            # Hold this divider — try to prepend it to the next code block
            if pending_divider is not None:
                # Two dividers in a row — attach first to previous code if possible
                if merged and merged[-1]["type"] == "code":
                    prev = dict(merged[-1])
                    prev["content"] = prev["content"] + "\n" + pending_divider
                    merged[-1] = prev
                else:
                    merged.append({"type": "code", "content": pending_divider, "is_repeated": False})
            pending_divider = block["content"]
        else:
            if pending_divider is not None:
                if block["type"] == "code":
                    # Pattern A: prepend divider to next code block
                    block = dict(block)
                    block["content"] = pending_divider + "\n" + block["content"]
                    pending_divider = None
                else:
                    # Pattern B: next is text — append divider to previous code block if any
                    if merged and merged[-1]["type"] == "code":
                        prev = dict(merged[-1])
                        prev["content"] = prev["content"] + "\n" + pending_divider
                        merged[-1] = prev
                    else:
                        merged.append({"type": "code", "content": pending_divider, "is_repeated": False})
                    pending_divider = None
            merged.append(block)
    if pending_divider is not None:
        if merged and merged[-1]["type"] == "code":
            prev = dict(merged[-1])
            prev["content"] = prev["content"] + "\n" + pending_divider
            merged[-1] = prev
        else:
            merged.append({"type": "code", "content": pending_divider, "is_repeated": False})

    return merged



def extract_docstring(module_text: str) -> str:
    try:
        tree = ast.parse(module_text)
    except SyntaxError:
        return ""
    return ast.get_docstring(tree, clean=True) or ""


def extract_bullets(doc_lines: list[str], header: str) -> list[str]:
    bullets: list[str] = []
    in_block = False
    header_lower = header.lower()

    for raw in doc_lines:
        line = raw.strip()
        lower = line.lower()

        if lower.startswith(header_lower):
            in_block = True
            continue

        if not in_block:
            continue

        if line.startswith("-"):
            bullets.append(line.lstrip("- ").strip())
            continue

        if not line:
            if bullets:
                break
            continue

        if line.endswith(":") and bullets:
            break

        if bullets:
            break

    return bullets


def extract_paragraph(doc_lines: list[str], header: str, stop_headers: list[str]) -> str:
    in_block = False
    collected: list[str] = []
    header_lower = header.lower()
    stop_lowers = [item.lower() for item in stop_headers]

    for raw in doc_lines:
        line = raw.strip()
        lower = line.lower()

        if lower.startswith(header_lower):
            in_block = True
            remainder = line[len(header):].strip() if len(line) >= len(header) else ""
            if remainder:
                collected.append(remainder)
            continue

        if not in_block:
            continue

        if any(lower.startswith(stop) for stop in stop_lowers):
            break

        if not line:
            if collected:
                break
            continue

        if set(line) == {"="}:
            continue

        collected.append(line)

    return " ".join(collected).strip()


def build_plain_explanation(section_title: str, text_blob: str) -> str:
    clean = re.sub(r"\s+", " ", text_blob).strip()
    if not clean:
        return f"This section introduces {section_title.lower()} with practical Python examples."

    sentences = re.split(r"(?<=[.!?])\s+", clean)
    selected: list[str] = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        selected.append(sentence)
        if len(" ".join(selected)) > 210 or len(selected) >= 2:
            break

    summary = " ".join(selected).strip()
    if len(summary) > 280:
        summary = summary[:277].rsplit(" ", 1)[0] + "..."
    return summary


def normalize_learning_text(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def is_redundant_explanation(summary: str, text_blob: str) -> bool:
    summary_norm = normalize_learning_text(summary)
    text_norm = normalize_learning_text(text_blob)
    if not summary_norm or not text_norm:
        return False
    return summary_norm in text_norm[: max(220, len(summary_norm) + 80)]


def topic_has_key(topic: str, key: str) -> bool:
    normalized_topic = normalize_learning_text(topic)
    normalized_key = normalize_learning_text(key)
    if not normalized_key:
        return False
    return re.search(rf"(?<![a-z0-9]){re.escape(normalized_key)}(?![a-z0-9])", normalized_topic) is not None


def code_concept_notes(source: str) -> list[str]:
    try:
        tree = ast.parse(source.strip())
    except SyntaxError:
        return []

    notes: list[str] = []

    def add(note: str) -> None:
        if note not in notes and len(notes) < 5:
            notes.append(note)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "print":
                add("`print(...)` sends a value to the screen so you can inspect what the program is doing.")
            elif isinstance(func, ast.Name) and func.id == "type":
                add("`type(...)` asks Python what kind of value you currently have.")
            elif isinstance(func, ast.Name) and func.id in {"int", "float", "str", "bool", "list", "dict", "set", "tuple"}:
                add(f"`{func.id}(...)` converts or builds a value of that type.")

        if isinstance(node, ast.Assign):
            add("`=` stores the value on the right into the variable name on the left.")
        elif isinstance(node, ast.AugAssign):
            add("Operators like `+=` update a variable using its current value.")
        elif isinstance(node, ast.If):
            add("`if` runs a block only when its condition evaluates to `True`.")
        elif isinstance(node, ast.For):
            add("`for` repeats the same block once for each item in a sequence.")
        elif isinstance(node, ast.FunctionDef):
            add("`def` creates a reusable function that can be called later.")
        elif isinstance(node, ast.Return):
            add("`return` sends a result back to the code that called the function.")

        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Add):
                add("`+` adds numbers; with strings, it joins text together.")
            elif isinstance(node.op, ast.Sub):
                add("`-` subtracts the right value from the left value.")
            elif isinstance(node.op, ast.Mult):
                add("`*` multiplies numbers; with strings, it repeats text.")
            elif isinstance(node.op, ast.Div):
                add("`/` divides and always produces a decimal-style `float` result.")
            elif isinstance(node.op, ast.FloorDiv):
                add("`//` divides and rounds down to a whole-number result.")
            elif isinstance(node.op, ast.Mod):
                add("`%` gives the remainder after division.")
            elif isinstance(node.op, ast.Pow):
                add("`**` raises a number to a power.")

        if isinstance(node, ast.Compare):
            add("Comparison operators like `==`, `<`, and `>` ask a question and return `True` or `False`.")
        elif isinstance(node, ast.BoolOp):
            add("`and` and `or` combine conditions so one decision can depend on multiple facts.")
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            add("`not` flips a boolean value: `True` becomes `False`, and `False` becomes `True`.")
        elif isinstance(node, ast.JoinedStr):
            add("An f-string lets you place variable values directly inside text.")
        elif isinstance(node, ast.List):
            add("Square brackets `[...]` create a list, which stores ordered values.")
        elif isinstance(node, ast.Dict):
            add("Curly braces with `key: value` pairs create a dictionary for labeled data.")

    return notes


def pick_real_life_example(lesson_title: str, section_title: str) -> str:
    topic = f"{lesson_title} {section_title}".lower()
    for keys, example in REAL_LIFE_MAP:
        if any(topic_has_key(topic, key) for key in keys):
            return example
    return ""


def parse_doc_metadata(filename: str, docstring: str) -> dict[str, Any]:
    fallback_title = fallback_title_from_filename(filename)

    title_match = re.search(r"Lesson\s+\d+\s*:\s*(.+)", docstring, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else fallback_title

    difficulty_match = re.search(r"Difficulty:\s*(.+)", docstring, re.IGNORECASE)
    estimated_match = re.search(r"Estimated\s+time:\s*(.+)", docstring, re.IGNORECASE)

    defaults = LESSON_DEFAULT_META.get(filename, {"difficulty": "Beginner", "time": "20 min"})

    difficulty = difficulty_match.group(1).strip() if difficulty_match else defaults["difficulty"]
    estimated_time = estimated_match.group(1).strip() if estimated_match else defaults["time"]

    doc_lines = docstring.splitlines()
    goals = extract_bullets(doc_lines, "What you will learn:")
    why_it_matters = extract_paragraph(
        doc_lines,
        "Why this matters for AI:",
        ["Estimated time:", "How to use this file:", "What you will learn:"],
    )

    plain_intro_parts: list[str] = []
    if goals:
        goals_text = "; ".join(goals[:3])
        plain_intro_parts.append(f"In this lesson you will learn {goals_text}.")
    if why_it_matters:
        plain_intro_parts.append(why_it_matters)

    plain_intro = " ".join(part.strip() for part in plain_intro_parts if part.strip())
    if not plain_intro:
        plain_intro = f"This lesson gives a beginner-friendly walkthrough of {title.lower()} with practical examples."

    return {
        "title": title,
        "difficulty": difficulty,
        "estimated_time": estimated_time,
        "learning_goals": goals,
        "why_it_matters": why_it_matters,
        "plain_intro": plain_intro,
    }


def parse_lesson_file(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    docstring = extract_docstring(content)
    metadata = parse_doc_metadata(path.name, docstring)

    matches = list(SECTION_HEADER_RE.finditer(content))
    sections: list[dict[str, Any]] = []
    seen_code_signatures: set[str] = set()
    seen_real_life_examples: set[str] = set()
    lesson_real_life_anchor = pick_real_life_example(metadata["title"], metadata["title"])
    if lesson_real_life_anchor:
        seen_real_life_examples.add(lesson_real_life_anchor)

    if matches:
        prelude_code = extract_prelude_code(content, matches[0].start())
        if prelude_code:
            runnable, reason = analyze_runnable_code(prelude_code)
            real_life_example = "Like placing ingredients on the counter before cooking, setup imports prepare the tools the lesson examples will use."
            seen_real_life_examples.add(real_life_example)
            sections.append(
                {
                    "id": 1,
                    "title": "Setup Imports",
                    "type": "theory",
                    "plain_explanation": "These imports and constants are used by the examples in this lesson. Read them once before you run or copy later snippets.",
                    "show_plain_explanation": True,
                    "real_life_example": real_life_example,
                    "blocks": [
                        {
                            "type": "code",
                            "content": prelude_code,
                            "is_repeated": False,
                            "id": code_block_id(prelude_code),
                            "runnable": runnable,
                            "runner_note": reason,
                            "concept_notes": code_concept_notes(prelude_code),
                        }
                    ],
                }
            )

    section_id_offset = len(sections)
    for match_index, match in enumerate(matches):
        idx = section_id_offset + match_index + 1
        title = match.group(1).strip().strip("=").strip()
        start = match.end()
        end = matches[match_index + 1].start() if match_index + 1 < len(matches) else len(content)
        body = content[start:end]

        blocks = parse_content_blocks(body)

        for block in blocks:
            if block["type"] != "code":
                continue
            normalized = re.sub(r"\s+", "", block["content"])
            signature = hashlib.sha1(normalized.encode("utf-8")).hexdigest()
            is_repeated = signature in seen_code_signatures
            block["is_repeated"] = is_repeated
            block["id"] = code_block_id(block["content"])
            runnable, reason = analyze_runnable_code(block["content"])
            block["runnable"] = runnable and not is_repeated
            block["runner_note"] = reason
            block["concept_notes"] = code_concept_notes(block["content"])
            if not is_repeated:
                seen_code_signatures.add(signature)

        text_blob = "\n\n".join(block["content"] for block in blocks if block["type"] == "text")
        plain_explanation = build_plain_explanation(title, text_blob)
        real_life_example = pick_real_life_example(metadata["title"], title)
        if real_life_example in seen_real_life_examples:
            real_life_example = ""
        elif real_life_example:
            seen_real_life_examples.add(real_life_example)

        section = {
            "id": idx,
            "title": title,
            "type": classify_section(title),
            "plain_explanation": plain_explanation,
            "show_plain_explanation": bool(plain_explanation) and not is_redundant_explanation(plain_explanation, text_blob),
            "real_life_example": real_life_example,
            "blocks": blocks,
        }
        sections.append(section)

    if not sections:
        fallback_blocks = parse_content_blocks(content)
        for block in fallback_blocks:
            if block["type"] != "code":
                continue
            block["id"] = code_block_id(block["content"])
            runnable, reason = analyze_runnable_code(block["content"])
            block["runnable"] = runnable
            block["runner_note"] = reason
            block["concept_notes"] = code_concept_notes(block["content"])
        sections.append(
            {
                "id": 1,
                "title": "Lesson Walkthrough",
                "type": "theory",
                "plain_explanation": build_plain_explanation("Lesson Walkthrough", " ".join(metadata["learning_goals"])),
                "show_plain_explanation": True,
                "real_life_example": pick_real_life_example(metadata["title"], "Lesson Walkthrough"),
                "blocks": fallback_blocks,
            }
        )

    number = path.name[:2] if path.name[:2].isdigit() else "00"
    slug = slug_from_filename(path.name)

    # Extract module details from parent directory (e.g. 01_python_programming)
    module_folder_name = path.parent.name
    if "_" in module_folder_name and module_folder_name[:2].isdigit():
        parts = module_folder_name.split("_", 1)
        module_id = parts[0]
        module_title = parts[1].replace("_", " ").title()
    else:
        module_id = "01"
        module_title = "Python Programming"

    code_block_count = sum(
        1
        for section in sections
        for block in section["blocks"]
        if block["type"] == "code"
    )

    lesson = {
        "number": number,
        "slug": slug,
        "filename": path.name,
        "title": metadata["title"],
        "difficulty": metadata["difficulty"],
        "estimated_time": metadata["estimated_time"],
        "learning_goals": metadata["learning_goals"],
        "why_it_matters": metadata["why_it_matters"],
        "plain_intro": metadata["plain_intro"],
        "real_life_anchor": lesson_real_life_anchor,
        "section_count": len(sections),
        "code_block_count": code_block_count,
        "sections": sections,
        "module": {
            "id": module_id,
            "title": module_title
        }
    }
    return lesson


# -----------------------------------------------------------------------------
# Progress store
# -----------------------------------------------------------------------------

def minutes_from_text(text: str) -> int:
    match = re.search(r"(\d+)", text)
    if not match:
        return 0
    return int(match.group(1))


def format_duration(total_minutes: int) -> str:
    if total_minutes <= 0:
        return "Self paced"
    hours, minutes = divmod(total_minutes, 60)
    if hours == 0:
        return f"{minutes}m"
    if minutes == 0:
        return f"{hours}h"
    return f"{hours}h {minutes}m"


def normalize_slug(value: Any, valid_slugs: set[str], filename_to_slug: dict[str, str]) -> str:
    if not isinstance(value, str):
        return ""

    candidate = value.strip()
    if not candidate:
        return ""

    if candidate in valid_slugs:
        return candidate

    if candidate in filename_to_slug:
        return filename_to_slug[candidate]

    if candidate.endswith(".py"):
        generated = slug_from_filename(candidate)
        if generated in valid_slugs:
            return generated

    return ""


def load_progress_data(valid_slugs: set[str], filename_to_slug: dict[str, str]) -> dict[str, Any]:
    default = {
        "student_name": "",
        "completed": [],
        "last_lesson": "",
        "theme": "day",
        "updated_at": "",
    }

    if not PROGRESS_FILE.exists():
        return default

    try:
        raw = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return default

    if isinstance(raw, list):
        raw_completed = raw
        student_name = ""
        last_lesson = ""
        theme = "day"
    elif isinstance(raw, dict):
        raw_completed = raw.get("completed", [])
        student_name = str(raw.get("student_name", ""))
        last_lesson = raw.get("last_lesson", "")
        theme = str(raw.get("theme", "day"))
    else:
        return default

    if isinstance(raw_completed, str):
        raw_completed = [raw_completed]
    if not isinstance(raw_completed, list):
        raw_completed = []

    completed: list[str] = []
    for item in raw_completed:
        slug = normalize_slug(item, valid_slugs, filename_to_slug)
        if slug and slug not in completed:
            completed.append(slug)

    last_slug = normalize_slug(last_lesson, valid_slugs, filename_to_slug)
    if not last_slug and completed:
        last_slug = completed[-1]

    if theme not in {"day", "night"}:
        theme = "day"

    return {
        "student_name": student_name,
        "completed": completed,
        "last_lesson": last_slug,
        "theme": theme,
        "updated_at": str(raw.get("updated_at", "")) if isinstance(raw, dict) else "",
    }


class ProgressStore:
    def __init__(self, valid_slugs: set[str], filename_to_slug: dict[str, str], slug_to_filename: dict[str, str], lesson_order: list[str]) -> None:
        self._valid_slugs = valid_slugs
        self._filename_to_slug = filename_to_slug
        self._slug_to_filename = slug_to_filename
        self._lesson_order = lesson_order
        self._index_map = {slug: idx for idx, slug in enumerate(lesson_order)}
        self._lock = threading.Lock()
        self._progress = load_progress_data(valid_slugs, filename_to_slug)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return json.loads(json.dumps(self._progress))

    def _sort_completed(self, values: list[str]) -> list[str]:
        unique = []
        for slug in values:
            if slug not in unique:
                unique.append(slug)
        return sorted(unique, key=lambda slug: self._index_map.get(slug, 10_000))

    def _save(self) -> None:
        payload = {
            "student_name": self._progress.get("student_name", ""),
            "completed": self._progress.get("completed", []),
            "completed_files": [self._slug_to_filename[slug] for slug in self._progress.get("completed", []) if slug in self._slug_to_filename],
            "last_lesson": self._progress.get("last_lesson", ""),
            "theme": self._progress.get("theme", "day"),
            "updated_at": self._progress.get("updated_at", ""),
        }
        PROGRESS_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def update(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError("Progress payload must be a JSON object")

        with self._lock:
            completed = list(self._progress.get("completed", []))

            if isinstance(payload.get("completed"), list):
                next_completed: list[str] = []
                for item in payload["completed"]:
                    slug = normalize_slug(item, self._valid_slugs, self._filename_to_slug)
                    if slug:
                        next_completed.append(slug)
                completed = self._sort_completed(next_completed)

            if "complete_lesson" in payload:
                slug = normalize_slug(payload.get("complete_lesson"), self._valid_slugs, self._filename_to_slug)
                if slug and slug not in completed:
                    completed.append(slug)
                    completed = self._sort_completed(completed)

            if "uncomplete_lesson" in payload:
                slug = normalize_slug(payload.get("uncomplete_lesson"), self._valid_slugs, self._filename_to_slug)
                if slug:
                    completed = [item for item in completed if item != slug]

            self._progress["completed"] = completed

            if "last_lesson" in payload:
                last_slug = normalize_slug(payload.get("last_lesson"), self._valid_slugs, self._filename_to_slug)
                if last_slug:
                    self._progress["last_lesson"] = last_slug

            if "theme" in payload:
                theme = str(payload.get("theme", "day"))
                self._progress["theme"] = "night" if theme == "night" else "day"

            if "student_name" in payload:
                name = str(payload.get("student_name", "")).strip()
                self._progress["student_name"] = name[:60]

            self._progress["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            self._save()
            return json.loads(json.dumps(self._progress))


# -----------------------------------------------------------------------------
# Search
# -----------------------------------------------------------------------------

def build_snippet(text: str, query: str) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return ""

    lower_cleaned = cleaned.lower()
    lower_query = query.lower()
    idx = lower_cleaned.find(lower_query)

    if idx == -1:
        if len(cleaned) <= 160:
            return cleaned
        return cleaned[:157].rstrip() + "..."

    start = max(0, idx - 60)
    end = min(len(cleaned), idx + len(query) + 90)
    snippet = cleaned[start:end]

    if start > 0:
        snippet = "..." + snippet
    if end < len(cleaned):
        snippet = snippet + "..."

    return snippet


def search_lessons(query: str, lessons: list[dict[str, Any]], limit: int = 20) -> list[dict[str, Any]]:
    q = query.strip().lower()
    if len(q) < 2:
        return []

    results: list[dict[str, Any]] = []

    for lesson in lessons:
        base_score = 0
        if q in lesson["title"].lower():
            base_score += 30
        if any(q in goal.lower() for goal in lesson.get("learning_goals", [])):
            base_score += 15
        if q in lesson.get("plain_intro", "").lower():
            base_score += 10

        for section in lesson["sections"]:
            score = base_score
            snippet_source = section.get("plain_explanation", "")

            if q in section["title"].lower():
                score += 20

            text_blob = " ".join(
                block["content"]
                for block in section["blocks"]
                if block["type"] == "text"
            )
            code_blob = " ".join(
                block["content"]
                for block in section["blocks"]
                if block["type"] == "code"
            )

            if q in text_blob.lower():
                score += 10
                snippet_source = text_blob
            elif q in code_blob.lower():
                score += 6
                snippet_source = code_blob

            if score <= 0:
                continue

            results.append(
                {
                    "lesson_slug": lesson["slug"],
                    "lesson_title": lesson["title"],
                    "section_id": section["id"],
                    "section_title": section["title"],
                    "snippet": build_snippet(snippet_source, q),
                    "score": score,
                }
            )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]


# -----------------------------------------------------------------------------
# Web UI
# -----------------------------------------------------------------------------

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Craft with AI - Build Enterprise AI from Scratch</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    :root {
      --font-heading: "Outfit", sans-serif;
      --font-body: "Plus Jakarta Sans", sans-serif;
      --font-code: "JetBrains Mono", monospace;

      --bg: #f8fafc;
      --bg-alt: #f1f5f9;
      --panel: rgba(255, 255, 255, 0.7);
      --panel-strong: #ffffff;
      --text: #0f172a;
      --muted: #475569;
      --accent: #4f46e5;
      --accent-soft: rgba(79, 70, 229, 0.08);
      --accent-strong: #3730a3;
      --warm: #f97316;
      --border: rgba(226, 232, 240, 0.8);
      --shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.02);
      --code-bg: #0f172a;
      --code-text: #e2e8f0;

      --accent-rgb: 79, 70, 229;
      --border-glow: rgba(79, 70, 229, 0.15);
    }

    body[data-theme="night"] {
      --bg: #080c14;
      --bg-alt: #0e1320;
      --panel: rgba(15, 23, 42, 0.65);
      --panel-strong: #1e293b;
      --text: #f8fafc;
      --muted: #94a3b8;
      --accent: #818cf8;
      --accent-soft: rgba(129, 140, 248, 0.12);
      --accent-strong: #a5b4fc;
      --warm: #fb923c;
      --border: rgba(51, 65, 85, 0.45);
      --shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.05);
      --code-bg: #090d16;
      --code-text: #f1f5f9;

      --accent-rgb: 129, 140, 248;
      --border-glow: rgba(129, 140, 248, 0.25);
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      color: var(--text);
      background: radial-gradient(circle at 10% 15%, rgba(var(--accent-rgb), 0.08), transparent 45%),
                  radial-gradient(circle at 85% 5%, rgba(249, 115, 22, 0.06), transparent 40%),
                  var(--bg);
      font-family: var(--font-body);
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.5;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: var(--border);
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: color-mix(in srgb, var(--border) 150%, transparent);
    }

    .app {
      position: relative;
      z-index: 1;
    }

    .topbar {
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      gap: 16px;
      align-items: center;
      justify-content: space-between;
      padding: 14px 24px;
      border-bottom: 1px solid var(--border);
      background: rgba(var(--accent-rgb), 0.02);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
    }

    .brand {
      font-family: var(--font-heading);
      font-size: 1.2rem;
      letter-spacing: -0.01em;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
      user-select: none;
    }

    .brand span {
      background: linear-gradient(135deg, var(--accent), var(--warm));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-weight: 900;
    }

    .search-wrap {
      display: flex;
      gap: 12px;
      align-items: center;
      width: min(760px, 100%);
      flex: 1;
      justify-content: flex-end;
      position: relative;
    }

    .search {
      width: min(520px, 100%);
      padding: 11px 16px 11px 40px;
      border: 1px solid var(--border);
      border-radius: 14px;
      background: var(--panel-strong);
      color: var(--text);
      font-size: 0.92rem;
      font-family: var(--font-heading);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'%3E%3C/circle%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'%3E%3C/line%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: 14px center;
    }

    .search:focus {
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 0 4px var(--accent-soft), inset 0 2px 4px rgba(0,0,0,0.01);
    }

    .btn {
      border: 1px solid var(--border);
      background: var(--panel-strong);
      color: var(--text);
      border-radius: 12px;
      padding: 10px 16px;
      font-family: var(--font-heading);
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      user-select: none;
    }

    .btn:hover:not(:disabled) {
      transform: translateY(-2px);
      border-color: var(--accent);
      box-shadow: 0 4px 12px rgba(var(--accent-rgb), 0.08);
    }

    .btn:active:not(:disabled) {
      transform: translateY(0);
    }

    .btn.primary {
      border-color: var(--accent);
      background: var(--accent);
      color: #ffffff;
    }

    .btn.primary:hover:not(:disabled) {
      background: color-mix(in srgb, var(--accent) 90%, #000);
      box-shadow: 0 4px 16px rgba(var(--accent-rgb), 0.20);
    }

    .layout {
      width: 100%;
      max-width: 100%;
      margin: 0 auto;
      padding: 24px;
      display: grid;
      grid-template-columns: var(--sidebar-width, 340px) minmax(0, 1fr);
      transition: grid-template-columns 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      align-items: start;
    }

    .card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 20px;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      box-shadow: var(--shadow);
      padding: 20px;
      animation: rise 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
      border-color: var(--border-glow);
    }

    @keyframes rise {
      from { opacity: 0; transform: translateY(12px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Collapsible Sticky Sidebar Styles */
    .sidebar {
      width: 100%;
      margin-right: 24px;
      transition: margin-right 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease, transform 0.3s ease;
      position: sticky;
      top: 90px;
      max-height: calc(100vh - 120px);
      overflow-y: auto;
      padding-right: 6px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    /* Beautiful custom scrollbar for sticky sidebar */
    .sidebar::-webkit-scrollbar {
      width: 6px;
    }
    .sidebar::-webkit-scrollbar-track {
      background: transparent;
    }
    .sidebar::-webkit-scrollbar-thumb {
      background: var(--border);
      border-radius: 99px;
    }
    .sidebar::-webkit-scrollbar-thumb:hover {
      background: var(--accent-soft);
    }
    
    .layout.hide-left {
      grid-template-columns: 0px minmax(0, 1fr);
    }
    
    .layout.hide-left .sidebar {
      opacity: 0;
      pointer-events: none;
      transform: translateX(-20px);
      margin-right: 0px;
    }

    #toggleLeftBtn {
      padding: 8px 10px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }

    .sidebar .heading {
      margin: 0 0 12px;
      font-family: var(--font-heading);
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--muted);
    }


    .course-title {
      margin: 0;
      font-family: var(--font-heading);
      font-size: 1.4rem;
      line-height: 1.2;
      font-weight: 800;
    }

    .course-subtitle {
      margin: 8px 0 12px;
      color: var(--muted);
      font-size: 0.92rem;
      line-height: 1.4;
    }

    .stat-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-top: 14px;
    }

    .stat {
      background: var(--panel-strong);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 10px 6px;
      text-align: center;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .stat:hover {
      transform: translateY(-1px);
      border-color: var(--accent);
    }

    .stat .value {
      display: block;
      font-family: var(--font-heading);
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--accent);
    }

    .stat .label {
      font-size: 0.68rem;
      font-weight: 600;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .progress-shell {
      margin-top: 14px;
      width: 100%;
      height: 8px;
      border-radius: 999px;
      background: var(--bg-alt);
      border: 1px solid var(--border);
      overflow: hidden;
    }

    .progress-fill {
      height: 100%;
      width: 0;
      background: linear-gradient(90deg, var(--accent), #06b6d4);
      transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
    }

    .status {
      margin-top: 10px;
      color: var(--muted);
      font-size: 0.88rem;
      font-weight: 500;
    }

    .lesson-list {
      margin-top: 12px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-height: calc(100vh - 300px);
      overflow-y: auto;
      padding-right: 4px;
    }
    .lesson-list::-webkit-scrollbar {
      width: 6px;
    }
    .lesson-list::-webkit-scrollbar-track {
      background: transparent;
    }
    .lesson-list::-webkit-scrollbar-thumb {
      background: var(--border);
      border-radius: 99px;
    }
    .lesson-list::-webkit-scrollbar-thumb:hover {
      background: var(--accent-soft);
    }

    .module-group {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 22px;
    }
    .module-group:last-child {
      margin-bottom: 0;
    }
    .module-group.collapsed .module-lessons {
      display: none;
    }
    .module-header {
      padding: 6px 12px;
      border-left: 3px solid var(--accent);
      background: linear-gradient(90deg, color-mix(in srgb, var(--panel-strong) 40%, transparent) 0%, transparent 100%);
      border-radius: 0 10px 10px 0;
      margin-bottom: 6px;
      cursor: pointer;
      user-select: none;
      transition: all 0.2s ease;
    }
    .module-header:hover {
      background: linear-gradient(90deg, color-mix(in srgb, var(--panel-strong) 60%, transparent) 0%, transparent 100%);
    }
    .module-eyebrow {
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--accent);
      font-weight: 750;
      font-family: var(--font-heading);
      display: block;
    }
    .module-title {
      font-size: 0.88rem;
      font-weight: 800;
      color: var(--text);
      font-family: var(--font-heading);
      margin: 2px 0 0 0;
      line-height: 1.25;
    }
    .module-lessons {
      display: flex;
      flex-direction: column;
      gap: 10px;
      padding-left: 2px;
    }

    .lesson-item {
      width: 100%;
      text-align: left;
      border: 1px solid var(--border);
      background: var(--panel-strong);
      background: color-mix(in srgb, var(--panel-strong) 85%, transparent);
      border-radius: 14px;
      padding: 12px 14px;
      cursor: pointer;
      color: var(--text);
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .lesson-item:hover {
      border-color: var(--accent);
      background: var(--accent-soft);
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(var(--accent-rgb), 0.06);
    }

    .lesson-item.active {
      border-color: var(--accent);
      background: var(--accent-soft);
      box-shadow: 0 0 0 1px var(--accent), 0 4px 16px rgba(var(--accent-rgb), 0.1);
    }

    .lesson-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
    }

    .lesson-top strong {
      font-family: var(--font-heading);
      font-size: 0.8rem;
      background: var(--accent-soft);
      color: var(--accent);
      padding: 2px 8px;
      border-radius: 6px;
      font-weight: 700;
    }

    .lesson-title {
      margin-top: 4px;
      font-size: 0.95rem;
      line-height: 1.3;
    }

    .meta {
      margin-top: 5px;
      font-size: 0.77rem;
      color: var(--muted);
    }

    .badge {
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 3px 10px;
      font-size: 0.72rem;
      font-weight: 600;
      font-family: var(--font-heading);
      color: var(--muted);
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .badge.done {
      color: #10b981;
      border-color: rgba(16, 185, 129, 0.25);
      background: rgba(16, 185, 129, 0.08);
    }

    .main {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .hero {
      position: relative;
      background-image: radial-gradient(var(--border) 1px, transparent 1px);
      background-size: 20px 20px;
      overflow: hidden;
    }

    .hero .eyebrow {
      margin: 0;
      font-family: var(--font-heading);
      font-size: 0.8rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent);
      font-weight: 700;
    }

    .hero h1 {
      margin: 8px 0 12px;
      font-family: var(--font-heading);
      font-size: clamp(1.6rem, 1.4rem + 1.2vw, 2.2rem);
      line-height: 1.15;
      font-weight: 800;
    }

    .hero p {
      margin: 0;
      line-height: 1.6;
      color: var(--text);
      font-size: 1.02rem;
      text-wrap: pretty;
    }

    .hero-callout {
      margin-top: 16px;
      border-left: 3px solid var(--accent);
      border-radius: 4px 12px 12px 4px;
      padding: 12px 16px;
      background: var(--accent-soft);
      font-size: 0.96rem;
      line-height: 1.5;
    }

    .goal-wrap {
      margin-top: 16px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .goal {
      border-radius: 999px;
      padding: 6px 12px;
      background: var(--panel-strong);
      border: 1px solid var(--border);
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text);
      transition: border-color 0.2s ease;
    }
    
    .goal:hover {
      border-color: var(--accent);
    }

    .hero-actions {
      margin-top: 14px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .section-toolbar {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: center;
      border-bottom: 1px solid var(--border);
      padding-bottom: 16px;
      margin-bottom: 16px;
    }

    .section-toolbar h2 {
      margin: 0;
      font-family: var(--font-heading);
      font-size: 1.2rem;
      font-weight: 800;
    }
    
    .section-toolbar > div {
      display: flex;
      gap: 8px;
    }

    .section-list {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .section-card {
      --section-accent: var(--accent);
      --section-accent-rgb: var(--accent-rgb);
      --section-title-size: 1.15rem;
      position: relative;
      border: 1px solid color-mix(in srgb, var(--section-accent) 18%, var(--border));
      border-radius: 18px;
      background:
        linear-gradient(135deg, rgba(var(--section-accent-rgb), 0.07), transparent 34%),
        var(--panel);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: all 0.3s ease;
      overflow: hidden;
    }

    .section-card::before {
      content: "";
      position: absolute;
      inset: 0 auto 0 0;
      width: 5px;
      background: linear-gradient(180deg, var(--section-accent), color-mix(in srgb, var(--section-accent) 45%, transparent));
    }

    .section-card.section-type-theory {
      --section-accent: #0ea5e9;
      --section-accent-rgb: 14, 165, 233;
      --section-title-size: 1.16rem;
    }

    .section-card.section-type-exercise {
      --section-accent: #f59e0b;
      --section-accent-rgb: 245, 158, 11;
      --section-title-size: 1.24rem;
      background:
        linear-gradient(135deg, rgba(var(--section-accent-rgb), 0.10), transparent 38%),
        var(--panel);
    }

    .section-card.section-type-solution {
      --section-accent: #10b981;
      --section-accent-rgb: 16, 185, 129;
      --section-title-size: 1.12rem;
    }

    .section-card.section-type-warning {
      --section-accent: #ef4444;
      --section-accent-rgb: 239, 68, 68;
      --section-title-size: 1.18rem;
    }

    .section-card.section-type-takeaway {
      --section-accent: #7c3aed;
      --section-accent-rgb: 124, 58, 237;
      --section-title-size: 1.08rem;
    }

    .section-card.section-type-realworld {
      --section-accent: #ea580c;
      --section-accent-rgb: 234, 88, 12;
      --section-title-size: 1.2rem;
    }

    .section-card.section-type-next {
      --section-accent: #14b8a6;
      --section-accent-rgb: 20, 184, 166;
      --section-title-size: 1.1rem;
    }
    
    .section-card:hover {
      border-color: color-mix(in srgb, var(--section-accent) 42%, var(--border));
      box-shadow: 0 18px 36px -24px rgba(var(--section-accent-rgb), 0.45);
    }

    .section-header {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      border-bottom: 1px solid var(--border);
      padding-bottom: 10px;
      margin-bottom: 8px;
      position: relative;
    }

    .section-header h3 {
      margin: 0;
      font-family: var(--font-heading);
      font-size: var(--section-title-size);
      font-weight: 850;
      line-height: 1.3;
      letter-spacing: 0;
      color: color-mix(in srgb, var(--section-accent) 24%, var(--text));
    }

    .step-pill {
      font-family: var(--font-heading);
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid var(--border);
      color: var(--muted);
      white-space: nowrap;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: color-mix(in srgb, var(--section-accent) 10%, var(--panel-strong));
      border-color: color-mix(in srgb, var(--section-accent) 26%, var(--border));
      color: var(--section-accent);
    }

    .step-pill.pill-theory {
      background: rgba(14, 165, 233, 0.08);
      border-color: rgba(14, 165, 233, 0.2);
      color: #0ea5e9;
    }
    .step-pill.pill-exercise {
      background: rgba(79, 70, 229, 0.08);
      border-color: rgba(79, 70, 229, 0.2);
      color: #4f46e5;
    }
    .step-pill.pill-solution {
      background: rgba(16, 185, 129, 0.08);
      border-color: rgba(16, 185, 129, 0.2);
      color: #10b981;
    }
    .step-pill.pill-warning {
      background: rgba(239, 68, 68, 0.08);
      border-color: rgba(239, 68, 68, 0.2);
      color: #ef4444;
    }
    .step-pill.pill-takeaway {
      background: rgba(168, 85, 247, 0.08);
      border-color: rgba(168, 85, 247, 0.2);
      color: #a855f7;
    }
    .step-pill.pill-realworld {
      background: rgba(245, 158, 11, 0.08);
      border-color: rgba(245, 158, 11, 0.2);
      color: #f59e0b;
    }
    .step-pill.pill-next {
      background: rgba(20, 184, 166, 0.08);
      border-color: rgba(20, 184, 166, 0.2);
      color: #20b8a6;
    }

    .mini-box {
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px;
      margin-top: 14px;
      background: var(--panel-strong);
      transition: transform 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .mini-box:hover {
      transform: translateY(-1px);
    }

    .mini-box-header {
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text);
    }

    .mini-box h4 {
      margin: 0;
      font-family: var(--font-heading);
      font-size: 0.84rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--muted);
    }

    .mini-box p {
      margin: 0;
      line-height: 1.6;
      font-size: 0.96rem;
      color: var(--text);
    }

    .mini-box.simple-words {
      border-left: 4px solid var(--warm);
      background: color-mix(in srgb, var(--warm) 4%, var(--panel-strong));
    }
    .mini-box.simple-words h4 {
      color: var(--warm);
    }
    .mini-box.simple-words .mini-box-icon {
      color: var(--warm);
    }

    .mini-box.real-life {
      border-left: 4px solid var(--accent);
      background: color-mix(in srgb, var(--accent) 4%, var(--panel-strong));
    }
    .mini-box.real-life h4 {
      color: var(--accent);
    }
    .mini-box.real-life .mini-box-icon {
      color: var(--accent);
    }

    .mini-box.what-is-definition {
      border-left: 4px solid var(--accent);
      background: color-mix(in srgb, var(--accent) 4%, var(--panel-strong));
      margin-top: 14px;
      margin-bottom: 14px;
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .mini-box.what-is-definition h4,
    .mini-box.what-is-definition .mini-box-icon {
      color: var(--accent);
    }
    .mini-box.what-is-definition p {
      margin: 0;
      line-height: 1.6;
      font-size: 0.96rem;
      color: var(--text);
    }

    .mini-box.code-concepts {
      border-left: 4px solid #0ea5e9;
      background: color-mix(in srgb, #0ea5e9 5%, var(--panel-strong));
    }
    .mini-box.code-concepts h4,
    .mini-box.code-concepts .mini-box-icon {
      color: #0ea5e9;
    }
    .mini-box.code-concepts ul {
      margin: 0;
      padding-left: 18px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      color: var(--text);
      line-height: 1.55;
      font-size: 0.94rem;
    }
    .mini-box.code-concepts code {
      font-family: var(--font-code);
      font-size: 0.88em;
      padding: 1px 5px;
      border-radius: 6px;
      background: var(--accent-soft);
      color: var(--accent-strong);
      border: 1px solid var(--border);
    }

    .text-block {
      margin-top: 12px;
      font-size: 1rem;
      line-height: 1.65;
      color: var(--text);
    }

    .structured-text {
      display: block;
    }



    .structured-text > * {
      break-inside: avoid;
    }

    .text-paragraph {
      margin: 0 0 13px;
      text-wrap: pretty;
    }

    .text-subhead {
      margin: 18px 0 8px;
      font-family: var(--font-heading);
      font-size: 0.94rem;
      line-height: 1.3;
      font-weight: 850;
      color: color-mix(in srgb, var(--section-accent) 34%, var(--text));
      text-transform: none;
    }

    .text-subhead:first-child {
      margin-top: 0;
    }

    .text-flow {
      margin: 8px 0;
      padding: 10px 12px;
      border: 1px solid color-mix(in srgb, var(--section-accent) 18%, var(--border));
      border-radius: 10px;
      background: color-mix(in srgb, var(--section-accent) 5%, var(--panel-strong));
      font-family: var(--font-code);
      font-size: 0.91rem;
      line-height: 1.55;
      color: var(--text);
    }

    .text-analogy {
      margin: 10px 0 14px;
      padding: 10px 12px;
      border-left: 3px solid var(--section-accent);
      border-radius: 4px 10px 10px 4px;
      background: color-mix(in srgb, var(--section-accent) 6%, var(--panel-strong));
      color: var(--muted);
      font-size: 0.96rem;
      line-height: 1.55;
    }

    .text-block .structured-list,
    .structured-list {
      margin: 0 0 14px 0;
      padding: 12px 14px 12px 34px;
      border: 1px solid color-mix(in srgb, var(--section-accent) 14%, var(--border));
      border-radius: 12px;
      background: color-mix(in srgb, var(--section-accent) 4%, var(--panel-strong));
    }

    .text-block p {
      margin: 0 0 12px;
      text-wrap: pretty;
    }

    .section-type-exercise .text-block,
    .section-type-realworld .text-block {
      font-size: 1.03rem;
    }

    .section-type-takeaway .text-block {
      font-size: 0.98rem;
      font-weight: 520;
    }

    .section-type-warning .text-block {
      font-size: 1.01rem;
    }

    .text-block ul {
      margin: 0 0 12px 20px;
      padding: 0;
    }
    
    .text-block li {
      margin-bottom: 6px;
    }

    .section-type-takeaway .text-block li,
    .section-type-warning .text-block li {
      padding-left: 2px;
      margin-bottom: 8px;
    }

    .text-block .lead-line {
      display: inline-flex;
      width: fit-content;
      margin: 4px 0 2px;
      padding: 4px 9px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: color-mix(in srgb, var(--accent) 8%, var(--panel-strong));
      color: var(--accent);
      font-family: var(--font-heading);
      font-size: 0.82rem;
      font-weight: 800;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .text-block .numbered-lines {
      margin: 0 0 12px 0;
      padding-left: 24px;
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .text-block .inline-code {
      font-family: var(--font-code);
      font-size: 0.9em;
      padding: 1px 5px;
      border-radius: 6px;
      background: var(--accent-soft);
      color: var(--accent-strong);
      border: 1px solid var(--border);
    }



    details.code {
      margin-top: 12px;
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      background: var(--code-bg);
      box-shadow: 0 10px 30px -15px rgba(0, 0, 0, 0.3);
      transition: all 0.3s ease;
    }

    details.code summary {
      cursor: pointer;
      font-family: var(--font-heading);
      font-size: 0.88rem;
      padding: 12px 16px;
      background: color-mix(in srgb, var(--code-bg) 92%, var(--text));
      border-bottom: 1px solid var(--border);
      list-style: none;
      display: flex;
      align-items: center;
      justify-content: space-between;
      user-select: none;
      color: var(--code-text);
      font-weight: 600;
    }

    details.code summary::-webkit-details-marker {
      display: none;
    }

    .summary-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .terminal-dots {
      display: flex;
      gap: 6px;
    }

    .terminal-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }
    .terminal-dot.red { background: #ff5f56; }
    .terminal-dot.yellow { background: #ffbd2e; }
    .terminal-dot.green { background: #27c93f; }

    .summary-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .tech-badge {
      font-size: 0.72rem;
      background: rgba(255, 255, 255, 0.08);
      color: var(--accent);
      padding: 2px 8px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.05);
      font-family: var(--font-heading);
      letter-spacing: 0.03em;
      text-transform: uppercase;
      font-weight: 700;
    }

    .chevron-icon {
      width: 16px;
      height: 16px;
      transition: transform 0.25s ease;
      stroke: var(--muted);
    }

    details.code[open] .chevron-icon {
      transform: rotate(90deg);
    }

    .code-shell {
      background: var(--code-bg);
      color: var(--code-text);
      padding: 16px;
      overflow: auto;
      position: relative;
    }

    details.code[open] .code-shell {
      animation: slideDown 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes slideDown {
      from { opacity: 0; transform: translateY(-8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .code-shell pre {
      margin: 0;
      font-family: var(--font-code);
      font-size: 0.86rem;
      line-height: 1.55;
      overflow-x: auto;
    }

    .copy-btn {
      position: absolute;
      top: 10px;
      right: 10px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--code-text);
      border-radius: 8px;
      padding: 6px 12px;
      font-family: var(--font-heading);
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .copy-btn:hover {
      background: var(--accent);
      border-color: var(--accent);
      color: #ffffff;
      transform: translateY(-1px);
      box-shadow: 0 4px 10px rgba(var(--accent-rgb), 0.25);
    }

    .repeat-note {
      margin-top: 12px;
      border: 1px dashed rgba(249, 115, 22, 0.3);
      border-radius: 14px;
      padding: 12px 16px;
      font-size: 0.88rem;
      color: var(--muted);
      background: rgba(249, 115, 22, 0.05);
      line-height: 1.5;
    }

    .runner-panel {
      margin-top: 10px;
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      background: var(--panel-strong);
    }

    .runner-header {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      background: color-mix(in srgb, var(--accent) 6%, var(--panel-strong));
    }

    .runner-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-heading);
      font-size: 0.84rem;
      font-weight: 800;
      color: var(--accent);
    }

    .runner-editor {
      width: 100%;
      min-height: 120px;
      resize: vertical;
      border: 0;
      outline: 0;
      padding: 14px;
      background: var(--code-bg);
      color: var(--code-text);
      font-family: var(--font-code);
      font-size: 0.84rem;
      line-height: 1.55;
      display: block;
    }

    .runner-output {
      margin: 0;
      min-height: 46px;
      max-height: 260px;
      overflow: auto;
      white-space: pre-wrap;
      padding: 12px 14px;
      border-top: 1px solid var(--border);
      background: var(--bg-alt);
      color: var(--text);
      font-family: var(--font-code);
      font-size: 0.82rem;
      line-height: 1.5;
    }

    .runner-output.error {
      color: #dc2626;
      background: rgba(239, 68, 68, 0.07);
    }

    .benchmark-list,
    .search-results {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-top: 10px;
    }

    .benchmark-item {
      border: 1px solid var(--border);
      border-radius: 16px;
      background: var(--panel-strong);
      background: color-mix(in srgb, var(--panel-strong) 85%, transparent);
      padding: 14px;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .benchmark-item:hover {
      transform: translateY(-2px);
      border-color: var(--accent);
    }

    .benchmark-item a {
      color: var(--accent);
      text-decoration: none;
      font-family: var(--font-heading);
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    
    .benchmark-item a:hover {
      text-decoration: underline;
    }

    .benchmark-item ul {
      margin: 8px 0 0 16px;
      padding: 0;
      font-size: 0.86rem;
      color: var(--muted);
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none !important;
      box-shadow: none !important;
    }

    .search-results-overlay {
      position: absolute;
      top: calc(100% + 8px);
      right: 50px; /* Offset the night toggle button */
      width: min(520px, calc(100vw - 48px));
      background: var(--panel);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--border-glow);
      border-radius: 16px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.25), 0 4px 12px rgba(var(--accent-rgb), 0.08);
      z-index: 1100;
      display: none;
      max-height: 380px;
      overflow-y: auto;
      padding: 12px;
      animation: spotlight-rise 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .search-results-overlay.active {
      display: block;
    }

    @keyframes spotlight-rise {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .search-results-overlay::-webkit-scrollbar {
      width: 6px;
    }
    .search-results-overlay::-webkit-scrollbar-track {
      background: transparent;
    }
    .search-results-overlay::-webkit-scrollbar-thumb {
      background: var(--border);
      border-radius: 99px;
    }

    .search-item {
      text-align: left;
      width: 100%;
      cursor: pointer;
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 14px;
      background: var(--panel-strong);
      background: color-mix(in srgb, var(--panel-strong) 85%, transparent);
      padding: 12px 14px;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .search-item:hover {
      border-color: var(--accent);
      background: var(--accent-soft);
      transform: translateY(-1px);
    }

    .empty {
      color: var(--muted);
      font-size: 0.88rem;
      margin: 6px 0 0;
      line-height: 1.4;
    }

    footer {
      max-width: 1550px;
      margin: 0 auto;
      padding: 8px 24px 24px;
      color: var(--muted);
      font-size: 0.84rem;
      text-align: center;
      border-top: 1px solid var(--border);
      margin-top: 32px;
    }

    @media (max-width: 900px) {
      .layout.hide-left .sidebar {
        display: none;
      }
      .topbar {
        flex-direction: column;
        align-items: stretch;
        padding: 16px;
      }
      .search-wrap {
        width: 100%;
        justify-content: flex-start;
      }
      .layout {
        display: flex;
        flex-direction: column;
        padding: 16px;
        gap: 16px;
      }
      .sidebar,
      .main {
        width: 100%;
      }
      .main {
        order: 1;
      }
      .sidebar {
        order: 2;
      }
      .lesson-list {
        max-height: 240px;
      }
      .section-toolbar {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
      }
      .section-toolbar > div {
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }
      .btn {
        flex: 1;
        justify-content: center;
      }
    }
  </style>
</head>
<body data-theme="day">
  <div class="app">
    <header class="topbar">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button id="toggleLeftBtn" class="btn" title="Toggle Syllabus">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="9" y1="3" x2="9" y2="21"/></svg>
        </button>
        <div class="brand">Craft with <span>AI</span></div>
      </div>
      <div class="search-wrap">
        <input id="searchInput" class="search" placeholder="Search concepts: loops, csv, api, functions..." autocomplete="off" />
        <div id="searchResults" class="search-results-overlay">
          <p class="empty">Type at least 2 letters to search.</p>
        </div>
        <button id="themeToggle" class="btn"></button>
      </div>
    </header>

    <div class="layout">
      <aside class="sidebar">
        <section class="card" style="margin-bottom: 20px;">
          <h2 class="course-title" id="courseTitle"></h2>
          <p class="course-subtitle" id="courseSubtitle"></p>
          <div id="courseStats" class="stat-grid"></div>
          <div class="progress-shell"><div id="progressFill" class="progress-fill"></div></div>
          <p id="courseStatus" class="status"></p>
        </section>

        <section class="card">
          <h3 class="heading">Syllabus</h3>
          <div id="lessonList" class="lesson-list"></div>
        </section>
      </aside>

      <main class="main">
        <section id="hero" class="card hero"></section>

        <section class="card">
          <div class="section-toolbar">
            <h2>Guided Walkthrough</h2>
            <div>
              <button id="markCompleteBtn" class="btn primary">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                <span>Mark Lesson Complete</span>
              </button>
              <button id="prevLessonBtn" class="btn">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
                <span>Previous</span>
              </button>
              <button id="nextLessonBtn" class="btn">
                <span>Next</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
              </button>
            </div>
          </div>
          <div id="sectionList" class="section-list"></div>
        </section>
      </main>
    </div>

    <footer>
      Craft with AI • Build enterprise-grade AI systems end-to-end, with the help of AI
    </footer>
  </div>

  <script>
    const state = {
      course: null,
      lessons: [],
      progress: null,
      benchmarks: [],
      currentLessonSlug: "",
      lessonCache: new Map(),
    };

    const refs = {
      searchInput: document.getElementById("searchInput"),
      themeToggle: document.getElementById("themeToggle"),
      courseTitle: document.getElementById("courseTitle"),
      courseSubtitle: document.getElementById("courseSubtitle"),
      courseStats: document.getElementById("courseStats"),
      progressFill: document.getElementById("progressFill"),
      courseStatus: document.getElementById("courseStatus"),
      lessonList: document.getElementById("lessonList"),
      hero: document.getElementById("hero"),
      sectionList: document.getElementById("sectionList"),
      markCompleteBtn: document.getElementById("markCompleteBtn"),
      prevLessonBtn: document.getElementById("prevLessonBtn"),
      nextLessonBtn: document.getElementById("nextLessonBtn"),
      searchResults: document.getElementById("searchResults"),
    };

    let searchTimer = null;

    function escapeHtml(value) {
      return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }

    function sectionTypeLabel(kind) {
      const map = {
        theory: "Concept",
        exercise: "Exercise",
        solution: "Solution",
        takeaway: "Key Point",
        warning: "Common Mistake",
        realworld: "Real World",
        next: "Next Step",
      };
      return map[kind] || "Concept";
    }

    function getPillIcon(kind) {
      const map = {
        theory: `<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>`,
        exercise: `<polygon points="5 3 19 12 5 21 5 3"/>`,
        solution: `<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>`,
        takeaway: `<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>`,
        warning: `<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>`,
        realworld: `<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>`,
        next: `<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>`,
      };
      return map[kind] || `<circle cx="12" cy="12" r="10"/>`;
    }

    function formatInlineText(value) {
      return escapeHtml(value).replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    }

    function formatConceptText(value) {
      return escapeHtml(value).replace(/`([^`]+)`/g, '<code>$1</code>');
    }

    function isSubheadingLine(line) {
      if (/^[A-Z][A-Z0-9 /&().'"-]{3,}:$/.test(line)) {
        return true;
      }
      if (/^[A-Z][A-Za-z0-9 /&().'"-]{2,}:$/.test(line) && line.length <= 80) {
        const cleanLine = line.replace(/:$/, "").trim();
        const words = cleanLine.split(/\\s+/).filter(Boolean);
        if (words.length > 2) {
          const minorWords = new Set([
            "a", "an", "the", "in", "on", "at", "to", "for", "with", "and", "but", "or", "is", "of", "by", "from", "as", "vs", "vs.", "via",
            "into", "over", "under", "through", "about", "its", "their", "our", "your", "my", "his", "her", "it", "them", "us"
          ]);
          let lowercaseMajorWords = 0;
          for (let idx = 1; idx < words.length; idx++) {
            const word = words[idx];
            if (!/^[a-zA-Z]+$/.test(word)) { continue; }
            if (minorWords.has(word.toLowerCase())) { continue; }
            if (word[0] === word[0].toLowerCase()) {
              lowercaseMajorWords++;
            }
          }
          if (lowercaseMajorWords >= 1) {
            return false;
          }
        }
        return true;
      }
      if (/^[A-Z][A-Za-z0-9 /&().'"-]{2,}\\. This means:$/.test(line)) {
        return true;
      }
      return false;
    }

    function renderStructuredLines(lines) {
      const parts = [];
      let paragraph = [];
      let list = [];
      let orderedList = [];

      function flushParagraph() {
        if (!paragraph.length) { return; }
        parts.push(`<p class="text-paragraph">${paragraph.map(formatInlineText).join(" ")}</p>`);
        paragraph = [];
      }

      function flushList() {
        if (!list.length) { return; }
        parts.push(`<ul class="structured-list">${list.map(item => `<li>${formatInlineText(item)}</li>`).join("")}</ul>`);
        list = [];
      }

      function flushOrderedList() {
        if (!orderedList.length) { return; }
        parts.push(`<ol class="structured-list numbered-lines" style="list-style-type: none; padding-left: 20px;">${orderedList.map(item => `<li style="list-style: none;">${formatInlineText(item)}</li>`).join("")}</ol>`);
        orderedList = [];
      }

      function flushAll() {
        flushParagraph();
        flushList();
        flushOrderedList();
      }

      let i = 0;
      while (i < lines.length) {
        const line = lines[i].trim();
        if (!line) {
          i++;
          continue;
        }

        // Check if this line is a question definition header
        const isQuestion = /^(WHAT IS|WHAT ARE|HOW DOES|HOW DO|HOW TO|WHY DOES|WHY IS|WHY ARE|WHAT DO)\b/.test(line) && line.includes("?");
        if (isQuestion) {
          flushAll();
          const questionHeader = line;
          const bodyLines = [];
          i++;
          
          // Collect body lines until we hit a subheading or another question
          while (i < lines.length) {
            const nextLine = lines[i].trim();
            if (!nextLine) {
              i++;
              continue;
            }
            
            const isNextQuestion = /^(WHAT IS|WHAT ARE|HOW DOES|HOW DO|HOW TO|WHY DOES|WHY IS|WHY ARE|WHAT DO)\b/.test(nextLine) && nextLine.includes("?");
            if (isNextQuestion || isSubheadingLine(nextLine)) {
              break;
            }
            
            bodyLines.push(nextLine);
            i++;
          }
          
          parts.push(`
            <div class="mini-box what-is-definition">
              <div class="mini-box-header">
                <svg class="mini-box-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                <h4>${formatInlineText(questionHeader)}</h4>
              </div>
              <p>${bodyLines.map(formatInlineText).join(" ")}</p>
            </div>
          `);
          continue;
        }

        const dashedMatch = line.match(/^--+\\s*([^-]+?)\\s*-*$/);
        if (dashedMatch) {
          flushAll();
          parts.push(`<h4 class="text-subhead">${formatInlineText(dashedMatch[1].trim())}</h4>`);
          i++;
          continue;
        }

        const opListMatch = line.match(/^([+\\-*\\/])\\s+(.+)$/);
        if (opListMatch) {
          flushParagraph();
          flushOrderedList();
          const symbol = opListMatch[1];
          const text = opListMatch[2].trim();
          if (symbol === "-" && line.startsWith("- ") && line.charAt(2) !== " ") {
            list.push(text);
          } else {
            list.push(`${symbol} ${text}`);
          }
          i++;
          continue;
        }

        if (/^\\d+\\.\\s+/.test(line)) {
          const isNumberedHeading = /^\\d+\\.\\s+[A-Z0-9\\s"'-]+$/.test(line) && line.length < 50;
          if (isNumberedHeading) {
            flushAll();
            parts.push(`<h4 class="text-subhead">${formatInlineText(line)}</h4>`);
            i++;
            continue;
          }

          flushParagraph();
          flushList();
          orderedList.push(line);
          i++;
          continue;
        }

        flushList();
        flushOrderedList();

        if (/^Analogy:\\s*/i.test(line)) {
          flushParagraph();
          const analogyHeader = line;
          const analogyLines = [];
          i++;
          while (i < lines.length) {
            const nextLine = lines[i].trim();
            if (!nextLine) {
              i++;
              continue;
            }
            const isNextQuestion = /^(WHAT IS|WHAT ARE|HOW DOES|HOW DO|HOW TO|WHY DOES|WHY IS|WHY ARE|WHAT DO)\b/i.test(nextLine) && nextLine.includes("?");
            if (/^Analogy:\\s*/i.test(nextLine) || isNextQuestion || isSubheadingLine(nextLine) || (nextLine.startsWith("- ") && nextLine.charAt(2) !== " ") || /^\\d+\\.\\s+/.test(nextLine)) {
              break;
            }
            analogyLines.push(nextLine);
            i++;
          }
          const fullAnalogy = [analogyHeader, ...analogyLines].join(" ");
          parts.push(`<div class="text-analogy">${formatInlineText(fullAnalogy)}</div>`);
          continue;
        }

        if (line.includes("->") || /^\\|/.test(line) || line === "v") {
          flushParagraph();
          parts.push(`<div class="text-flow">${formatInlineText(line)}</div>`);
          i++;
          continue;
        }

        if (isSubheadingLine(line)) {
          flushParagraph();
          parts.push(`<h4 class="text-subhead">${formatInlineText(line.replace(/:$/, ""))}</h4>`);
          i++;
          continue;
        }

        paragraph.push(line);
        i++;
      }

      flushAll();
      return `<div class="structured-text">${parts.join("")}</div>`;
    }

    function formatTextBlock(text) {
      const chunks = text.split(/\\n\\n+/).map(chunk => chunk.trim()).filter(Boolean);
      if (!chunks.length) { return ""; }
      return chunks.map(chunk => {
        const lines = chunk.split("\\n").map(line => line.trim()).filter(Boolean);
        if (!lines.length) { return ""; }
        return renderStructuredLines(lines);
      }).join("");
    }

    function applyTheme(theme, persist = true) {
      const next = theme === "night" ? "night" : "day";
      document.body.setAttribute("data-theme", next);
      refs.themeToggle.innerHTML = next === "night" 
        ? `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`
        : `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

      if (persist) {
        localStorage.setItem("craftwai-theme", next);
        updateProgress({ theme: next }, false).catch(() => {});
      }
    }



    function renderCourseSummary() {
      refs.courseTitle.textContent = state.course.title;
      refs.courseSubtitle.textContent = state.course.subtitle;
      const completed = state.progress.completed.length;
      const total = state.lessons.length || 1;
      const percent = Math.round((completed / total) * 100);
      refs.courseStats.innerHTML = `
        <div class="stat"><span class="value">${completed}</span><span class="label">Done</span></div>
        <div class="stat"><span class="value">${state.lessons.length}</span><span class="label">Lessons</span></div>
        <div class="stat"><span class="value">${state.course.estimated_duration}</span><span class="label">Duration</span></div>
      `;
      refs.progressFill.style.width = `${percent}%`;
      refs.courseStatus.textContent = `${percent}% complete - comfortable pace for beginners.`;
    }

    function renderLessonList() {
      const completedSet = new Set(state.progress.completed);
      
      // Group lessons by module
      const modules = {};
      state.lessons.forEach(lesson => {
        const modId = lesson.module ? lesson.module.id : "01";
        const modTitle = lesson.module ? lesson.module.title : "Python Programming";
        if (!modules[modId]) {
          modules[modId] = { id: modId, title: modTitle, lessons: [] };
        }
        modules[modId].lessons.push(lesson);
      });

      // Render grouped layout
      refs.lessonList.innerHTML = Object.values(modules).map(mod => {
        const isModuleActive = mod.lessons.some(lesson => lesson.slug === state.currentLessonSlug);
        const collapseClass = isModuleActive ? "" : "collapsed";
        const arrowRotation = isModuleActive ? "rotate(0deg)" : "rotate(-90deg)";

        const lessonsHtml = mod.lessons.map(lesson => {
          const activeClass = lesson.slug === state.currentLessonSlug ? "active" : "";
          const displayNum = `${parseInt(mod.id)}.${parseInt(lesson.number)}`;
          const isCompleted = completedSet.has(lesson.slug);
          
          let doneBadge = isCompleted 
            ? `<span class="badge done"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> Done</span>` 
            : `<span class="badge">In progress</span>`;

          return `
            <button class="lesson-item ${activeClass}" data-slug="${escapeHtml(lesson.slug)}">
              <div class="lesson-top">
                <strong>Lesson ${escapeHtml(displayNum)}</strong>
                ${doneBadge}
              </div>
              <div class="lesson-title" style="font-family: var(--font-heading); font-weight: 700; margin-top: 4px; line-height: 1.25;">${escapeHtml(lesson.title)}</div>
              <div class="meta" style="font-size: 0.76rem; color: var(--muted); margin-top: 2px;">${escapeHtml(lesson.difficulty)} • ${escapeHtml(lesson.estimated_time)} • ${lesson.section_count} steps</div>
            </button>
          `;
        }).join("");

        return `
          <div class="module-group ${collapseClass}" data-module-id="${mod.id}">
            <div class="module-header" style="display: flex; justify-content: space-between; align-items: center;">
              <div style="flex: 1; padding-right: 8px;">
                <span class="module-eyebrow">Module ${parseInt(mod.id)}</span>
                <h4 class="module-title">${escapeHtml(mod.title)}</h4>
              </div>
              <svg class="module-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="transition: transform 0.25s ease; transform: ${arrowRotation}; color: var(--muted); flex-shrink: 0;"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
            <div class="module-lessons">
              ${lessonsHtml}
            </div>
          </div>
        `;
      }).join("");

      // Bind Collapsible click events to module headers
      refs.lessonList.querySelectorAll(".module-header").forEach(header => {
        header.addEventListener("click", () => {
          const group = header.closest(".module-group");
          group.classList.toggle("collapsed");
          
          const arrow = header.querySelector(".module-arrow");
          if (arrow) {
            if (group.classList.contains("collapsed")) {
              arrow.style.transform = "rotate(-90deg)";
            } else {
              arrow.style.transform = "rotate(0deg)";
            }
          }
        });
      });

      refs.lessonList.querySelectorAll(".lesson-item").forEach(button => {
        button.addEventListener("click", async () => { await loadLesson(button.dataset.slug); });
      });

      // Smoothly scroll the active lesson item into view within the syllabus list
      setTimeout(() => {
        const activeItem = refs.lessonList.querySelector(".lesson-item.active");
        if (activeItem) {
          activeItem.scrollIntoView({ behavior: "auto", block: "nearest" });
        }
      }, 50);
    }

    function updateNavigationButtons() {
      const index = state.lessons.findIndex(lesson => lesson.slug === state.currentLessonSlug);
      refs.prevLessonBtn.disabled = index <= 0;
      refs.nextLessonBtn.disabled = index < 0 || index >= state.lessons.length - 1;
      const isDone = state.progress.completed.includes(state.currentLessonSlug);
      refs.markCompleteBtn.innerHTML = isDone 
        ? `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg> <span>Mark Lesson Incomplete</span>`
        : `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> <span>Mark Lesson Complete</span>`;
    }

    function renderHero(lesson) {
      const goals = (lesson.learning_goals || []).map(goal => `<span class="goal">${escapeHtml(goal)}</span>`).join("");
      const anchor = lesson.real_life_anchor ? `
        <div class="hero-callout">
          <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: var(--accent); margin-bottom: 4px;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            Real-life anchor
          </div>
          ${escapeHtml(lesson.real_life_anchor)}
        </div>
      ` : "";
      refs.hero.innerHTML = `
        <p class="eyebrow">Lesson ${escapeHtml(lesson.number)} • ${escapeHtml(lesson.difficulty)} • ${escapeHtml(lesson.estimated_time)}</p>
        <h1>${escapeHtml(lesson.title)}</h1>
        <p>${escapeHtml(lesson.plain_intro)}</p>
        ${anchor}
        <div class="goal-wrap">${goals || '<span class="goal">Practical progress</span>'}</div>
      `;
    }

    function renderSections(lesson) {
      refs.sectionList.innerHTML = lesson.sections.map(section => {
        const simpleWordsBox = section.show_plain_explanation ? `
          <div class="mini-box simple-words">
            <div class="mini-box-header">
              <svg class="mini-box-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
              <h4>In simple words</h4>
            </div>
            <p>${escapeHtml(section.plain_explanation)}</p>
          </div>
        ` : "";

        const realLifeBox = section.real_life_example ? `
          <div class="mini-box real-life">
            <div class="mini-box-header">
              <svg class="mini-box-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
              <h4>Real-life example</h4>
            </div>
            <p>${escapeHtml(section.real_life_example)}</p>
          </div>
        ` : "";

        let codeIndex = 0;
        const bodyBlocks = section.blocks.map(block => {
          if (block.type === "text") {
            const wideClass = block.content.length > 700 ? " wide-text" : "";
            return `<div class="text-block${wideClass}">${formatTextBlock(block.content)}</div>`;
          }

          if (block.type !== "code") {
            return "";
          }

          if (block.is_repeated) {
            return `<div class="repeat-note">Repeated example detected. Focus on the new explanation in this step instead of re-reading identical code.</div>`;
          }

          codeIndex += 1;
          const conceptNotes = Array.isArray(block.concept_notes) && block.concept_notes.length ? `
            <div class="mini-box code-concepts">
              <div class="mini-box-header">
                <svg class="mini-box-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 18l6-6-6-6"/><path d="M8 6l-6 6 6 6"/></svg>
                <h4>Before you run it</h4>
              </div>
              <ul>${block.concept_notes.map(note => `<li>${formatConceptText(note)}</li>`).join("")}</ul>
            </div>
          ` : "";

          const runnerPanel = block.runnable ? `
            <div class="runner-panel" data-block-id="${escapeHtml(block.id)}">
              <div class="runner-header">
                <div class="runner-title">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  Try it here
                </div>
                <button class="btn primary run-btn" type="button" style="padding: 7px 12px;">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                  <span>Run</span>
                </button>
              </div>
              <textarea class="runner-editor" spellcheck="false">${escapeHtml(block.content)}</textarea>
              <pre class="runner-output">Output will appear here.</pre>
            </div>
          ` : "";

          return `
            ${conceptNotes}
            <details class="code">
              <summary>
                <div class="summary-left">
                  <div class="terminal-dots">
                    <div class="terminal-dot red"></div>
                    <div class="terminal-dot yellow"></div>
                    <div class="terminal-dot green"></div>
                  </div>
                  <span>Show Python Example ${codeIndex}</span>
                </div>
                <div class="summary-right">
                  <span class="tech-badge">python</span>
                  <svg class="chevron-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
                </div>
              </summary>
              <div class="code-shell">
                <pre><code>${escapeHtml(block.content)}</code></pre>
                <button class="copy-btn" type="button">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                  Copy
                </button>
              </div>
            </details>
            ${runnerPanel}
          `;
        }).join("");

        return `
          <article class="section-card section-type-${escapeHtml(section.type)}" id="section-${section.id}">
            <div class="section-header">
              <h3>${escapeHtml(section.title)}</h3>
              <span class="step-pill pill-${section.type}">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;">${getPillIcon(section.type)}</svg>
                Step ${section.id} • ${escapeHtml(sectionTypeLabel(section.type))}
              </span>
            </div>

            ${simpleWordsBox}
            ${realLifeBox}

            ${bodyBlocks}
          </article>
        `;
      }).join("");
    }

    async function fetchLesson(slug) {
      if (state.lessonCache.has(slug)) {
        return state.lessonCache.get(slug);
      }

      const response = await fetch(`/api/lesson/${encodeURIComponent(slug)}`);
      if (!response.ok) {
        throw new Error("Could not load lesson.");
      }

      const payload = await response.json();
      state.lessonCache.set(slug, payload.lesson);
      return payload.lesson;
    }

    async function loadLesson(slug, focusSectionId = null) {
      const lesson = await fetchLesson(slug);
      state.currentLessonSlug = lesson.slug;

      renderHero(lesson);
      renderSections(lesson);
      renderLessonList();
      updateNavigationButtons();

      updateProgress({ last_lesson: slug }, false).catch(() => {});

      if (focusSectionId) {
        const target = document.getElementById(`section-${focusSectionId}`);
        if (target) {
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }
    }

    async function updateProgress(payload, rerender = true) {
      const response = await fetch("/api/progress", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        return;
      }

      const data = await response.json();
      state.progress = data.progress;

      if (rerender) {
        renderCourseSummary();
        renderLessonList();
        updateNavigationButtons();
      }
    }

    async function toggleCompletion() {
      if (!state.currentLessonSlug) {
        return;
      }

      const isDone = state.progress.completed.includes(state.currentLessonSlug);
      if (isDone) {
        await updateProgress({ uncomplete_lesson: state.currentLessonSlug, last_lesson: state.currentLessonSlug });
      } else {
        await updateProgress({ complete_lesson: state.currentLessonSlug, last_lesson: state.currentLessonSlug });
      }
    }

    async function moveLesson(offset) {
      const index = state.lessons.findIndex(lesson => lesson.slug === state.currentLessonSlug);
      if (index < 0) {
        return;
      }
      const target = state.lessons[index + offset];
      if (!target) {
        return;
      }
      await loadLesson(target.slug);
    }

    async function performSearch(query) {
      if (query.trim().length < 2) {
        refs.searchResults.innerHTML = '<p class="empty" style="margin: 0; padding: 10px; font-size: 0.88rem; color: var(--muted); text-align: center;">Type at least 2 letters to search.</p>';
        refs.searchResults.classList.remove("active");
        return;
      }

      refs.searchResults.classList.add("active");
      refs.searchResults.innerHTML = '<p class="empty" style="margin: 0; padding: 10px; font-size: 0.88rem; color: var(--muted); text-align: center;">Searching...</p>';

      const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      if (!response.ok) {
        refs.searchResults.innerHTML = '<p class="empty" style="margin: 0; padding: 10px; font-size: 0.88rem; color: var(--muted); text-align: center;">Search unavailable.</p>';
        return;
      }

      const data = await response.json();
      if (!data.results.length) {
        refs.searchResults.innerHTML = '<p class="empty" style="margin: 0; padding: 10px; font-size: 0.88rem; color: var(--muted); text-align: center;">No matching section found.</p>';
        return;
      }

      refs.searchResults.innerHTML = data.results.map(result => `
        <button class="search-item" data-lesson="${escapeHtml(result.lesson_slug)}" data-section="${result.section_id}" style="margin-bottom: 8px;">
          <div class="title" style="font-family: var(--font-heading); font-weight: 700; font-size: 0.88rem; color: var(--accent);">${escapeHtml(result.lesson_title)} • ${escapeHtml(result.section_title)}</div>
          <div class="snippet" style="font-size: 0.82rem; color: var(--muted); margin-top: 4px; line-height: 1.4;">${escapeHtml(result.snippet)}</div>
        </button>
      `).join("");

      refs.searchResults.querySelectorAll(".search-item").forEach(button => {
        button.addEventListener("click", async () => {
          await loadLesson(button.dataset.lesson, Number(button.dataset.section));
          refs.searchResults.classList.remove("active");
          refs.searchInput.value = ""; // Clear input on selection
        });
      });
    }

    function bindEvents() {
      refs.themeToggle.addEventListener("click", () => {
        const current = document.body.getAttribute("data-theme");
        applyTheme(current === "night" ? "day" : "night");
      });

      refs.markCompleteBtn.addEventListener("click", async () => {
        await toggleCompletion();
      });

      refs.prevLessonBtn.addEventListener("click", async () => {
        await moveLesson(-1);
      });

      refs.nextLessonBtn.addEventListener("click", async () => {
        await moveLesson(1);
      });

      refs.searchInput.addEventListener("input", event => {
        if (searchTimer) {
          clearTimeout(searchTimer);
        }
        const value = event.target.value;
        searchTimer = setTimeout(() => {
          performSearch(value).catch(() => {});
        }, 180);
      });

      // Close search results overlay when clicking outside
      document.addEventListener("click", event => {
        if (!event.target.closest(".search-wrap")) {
          refs.searchResults.classList.remove("active");
        }
      });

      // Close search results overlay on Escape key
      refs.searchInput.addEventListener("keydown", event => {
        if (event.key === "Escape") {
          refs.searchResults.classList.remove("active");
          refs.searchInput.blur();
        }
      });

      refs.sectionList.addEventListener("click", async event => {
        const target = event.target;
        if (!(target instanceof HTMLElement)) {
          return;
        }

        const runBtn = target.closest(".run-btn");
        if (runBtn) {
          const panel = runBtn.closest(".runner-panel");
          const editor = panel?.querySelector(".runner-editor");
          const output = panel?.querySelector(".runner-output");
          const blockId = panel?.dataset.blockId || "";
          if (!panel || !(editor instanceof HTMLTextAreaElement) || !output) {
            return;
          }

          const oldHtml = runBtn.innerHTML;
          runBtn.setAttribute("disabled", "disabled");
          runBtn.innerHTML = `<span>Running...</span>`;
          output.classList.remove("error");
          output.textContent = "Running...";

          try {
            const response = await fetch("/api/run-code", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ block_id: blockId, source: editor.value }),
            });
            const data = await response.json();
            if (!response.ok) {
              throw new Error(data.error || "Run failed.");
            }
            const result = data.result || {};
            const stdout = result.stdout || "";
            const stderr = result.stderr || "";
            output.classList.toggle("error", !result.ok);
            output.textContent = [stdout, stderr].filter(Boolean).join("\\n") || "✨ Success! (No output to display)\\n\\nNote: The code ran without errors! If you only defined functions or variables without calling print(), you won't see output. Try adding print() statements or calling the functions yourself!";
          } catch (error) {
            output.classList.add("error");
            output.textContent = error.message || "Run failed.";
          } finally {
            runBtn.removeAttribute("disabled");
            runBtn.innerHTML = oldHtml;
          }
          return;
        }

        const copyBtn = target.closest(".copy-btn");
        if (!copyBtn) {
          return;
        }

        const code = copyBtn.closest(".code-shell")?.querySelector("code")?.innerText || "";
        if (!code) {
          return;
        }

        try {
          await navigator.clipboard.writeText(code);
          const oldHtml = copyBtn.innerHTML;
          copyBtn.innerHTML = `
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            <span style="color: #10b981;">Copied!</span>
          `;
          setTimeout(() => {
            copyBtn.innerHTML = oldHtml;
          }, 1200);
        } catch (_) {
          copyBtn.textContent = "Copy failed";
        }
      });

      // Sidebar Toggles
      const layoutEl = document.querySelector(".layout");
      document.getElementById("toggleLeftBtn").addEventListener("click", () => {
        layoutEl.classList.toggle("hide-left");
      });
    }

    async function bootstrap() {
      bindEvents();

      const response = await fetch("/api/manifest");
      if (!response.ok) {
        throw new Error("Unable to load manifest.");
      }

      const data = await response.json();
      state.course = data.course;
      state.lessons = data.lessons;
      state.progress = data.progress;
      state.benchmarks = data.benchmarks;

      renderCourseSummary();

      const preferredTheme = state.progress.theme || localStorage.getItem("craftwai-theme") || "day";
      applyTheme(preferredTheme, false);

      const startSlug = state.progress.last_lesson && state.lessons.some(lesson => lesson.slug === state.progress.last_lesson)
        ? state.progress.last_lesson
        : state.lessons[0]?.slug;

      if (startSlug) {
        await loadLesson(startSlug);
      }

      refs.searchResults.innerHTML = '<p class="empty">Type at least 2 letters to search.</p>';

      // Auto-hide panels on narrow screens
      const layoutEl = document.querySelector(".layout");
      if (window.innerWidth < 1300) {
        layoutEl.classList.add("hide-right");
      }
      if (window.innerWidth < 1000) {
        layoutEl.classList.add("hide-left");
      }
    }

    bootstrap().catch(error => {
      let debugInfo = "";
      try {
        for (const [key, value] of Object.entries(refs)) {
          debugInfo += `<li><strong>refs.${key}</strong>: ${value ? "Found (" + value.tagName + ")" : "<span style='color: #ef4444;'>NULL</span>"}</li>`;
        }
      } catch (e) {
        debugInfo = `Failed to introspect refs: ${e.message}`;
      }
      
      refs.hero.innerHTML = `
        <h1 style="color: var(--accent); margin-bottom: 12px;">Could not start UI</h1>
        <p style="font-size: 1.1rem; font-weight: 500; margin-bottom: 16px;">Error: ${escapeHtml(error.message)}</p>
        <div style="text-align: left; background: var(--bg-card); padding: 16px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 16px; max-width: 100%;">
          <h3 style="margin-bottom: 8px; font-family: var(--font-heading);">DOM References Status:</h3>
          <ul style="padding-left: 20px; line-height: 1.6; margin: 0; font-size: 0.9rem;">
            ${debugInfo}
          </ul>
        </div>
        <div style="text-align: left; background: var(--bg-card); padding: 16px; border-radius: 8px; border: 1px solid var(--border); overflow-x: auto; max-width: 100%;">
          <h3 style="margin-bottom: 8px; font-family: var(--font-heading);">Stack Trace:</h3>
          <pre style="font-family: monospace; font-size: 0.8rem; margin: 0; line-height: 1.4; color: var(--muted);">${escapeHtml(error.stack || error.message)}</pre>
        </div>
      `;
    });
  </script>
</body>
</html>
"""


# -----------------------------------------------------------------------------
# HTTP handler
# -----------------------------------------------------------------------------

def run_python_snippet(source: str) -> dict[str, Any]:
    runnable, reason = analyze_runnable_code(source)
    if not runnable:
        return {
            "ok": False,
            "stdout": "",
            "stderr": f"This snippet is not enabled for inline running: {reason}.",
            "returncode": None,
            "timed_out": False,
        }

    with tempfile.TemporaryDirectory(prefix="craftwai-run-") as tmpdir:
        try:
            completed = subprocess.run(
                [sys.executable, "-I", "-u", "-c", source],
                cwd=tmpdir,
                text=True,
                capture_output=True,
                timeout=RUNNER_TIMEOUT_SECONDS,
                env={"PYTHONIOENCODING": "utf-8"},
            )
        except subprocess.TimeoutExpired as exc:
            return {
                "ok": False,
                "stdout": (exc.stdout or "")[:20_000],
                "stderr": f"Stopped after {RUNNER_TIMEOUT_SECONDS} seconds. Check for a very large loop or blocking code.",
                "returncode": None,
                "timed_out": True,
            }

    return {
        "ok": completed.returncode == 0,
        "stdout": completed.stdout[:20_000],
        "stderr": completed.stderr[:20_000],
        "returncode": completed.returncode,
        "timed_out": False,
    }


class CourseRequestHandler(BaseHTTPRequestHandler):
    server_version = "Py4AIWebRunner/2.0"

    course_payload: dict[str, Any] = {}
    lessons: list[dict[str, Any]] = []
    lesson_by_slug: dict[str, dict[str, Any]] = {}
    runnable_code_by_id: dict[str, str] = {}
    progress_store: Optional[ProgressStore] = None

    def log_message(self, format: str, *args: Any) -> None:
        # Quiet logs: keeps terminal output clean and avoids repeated lines.
        return

    def send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_not_found(self) -> None:
        self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

    def read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON payload")

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path

        if route in {"/", "/index.html"}:
            self.send_html(INDEX_HTML)
            return

        if route == "/api/manifest":
            if not self.progress_store:
                self.send_json({"error": "Progress store unavailable"}, HTTPStatus.INTERNAL_SERVER_ERROR)
                return
            self.send_json(
                {
                    "course": self.course_payload["course"],
                    "lessons": self.course_payload["manifest_lessons"],
                    "benchmarks": UI_BENCHMARKS,
                    "progress": self.progress_store.snapshot(),
                }
            )
            return

        if route.startswith("/api/lesson/"):
            slug = route[len("/api/lesson/") :].strip()
            lesson = self.lesson_by_slug.get(slug)
            if not lesson:
                self.send_not_found()
                return
            self.send_json({"lesson": lesson})
            return

        if route == "/api/search":
            query = parse_qs(parsed.query).get("q", [""])[0]
            results = search_lessons(query, self.lessons)
            self.send_json({"query": query, "results": results})
            return

        if route == "/healthz":
            self.send_json({"ok": True})
            return

        self.send_not_found()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path

        if route == "/api/run-code":
            try:
                payload = self.read_json_body()
            except ValueError as exc:
                self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
                return

            block_id = str(payload.get("block_id", "")).strip()
            original = self.runnable_code_by_id.get(block_id)
            if not original:
                self.send_json({"error": "This code block is not enabled for inline running."}, HTTPStatus.BAD_REQUEST)
                return

            source = str(payload.get("source", original))
            result = run_python_snippet(source)
            self.send_json({"result": result})
            return

        if route != "/api/progress":
            self.send_not_found()
            return

        if not self.progress_store:
            self.send_json({"error": "Progress store unavailable"}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        try:
            payload = self.read_json_body()
        except ValueError as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return

        try:
            progress = self.progress_store.update(payload)
        except ValueError as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return
        except Exception:
            self.send_json({"error": "Failed to update progress"}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        self.send_json({"progress": progress})


# -----------------------------------------------------------------------------
# Bootstrapping
# -----------------------------------------------------------------------------

def find_free_port(host: str, start: int) -> int:
    for port in range(start, start + 120):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((host, port))
            except OSError:
                continue
            return port
    raise RuntimeError("No free port available in the expected range.")


def build_course_payload(lessons: list[dict[str, Any]]) -> dict[str, Any]:
    total_minutes = sum(minutes_from_text(lesson["estimated_time"]) for lesson in lessons)

    manifest_lessons = [
        {
            "number": lesson["number"],
            "slug": lesson["slug"],
            "filename": lesson["filename"],
            "title": lesson["title"],
            "difficulty": lesson["difficulty"],
            "estimated_time": lesson["estimated_time"],
            "section_count": lesson["section_count"],
            "code_block_count": lesson["code_block_count"],
            "learning_goals": lesson["learning_goals"],
            "plain_intro": lesson["plain_intro"],
            "module": lesson.get("module", {"id": "01", "title": "Python Programming"}),
        }
        for lesson in lessons
    ]

    return {
        "course": {
            "title": "Craft with AI",
            "subtitle": "Build enterprise-grade AI systems end-to-end, with the help of AI",
            "lesson_count": len(lessons),
            "estimated_duration": format_duration(total_minutes),
            "ui_strategy": "guided path + outcomes clarity + micro-step momentum",
        },
        "manifest_lessons": manifest_lessons,
    }


def main() -> None:
    lesson_paths = discover_lessons()
    if not lesson_paths:
        print("No lesson files found next to course_runner.py")
        sys.exit(1)

    valid, reason = verify_course_integrity(lesson_paths)
    if not valid:
        print_integrity_failure(reason)
        sys.exit(1)

    lessons = [parse_lesson_file(path) for path in lesson_paths]
    lessons.sort(key=lambda item: (int(item["module"]["id"]), int(item["number"])))

    runnable_code_by_id = {
        block["id"]: block["content"]
        for lesson in lessons
        for section in lesson["sections"]
        for block in section["blocks"]
        if block["type"] == "code" and block.get("runnable") and block.get("id")
    }

    lesson_by_slug = {lesson["slug"]: lesson for lesson in lessons}
    filename_to_slug = {lesson["filename"]: lesson["slug"] for lesson in lessons}
    slug_to_filename = {lesson["slug"]: lesson["filename"] for lesson in lessons}
    valid_slugs = set(lesson_by_slug.keys())
    lesson_order = [lesson["slug"] for lesson in lessons]

    progress_store = ProgressStore(valid_slugs, filename_to_slug, slug_to_filename, lesson_order)
    payload = build_course_payload(lessons)

    CourseRequestHandler.course_payload = payload
    CourseRequestHandler.lessons = lessons
    CourseRequestHandler.lesson_by_slug = lesson_by_slug
    CourseRequestHandler.runnable_code_by_id = runnable_code_by_id
    CourseRequestHandler.progress_store = progress_store

    port = find_free_port(HOST, START_PORT)
    server = ThreadingHTTPServer((HOST, port), CourseRequestHandler)
    url = f"http://{HOST}:{port}"

    print()
    print("=" * 72)
    print("Craft with AI - Browser Runner")
    print("=" * 72)
    print(f"Local course server: {url}")
    print("A browser tab will open automatically.")
    print("Press Ctrl+C in this terminal to stop the runner.")
    print("=" * 72)
    print()

    try:
        webbrowser.open(url, new=2)
    except Exception:
        print("Could not open the browser automatically.")
        print(f"Open this URL manually: {url}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down browser runner...")
    finally:
        server.server_close()
        print("Runner stopped.")


if __name__ == "__main__":
    main()
