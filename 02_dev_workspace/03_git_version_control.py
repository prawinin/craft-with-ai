# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 21: Git & Version Control (Handling Conflicts)
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - Git basics: Commits, staging, branches, and commits history
    - Git branching model (branch, checkout, switch)
    - Pushing and pulling code from remote platforms (GitHub, GitLab)
    - Handling Git Merge Conflicts (the absolute kryptonite of AI assistants)
    - A step-by-step manual resolution playbook

  Why this matters for AI:
    When you build code with AI, you will move fast. You'll generate entire features
    in seconds. If you aren't committing your code in clean Git states, you run
    a high risk of overwriting working code with a bad AI suggestion.
    Furthermore, AI agents frequently generate merge conflicts when multiple agents
    work on the same project. You must know how to clean these up.

  Estimated time: 25 minutes

===============================================================================
"""

# === THE VERSION CONTROL FLOW ===============================================
#
# WHAT IS VERSION CONTROL (VCS)?
#   Imagine you are writing a book, but instead of hit-or-miss manual saving, you have a
#   magical typewriter that remembers every single keystroke you make. At any point,
#   you can tell the typewriter, "Let's travel back in time to last Tuesday at 2 PM when
#   I was writing Chapter 3," and it instantly restores your pages. Git is that magical
#   typewriter for programmers, keeping track of every edit in your code.
#
# WHAT IS A REPOSITORY (REPO)?
#   A repository (or "repo") is simply a project folder that is being tracked by Git.
#   It contains all your source files, resources, and a secret hidden database (stored in the
#   `.git` folder) that logs every single change and commit made since the project was created.
#
# WHAT IS A COMMIT?
#   A commit is a digital snapshot of your project's current state. Think of it like
#   saving your progress in a video game before entering a dangerous boss fight. If your new
#   code blows up or the AI generates code that breaks the app, you can instantly load the
#   previous "saved game" (commit) and pretend nothing went wrong.
#
# Git takes snapshots of your codebase. Instead of saving "main_v1.py", "main_v2_final.py",
# Git tracks incremental changes.
#
# The 3 Git States:
#   1. Working Directory - Files you are editing right now.
#   2. Staging Area      - Files prepared for a snapshot (git add).
#   3. Local Repository  - The saved snapshot database (git commit).
#
# Standard workflow:
#   git status        - Check current file states
#   git add file.py   - Stage file changes
#   git commit -m "m" - Snapshot changes with a descriptive message
#   git log --oneline - View history of snapshots in a single-line summary

# print("--- 1. VERSION CONTROL SYSTEM FLOW ---")
# Git operates via shell commands. Let's look at what git commands represent conceptually.
print("Staging (git add) -> Snapshotting (git commit) -> Sharing (git push)")


# === BRANCHING AND TEAMS =====================================================
#
# WHAT IS A BRANCH?
#   A branch is like a parallel universe or a "multiverse" timeline for your codebase.
#   Normally, your stable code lives on the main timeline (the `main` branch). If you want
#   to test a crazy new AI feature, you split off into a parallel branch. You can experiment,
#   break things, and rebuild without affecting the main timeline. Once your feature is
#   perfect, you merge it back into the main universe.
#
# A branch is a parallel path of development. It lets you build new features
# without breaking the stable, working "main" branch code.
#
# Commands:
#   git branch feature-auth       - Create a new branch named 'feature-auth'
#   git checkout feature-auth     - Switch active branch to 'feature-auth'
#   git checkout -b feature-db    - Shortcut: Create and switch instantly
#   git merge feature-auth        - Merge feature branch back into current branch

# print("\n--- 2. THE GIT BRANCHING PIPELINE ---")
print("main (stable) ────────┬─────────────────────────► merge back into main")
print("                      └─► feature-branch (edit) ─┘")


# === UNDERSTANDING MERGE CONFLICTS ===========================================
#
# WHAT IS A MERGE CONFLICT?
#   Imagine two chefs are writing a recipe book. Chef A edits line 12 of a document to say
#   "Add 2 cups of sugar." At the same time, Chef B edits that exact same line 12 to say
#   "Add 1 pinch of salt." When they try to combine their pages, the system has no idea who
#   is right and throws a Merge Conflict. It stops and says, "Humans, you have to decide this!"
#
# WHAT IS HEAD?
#   In Git, `HEAD` is simply a pointer that says "You are currently standing here." Think of
#   it like the needle on a record player or the cursor in a text document. Whichever branch or
#   commit `HEAD` is pointing to is the active version of the codebase you see on your screen.
#
# A merge conflict happens when Git tries to combine two branches that edited
# the EXACT SAME LINE in the same file. Git doesn't know which version is the
# "correct" one, so it halts the merge and asks the human to resolve it.
#
# When this happens, Git writes special CONFLICT MARKERS directly into the file:
#
#   <<<<<<< HEAD
#   print("Welcome to the AI Platform V1")
#   =======
#   print("Welcome to the Agentic Core Platform V2")
#   >>>>>>> feature-upgrade
#
# Anatomy of the markers:
#   - <<<<<<< HEAD : Start of conflict. The code below is on your CURRENT branch.
#   - =======      : The separator dividing the two versions.
#   - >>>>>>> name : End of conflict. The code above is on the INCOMING branch.

# print("\n--- 3. PARSING MERGE CONFLICT MARKERS ---")

conflict_markup = """<<<<<<< HEAD
    # Current branch code (what you have locally right now)
    server_port = 8080
