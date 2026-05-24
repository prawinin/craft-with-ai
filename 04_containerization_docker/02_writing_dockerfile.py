# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 28: Writing a Dockerfile & Cache Optimization
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - The structural directives of a Dockerfile (FROM, WORKDIR, COPY, RUN, ENV, EXPOSE, CMD)
    - Optimizing base images (using python:3.10-slim instead of full bulky base images)
    - Cache Layering: Organizing commands to prevent dependency rebuilds
    - Building a programmatic Dockerfile Auditor in Python to check for optimization bugs
    - Creating and using `.dockerignore` files to keep images lean

  Why this matters for AI:
    AI libraries (like Pandas, NumPy, or transformers) are massive. A poorly written
    Dockerfile that reinstalls these packages every time you edit a single line
    of code will take 10 minutes to build and upload. By mastering layer caching,
    your Docker image rebuilds will compile in under 3 seconds!

  Estimated time: 25 minutes

===============================================================================
"""

# === THE DIRECTIVES CHEAT SHEET ==============================================
#
# WHAT IS A DOCKERFILE?
#   A Dockerfile is a text recipe file containing step-by-step instructions that tell Docker how
#   to build a container image. Think of it like a list of IKEA assembly instructions: "First, start with
#   a standard wooden board (FROM base). Second, drill a few holes (RUN command). Third, screw in the legs
#   (COPY files)."
#
# WHAT IS A BASE IMAGE?
#   Think of a Base Image as a starting template or a pre-built foundation. If you are baking a cake,
#   instead of planting wheat and milling flour from scratch, you start with a box of pre-mixed cake flour
#   (Base Image). For Python apps, we usually start with `python:3.10-slim`, which has Linux and Python
#   pre-installed, so we only have to add our specific application files.
#
# A `Dockerfile` is a text document containing instructions to build a Docker image.
#
# Directives:
#   FROM    - Defines the base operating system & runtime (e.g. FROM python:3.10-slim)
#   WORKDIR - Sets the default directory inside the container (like 'cd /app')
#   COPY    - Copies files from your local computer into the container
#   RUN     - Executes command-line scripts during the BUILD phase (like 'pip install')
#   ENV     - Sets environment variables that persist inside the container
#   EXPOSE  - Documents which network port the container listens on at runtime
#   CMD     - The command executed automatically when the container STARTS

# print("--- 1. THE DOCKERFILE BUILD PIPELINE ---")
# FROM (Base) ──► WORKDIR (Folder) ──► COPY (Files) ──► RUN (Install) ──► CMD (Start)


# === DOCKER CACHING & OPTIMIZATION ===========================================
#
# WHAT IS A LAYER?
#   Docker images are built like stacks of transparent LEGO blocks. Each instruction in your Dockerfile
#   creates a new layer. If you change a step at the top of the stack (like a code edit), Docker keeps
#   all the unchanged bottom blocks intact and only swaps out the top block. This caching system makes
#   rebuilding images incredibly fast, as long as you order your steps correctly!
#
# WHAT IS THE BUILD CONTEXT?
#   Think of the Build Context as the folder on your laptop that you "pack into a suitcase" and send to
#   the Docker engine so it can build the image. If you have huge database files or virtual environments
#   (.venv) in that folder, you are packing bricks into your suitcase, making the upload incredibly slow.
#   We use a `.dockerignore` file to act like a packing filter, ensuring only necessary code files get sent!
#
# Docker executes directives top-to-bottom. Each directive creates a cached layer.
# If a layer changes, ALL layers beneath it are invalidated and must rebuild!
#
# --- THE BAD PATHWAY (No Caching) ---
#   COPY . .
#   RUN pip install -r requirements.txt
#   # BUG: If you change one character in main.py, the COPY layer changes.
#   # This invalidates the RUN layer, forcing Docker to reinstall ALL pip dependencies!
#
# --- THE GOOD PATHWAY (Optimized Caching) ---
#   COPY requirements.txt .
#   RUN pip install -r requirements.txt
#   COPY . .
#   # SUCCESS: Dependencies are installed first and cached. If you edit main.py,
#   # Docker skips the slow 'RUN pip install' and only rebuilds the final COPY layer!

# print("\n--- 2. CACHE LAYER COMPILATION MECHANICS ---")
print("  Bad:  [COPY . .] (Code changes) ──► [RUN pip install] (CACHE BROKEN - Slow Reinstall!)")
print("  Good: [COPY reqs] ──► [RUN pip install] (CACHED) ──► [COPY . .] (Instant Build!)")


# === PROGRAMMATIC DOCKERFILE STATIC AUDITOR ==================================
#
# Let's write a beautiful, interactive static auditor in Python that reads
# a Dockerfile structure, parses its lines, and warns us if it detects caching
# inefficiency or security violations!

# print("\n--- 3. STATIC DOCKERFILE AUDITOR ---")

def audit_dockerfile(dockerfile_text):
    lines = dockerfile_text.strip().split("\n")
    warnings = []
    
    # Track sequence of directives to audit caching
    directives = []
    has_requirements_copy = False
    has_generic_copy_before_pip = False
    has_non_root_user = False
    
    for idx, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        parts = line.split(None, 1)
        if not parts:
            continue
        directive = parts[0].upper()
        content = parts[1] if len(parts) > 1 else ""
        
        directives.append((idx, directive, content))
        
        # Rule 1: Bulky base images
        if directive == "FROM":
            if "alpine" not in content.lower() and "slim" not in content.lower():
                warnings.append(f"Line {idx}: Base image '{content}' might be bulky. Prefer using '-slim' or '-alpine' to shrink image size by 90%.")
                
        # Rule 2: Caching sequence audit
        if directive == "COPY":
            if "requirements.txt" in content:
                has_requirements_copy = True
            elif "." in content or "*" in content:
                # Generic copy statement (like COPY . .)
                # If this happens before requirements copy, it's a caching bug!
                if not has_requirements_copy:
                    has_generic_copy_before_pip = True
                    
        if directive == "RUN":
            if "pip install" in content and has_generic_copy_before_pip:
                warnings.append(f"Line {idx}: Caching bug! You run 'pip install' after copying all files. Separate COPY requirements.txt first to preserve cache layers.")
                
        # Rule 3: Check for root security
        if directive == "USER":
            has_non_root_user = True
            
    if not has_non_root_user:
        warnings.append("Security warning: No 'USER' directive specified. Container will execute as ROOT user (unsafe in production).")
        
    return warnings

# Let's audit a poorly written Dockerfile:
unoptimized_dockerfile = """
FROM python:3.10
WORKDIR /app
# Bug 1: Copying all files before running pip install breaks layer caching
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "main.py"]
"""

issues = audit_dockerfile(unoptimized_dockerfile)
print("Auditing unoptimized Dockerfile:")
for iss in issues:
    print(f"  [ALERT] {iss}")

# Let's audit a perfectly optimized Dockerfile:
optimized_dockerfile = """
FROM python:3.10-slim
WORKDIR /app
# Layer 1: Copy dependencies first
COPY requirements.txt .
# Layer 2: Install dependencies (highly cached!)
RUN pip install --no-cache-dir -r requirements.txt
# Layer 3: Copy code last
COPY . .
# Layer 4: Set security non-root context
RUN useradd -m appuser && chown -R appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
"""

optimized_issues = audit_dockerfile(optimized_dockerfile)
print("\nAuditing optimized Dockerfile:")
if not optimized_issues:
    print("  [SUCCESS] Dockerfile is 100% optimized! Caching layers and security checks passed.")


# === THE .dockerignore FILE ==================================================
#
# Just like a `.gitignore` excludes files from git, a `.dockerignore` file
# prevents large local files from being sent to the Docker build context.
#
# Standard `.dockerignore` content:
#   .venv/
#   .git/
#   __pycache__/
#   *.db
#   data/output/

# print("\n--- 4. THE LEAN DOCKERIGNORE SYSTEM ---")
# Keeps local build packages separated from running container environments.


# === MULTI-STAGE BUILDS ========================================================
#
# WHAT IS A MULTI-STAGE BUILD?
#   AI libraries like PyTorch or LlamaCPP often require massive C++ compilers
#   just to install. If you include those compilers in your final Docker image,
#   it might be 5GB+ in size! 
#
#   Multi-stage builds let you use one image as a "builder" (to compile everything),
#   and then copy JUST the finished files into a fresh, empty "runtime" image.
#
#   FROM python:3.10 as builder
#   RUN pip install --prefix=/install torch
#   
#   FROM python:3.10-slim as runtime
#   COPY --from=builder /install /usr/local
#   # The final image is tiny because the compilers are left behind!


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Forgetting to specify "--host 0.0.0.0" when launching FastAPI
#   By default, local API servers run on localhost (127.0.0.1). But inside a container,
#   localhost refers to the *container itself*. To let requests bridge outside the
#   container boundary, you must host bind to `0.0.0.0` (all interface adapters).

# MISTAKE 2: Not using "--no-cache-dir" during pip installations
#   Pip saves local cache files during packages compilation inside the container.
#   These cache packages are useless once built. Use `pip install --no-cache-dir`
#   to save hundreds of megabytes of image space.

# MISTAKE 3: Multiple RUN statements instead of chaining
#   Every directive creates a layer. Instead of running `RUN apt-get update` followed
#   by `RUN apt-get install`, chain them with double-ampersands:
#   `RUN apt-get update && apt-get install -y package && rm -rf /var/lib/apt/lists/*`.


# === EXERCISES ================================================================
#
# Exercise 1: In our static auditor, add a new rule that flags a warning if the
#             Dockerfile contains multiple "CMD" directives (only the last one runs!).
#
# Exercise 2: Explain why using specific image versions (like `python:3.10.12-slim`)
#             is safer than using the generic tag `python:latest` in production.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# # Count cmd directives:
# # cmd_count = sum(1 for _, dir, _ in directives if dir == "CMD")
# # if cmd_count > 1:
# #     warnings.append("Warning: Multiple CMD directives found. Only the final one will execute.")


# === KEY TAKEAWAYS ============================================================
#
# - A Dockerfile specifies the build layers required to freeze an environment.
# - Choose minimal base tags (like `-slim`) to reduce image storage overhead.
# - Order COPY directives to keep slow package compiles separated from fast code edits.
# - Use a `.dockerignore` file to omit developer virtual nodes and secret credentials.
# - Bind APIs to `0.0.0.0` inside containers to allow port forward translation.
