# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 39: Continuous Integration & GitHub Actions
  Difficulty: Intermediate-Advanced
===============================================================================

  What you will learn:
    - What is CI/CD and why manual testing and building is a production hazard
    - Automating Python quality gates using the `pytest` testing library
    - Declaring GitHub Actions Automation workflows inside `.github/workflows/`
    - Building a YAML sequence parser in Python to audit CI/CD steps
    - Automating Docker builds and pushing images to remote registries on push

  Why this matters for AI:
    When you build features rapidly with AI, it is easy to accidentally break
    existing modules or commit broken syntax. By setting up a **CI/CD pipeline**,
    GitHub automatically boots a virtual machine on every single code commit,
    installs your dependencies, runs your test suite, and builds your Docker image.
    If any check fails, it blocks the code from deploying, ensuring production health.

  Estimated time: 20 minutes

===============================================================================
"""

# === THE AUTOMATION SAFETY VALVE ============================================
#
# WHAT IS CI/CD?
#   - Continuous Integration (CI) is the practice of automatically testing your code every single time you
#     push edits to GitHub. It's like having a spelling checker automatically run on your document whenever
#     you finish writing a paragraph.
#     (Git explained in Module 2, Lesson 3 — "Git & Version Control")
#   - Continuous Delivery/Deployment (CD) is the automated follow-up: once the tests pass, a robot
#     automatically builds your container image and deploys it live to the cloud, ensuring your users
#     get your new features instantly without you having to deploy manually!
#
# WHAT ARE PIPELINES AND WORKFLOWS?
#   - A Workflow is a written instruction manual or sequence of automation jobs (like a script).
#   - A Pipeline is the actual assembly-line conveyor belt that executes that manual. Think of it like a
#     factory conveyor belt: a push on Git drops the code onto the belt, which carries it through automatic
#     washing (linting/checking), testing (pytest), packaging (Docker build), and shipping (deployment).
#
# Continuous Integration (CI):
#   - Automatically test your code every time you run `git push`.
#   - Catches integration issues before code is merged into the master branch.
#
# Continuous Deployment (CD):
#   - Automatically compiles and deploys your application once tests pass.
#   - Builds your Docker container image and pushes it to cloud registries.

# print("--- 1. THE CI/CD AUTOMATION TIMELINE ---")
print("  Git Push ──► Trigger Actions VM ──► Run tests (pytest) ──► Compile Image ──► Deploy Cloud")


# === ANATOMY OF A GITHUB ACTIONS WORKFLOW ===================================
#
# WHAT IS A RUNNER?
#   A Runner is the actual computer or virtual machine (VM) in the cloud that GitHub boots up to execute
#   your workflow steps. It's like renting a temporary workstation in a digital factory: you boot it up,
#   run your code checks on it, and then hand it back when you're done.
#
# WHAT IS AN ARTIFACT?
#   An Artifact is any file or package generated during your pipeline run that you want to keep and save
#   (like compiled binary files, testing reports, or Docker images). It's like a finished product
#   sent down the conveyor belt to the warehouse, which you can download later even after the temporary
#   runner VM is completely destroyed.
#
# GitHub Actions workflows are declared in YAML files placed inside the
# `.github/workflows/` directory in your repository.
#
# Key structural sections:
#   on:    - The trigger event (e.g. `on: push` or `on: pull_request`)
#   jobs:  - The logical groups of automation execution steps
#   runs-on:- The target runner operating system (e.g. `ubuntu-latest`)
#   steps: - The precise sequence of terminal actions and external action plugins

# print("\n--- 2. PRODUCTION ACTIONS WORKFLOW (YAML) ---")

# Let's inspect a production-grade CI/CD YAML configuration:
sample_workflow_yaml = """
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest

      - name: Run Test Suite
        run: |
          pytest tests/

      - name: Compile Docker Image
        run: |
          docker build -t app-service:latest .
