# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 27: Containerization & Core Docker Concepts
  Difficulty: Beginner-Intermediate
===============================================================================

  What you will learn:
    - The "Works on my machine" problem and why isolation is necessary
    - Lightweight Virtualization: Containers vs. Virtual Machines (VMs)
    - OS Kernel Sharing: Namespaces and Cgroups made simple
    - Blueprints vs. Instances: What is a Docker Image vs. a Docker Container?
    - How containers prevent environment drift during model deployments

  Why this matters for AI:
    AI projects require complex, heavy native dependencies (like PyTorch, CUDA drivers,
    NumPy, or specific C++ compiled packages). Installing these globally on different
    laptops often fails. Docker packages everything into a single immutable image.
    If it runs on your laptop, it is guaranteed to run identically on AWS,
    Hugging Face Spaces, or a Kubernetes cluster.

  Estimated time: 20 minutes

===============================================================================
"""

# === THE ENVIRONMENT DRIFT PROBLEM ===========================================
#
# WHAT IS A CONTAINER?
#   Think of a container like a shipping container on a cargo ship. It wraps your application,
#   its libraries, and its system tools inside a standard protective box. No matter what country the
#   ship sails to or what cargo sits next to it, the contents of the container remain completely isolated,
#   protected, and unaffected. If your code runs inside a Docker container on your laptop, it will run
#   the exact same way on any cloud server in the world.
#
# WHAT IS A VIRTUAL MACHINE (VM)?
#   A Virtual Machine is like building an entirely separate virtual house inside your real house.
#   It virtualizes actual hardware: it has a virtual motherboard, virtual hard drives, and its own entire
#   operating system (Guest OS) sitting on top of a hypervisor. Because it simulates a whole computer,
#   VMs are very heavy, slow to boot, and consume gigabytes of memory.
#
# WHAT IS AN OS KERNEL?
#   The Kernel is the ultimate engine and brain of your operating system. It is the core software that
#   bridges the gap between your hardware (CPU, RAM, hard drives) and your software applications.
#   When a program wants to save a file or send data over the internet, it asks the Kernel to do it.
#
# Environmental drift happens when code behaves differently on different machines
# due to:
#   1. Global package mismatches (e.g. Python 3.9 on laptop, Python 3.11 on server).
#   2. OS-specific paths (e.g. C:\\Data on Windows, /data on Linux).
#   3. Missing system libraries (e.g. missing libgl1 for OpenCV graphics rendering).
#
# Docker solves this by freezing the entire environment into a single static package.

# print("--- 1. DRIFT VS. IMMUTABLE CONTAINERS ---")
print("Traditional: Developer OS (Windows) ──► Staging OS (Ubuntu) ──► [FAIL: Mismatched libs]")
print("Docker:      Container Image (Frozen Ubuntu) ──► Runs identical on ANY Host OS")


# === VIRTUAL MACHINES VS. CONTAINERS ========================================
#
# WHAT IS A NAMESPACE AND A CONTROL GROUP (CGROUP)?
#   These are isolation and limit-setting features built into the Linux OS Kernel that make containers possible:
#   - A Namespace is like giving a process a pair of "blinders" (isolation). It ensures a process can only
#     see its own files and network, making it believe it is the only program running on the computer.
#   - A Control Group (cgroup) is like a "strict parent" (resource limit). It sets hard limits on how much
#     RAM, CPU power, or disk speed a container is allowed to consume, preventing it from crashing the host!
#
# Virtual Machines (VMs):
#   - Heavyweight (Gigabytes).
#   - Each VM packages a complete Guest Operating System + Hypervisor virtualization.
#   - Slow startup (minutes) because it boots a whole virtual computer.
#
# Docker Containers:
#   - Lightweight (Megabytes).
#   - Shares the host computer's operating system kernel directly.
#   - Isolates processes using Linux Kernel features: Namespaces (who can see what)
#     and Control Groups / cgroups (who can use how much RAM/CPU).
#   - Instant startup (seconds).

# print("\n--- 2. ARCHITECTURAL VIRTUALIZATION DIFFERENCES ---")
print("  Virtual Machine Setup:           Docker Container Setup:")
print("  ┌─────────────────────────┐     ┌─────────────────────────┐")
print("  │     App / Code          │     │     App / Code          │")
print("  ├─────────────────────────┤     ├─────────────────────────┤")
print("  │     Guest OS (Heavy)    │     │     Libs / Dependencies │")
print("  ├─────────────────────────┤     ├─────────────────────────┤")
print("  │     Hypervisor          │     │     Docker Engine (OS)  │")
print("  └─────────────────────────┘     └─────────────────────────┘")


# === IMAGES VS. CONTAINERS (BLUEPRINTS VS. INSTANCES) ========================
#
# WHAT IS A DOCKER IMAGE VS. CONTAINER?
#   This is the ultimate distinction in Docker:
#   - A Docker Image is a static, read-only template. Think of it like a blueprint of a house or a recipe
#     for chocolate chip cookies. It contains all code, tools, dependencies, and settings.
#   - A Docker Container is the active, running instantiation. It is the physical house built from the blueprint,
#     or the actual cookies baked from the recipe. You can use a single Image blueprint to spin up 50
#     identical running Containers!
#
# DOCKER IMAGE:
#   - A read-only, static template.
#   - Think of it as a compiled class or a blueprint of a house.
#   - It contains all code, tools, dependencies, and settings.
#
# DOCKER CONTAINER:
#   - A running, active instance of an image.
#   - Think of it as an instantiated object of a class or the built house.
#   - You can spin up 10 identical containers from the exact same image.

# print("\n--- 3. IMAGES VS. RUNNING CONTAINERS ---")

# Let's model this distinction in Python!
class DockerImageBlueprint:
    def __init__(self, OS_base: str, installed_packages: list, cmd_to_run: str):
        self.OS_base = OS_base
        self.installed_packages = installed_packages
        self.cmd_to_run = cmd_to_run
        
    def instantiate_container(self, container_id: str, port_mapping: str):
        # Creates a running container instance from this static image template
        return DockerContainerInstance(self, container_id, port_mapping)

class DockerContainerInstance:
    def __init__(self, image: DockerImageBlueprint, container_id: str, port_mapping: str):
        self.image = image
        self.container_id = container_id
        self.port_mapping = port_mapping
        self.status = "stopped"
        
    def start(self):
        self.status = "running"
        print(f"  [Container {self.container_id}] Booted up in 0.1s!")
        print(f"  [Container {self.container_id}] Port mapped: {self.port_mapping}")
        print(f"  [Container {self.container_id}] Executing: '{self.image.cmd_to_run}' inside {self.image.OS_base} environment...")

# 1. Create a static image blueprint (Docker Image)
ai_service_image = DockerImageBlueprint(
    OS_base="python:3.10-slim",
    installed_packages=["fastapi", "torch", "pandas"],
    cmd_to_run="uvicorn main:app --host 0.0.0.0"
)

# 2. Instantiate and run three identical isolated environments (Docker Containers)
container_A = ai_service_image.instantiate_container("C-A101", "8000:8000")
container_B = ai_service_image.instantiate_container("C-B202", "8001:8000")

print("Spinning up Container A:")
container_A.start()

print("\nSpinning up Container B (Identical code, completely isolated network and process):")
container_B.start()


# === THE LAYERED FILESYSTEM ==================================================
#
# Docker images are made of layers. If you change a line of code, Docker does
# not rebuild the entire image—it only rebuilds the modified layer and caches
# the rest (FROM, WORKDIR, COPY layers). This makes rebuilds blazing fast.

# print("\n--- 4. IMAGE BUILDING LAYERS ---")
#   [Layer 4] CMD ["uvicorn", "main:app"] (Changes frequently - runs instantly)
#   [Layer 3] COPY main.py .             (Changes when you edit your code)
#   [Layer 2] RUN pip install -r req.txt  (Slow - cached unless requirements change)
#   [Layer 1] FROM python:3.10-slim       (Base OS layer - downloaded once)



# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Treating containers like persistent Virtual Machines
#   Containers are ephemeral (temporary). If a container is deleted, any files written
#   inside it are lost forever! To persist files (like databases or user logs),
#   you must use Docker Volumes to map folder paths back to the host machine.

# MISTAKE 2: Including virtual environments (.venv) inside images
#   A `.venv` folder contains binary paths compiled specifically for your host machine (Mac/Windows).
#   If you copy `.venv` into a Linux Docker container, it will fail.
#   Always ignore `.venv` via `.dockerignore` and let the Dockerfile run `pip install` inside.

# MISTAKE 3: Running containers as Root
#   By default, processes inside containers run as the privileged root user.
#   If a hacker breaches your container, they might get root access to your host machine.
#   In production, always declare a non-root user in your Dockerfile to restrict permissions.


# === EXERCISES ================================================================
#
# Exercise 1: In our Python simulation, extend `DockerContainerInstance` with a
#             `.stop()` method that switches status to "stopped" and clears port maps.
#
# Exercise 2: Contrast the start speed and memory footprint of a Virtual Machine
#             (which virtualizes hardware) vs a Container (which virtualizes processes).

# === SOLUTIONS ================================================================
#
# Exercise 1:
# # (Inside DockerContainerInstance class):
# # def stop(self):
# #     self.status = "stopped"
# #     print(f"Container {self.container_id} shut down safely.")


# === KEY TAKEAWAYS ============================================================
#
# - Docker solves "works on my machine" by unifying the system runtime layer.
# - VMs virtualize entire hardware stacks, while containers isolate process execution.
# - An image is the static immutable blueprint; a container is the live process instance.
# - Namespaces and control groups provide process-level sandboxing on Linux kernels.
# - Docker images rely on stacked caching layers to enable rapid builds and transfers.