=======
    # Incoming branch code (what you are pulling or merging)
    server_port = 9000
>>>>>>> feature-upgrade"""

# Let's write a python parser to show how we extract conflict groups programmatically!
def extract_conflict_options(text):
    lines = text.split("\n")
    state = "normal"
    local_ver = []
    incoming_ver = []
    
    for line in lines:
        if line.startswith("<<<<<<<"):
            state = "local"
        elif line.startswith("======="):
            state = "incoming"
        elif line.startswith(">>>>>>>"):
            state = "normal"
        else:
            if state == "local":
                local_ver.append(line.strip())
            elif state == "incoming":
                incoming_ver.append(line.strip())
                
    return "\n".join(local_ver), "\n".join(incoming_ver)

local_code, incoming_code = extract_conflict_options(conflict_markup)
print("Conflict Resolved! Two choices available:")
print(f"  Option A (Keep Local / HEAD):\n    {local_code}")
print(f"  Option B (Keep Incoming / feature-upgrade):\n    {incoming_code}")


# === THE CONFLICT RESOLUTION PLAYBOOK ========================================
#
# How to resolve a merge conflict in 5 systematic steps:
#
# Step 1: Find all files with conflicts. Running `git status` will list them as
#         "both modified".
#
# Step 2: Open the file. Search for `<<<<<<<`.
#
# Step 3: Decide which code to keep. You can keep your version, their version,
#         or combine lines from both.
#
# Step 4: Delete the conflict markers entirely (`<<<<<<<`, `=======`, `>>>>>>>`).
#         If you leave these markers in the file, it will cause syntax errors!
#
# Step 5: Save the file. Stage the file (`git add filename.py`) and commit the
#         merge (`git commit -m "Merge resolved"`).

# print("\n--- 4. MERGE CONFLICT RESOLUTION STATUS ---")
print("1. Status Check -> 2. Locate Markers -> 3. Choose Version -> 4. Strip Markers -> 5. Commit")


# === REMOTE OPERATIONS (GITHUB / GITLAB) =======================================
#
# WHAT IS A REMOTE REPOSITORY?
#   Think of your local repository as your personal laptop, and the remote repository
#   as a Google Drive or central cloud backup (like GitHub).
#
# CORE COMMANDS:
#   `git clone <url>`         - Download a repository from the internet to your machine.
#   `git remote add origin`   - Link your local repo to a new empty cloud repository.
#   `git push -u origin main` - Upload your committed changes to the cloud.
#   `git pull`                - Download new changes from the cloud to your machine.
#
# When collaborating, always `git pull` before you start working to ensure you
# have the latest code, and `git push` when you've finished a feature branch!

# print("\n--- 5. REMOTE GIT OPERATIONS ---")
# print("  Local:  [Your Laptop] ──► `git push` ──► [GitHub (origin)]")
# print("  Remote: [GitHub]      ──► `git pull` ──► [Your Laptop]")


# === COMMON MISTAKES ==========================================================


# MISTAKE 1: Leaving Git Conflict Markers in your code
#   If you run code containing `<<<<<<< HEAD` or `=======`, Python will crash
#   with `SyntaxError: invalid syntax`. Always strip the markers!

# MISTAKE 2: Committing large datasets or node_modules to Git
#   Never commit binary datasets or environment virtual directories (.venv).
#   Create a `.gitignore` in your repository root listing files to exclude.

# MISTAKE 3: Blaming the AI for overriding commits
#   If an AI assistant generates code that conflicts with your updates, checkout
#   your files (`git checkout path/to/file`) to restore, or use branch separation.


# === EXERCISES ================================================================
#
# Exercise 1: Write a function `has_git_markers(filepath)` that reads a file and
#             returns True if it contains any Git merge conflict markers.
#
# Exercise 2: Create a sample `.gitignore` content string that ignores the `.venv`
#             folder, any `.env` files, and all JSON files inside `data/output/`.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# def has_git_markers(filepath):
#     with open(filepath, "r", encoding="utf-8") as f:
#         for line in f:
#             if line.startswith("<<<<<<< ") or line.startswith(">>>>>>> "):
#                 return True
#     return False
#
# Exercise 2:
# gitignore_rules = """.venv/
# .env
# data/output/*.json
# """


# === KEY TAKEAWAYS ============================================================
#
# - Git allows developers to work safely on parallel feature branches.
# - Merge conflicts are normal—they simply occur when same lines are edited differently.
# - Conflict markers explicitly demarcate local changes (HEAD) from incoming changes.
# - Never leave conflict markers inside code files; they must be manually cleaned.
# - Commit small changes frequently when building with AI to retain quick rollback points.