"""

print(sample_workflow_yaml)


# === SIMULATING GITHUB ACTIONS PARSING =======================================
#
# Let's write an interactive pipeline interpreter in Python that parses this YAML
# configuration, extracts the execution stages, and prints out a timeline diagram
# explaining exactly what happens on GitHub servers!

# print("--- 3. PIPELINE AUTOMATION INTERPRETER ---")

def interpret_workflow_pipeline(yaml_text):
    lines = yaml_text.strip().split("\n")
    stages = []
    runs_on = "unknown"
    trigger = "unknown"
    
    current_step_name = None
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue
            
        # Detect trigger event
        if line_stripped == "push:":
            trigger = "Code Push to targeted branches"
            
        # Detect runner OS
        if line_stripped.startswith("runs-on:"):
            runs_on = line_stripped.split(":", 1)[1].strip()
            
        # Detect step names
        if line_stripped.startswith("- name:"):
            current_step_name = line_stripped.split(":", 1)[1].strip()
            stages.append(current_step_name)
            
    print(f"\nWorkflow Analysis Report:")
    print(f"  Trigger:   {trigger}")
    print(f"  Runner OS: {runs_on} Virtual Machine")
    print("\nStep Execution Sequence Map:")
    for idx, stage in enumerate(stages, start=1):
        print(f"  Step #{idx}: {stage}")
        print("    ↳ Action: Provision VM, execute logic, check exit status...")

interpret_workflow_pipeline(sample_workflow_yaml)


# === WRITING AUTOMATED TESTS WITH PYTEST =====================================
#
# For the CI/CD pipeline to catch errors, you must write tests!
# `pytest` is the standard Python test runner. It scans files matching `test_*.py`
# and runs all functions starting with `test_`.

# print("\n--- 4. MOCKING pytest LOGIC ---")

# Let's write a simple python function we want to test:
def calculate_token_cost(tokens, is_completion=True):
    rate = 0.000015 if is_completion else 0.000005
    return tokens * rate

# Here is what a pytest file (test_billing.py) looks like:
def test_calculate_token_cost():
    # Assert checks values; if it evaluates to False, the test fails!
    assert calculate_token_cost(100, is_completion=True) == 0.0015
    assert calculate_token_cost(100, is_completion=False) == 0.0005
    print("  [pytest] test_calculate_token_cost passed successfully!")

# Run the test
test_calculate_token_cost()


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Hardcoding secrets inside GitHub Action YAML files
#   Never type API keys, database passwords, or Docker registry keys directly in YAML.
#   Store them in the GitHub repository's **Settings -> Secrets and Variables -> Actions** page.
#   Retrieve them securely in the YAML using: `${{ secrets.DOCKER_PASSWORD }}`.

# MISTAKE 2: Not restricting trigger branches
#   If your YAML trigger is `on: push` without branch limitations, GitHub will run the slow,
#   expensive build suite on *every* single experiment branch you push.
#   Restrict builds to stable branches: `branches: [ main, staging ]`.

# MISTAKE 3: No caching configured in runner steps
#   By default, the GitHub VM starts completely fresh. If it runs `pip install` on every push,
#   it downloads hundreds of megabytes every build. Use caching actions (like `actions/cache`)
#   to preserve your pip virtual packages across runs, slicing build times in half.


# === EXERCISES ================================================================
#
# Exercise 1: In our Python interpreter, add a check that warns the user if the
#             workflow file does not contain a step that installs `pytest`.
#
# Exercise 2: Explain why running unit tests *before* compiling the Docker image
#             is the optimal order of operations in a CI/CD pipeline.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# # checks = [s.lower() for s in stages]
# # if not any("test" in c or "pytest" in c for c in checks):
# #     print("[WARNING] Pipeline lacks automated testing steps!")


# === KEY TAKEAWAYS ============================================================
#
# - CI/CD pipelines automate testing, quality validation, and cloud delivery.
# - GitHub Actions triggers automated workflows on code push or pull events.
# - YAML configurations declare virtual runner OS targets and step execution blocks.
# - pytest validates code behavior automatically at compilation boundaries.
# - Keep API keys and credentials secure by using GitHub Actions Secrets variables.
