# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 29: Managing Containers with Docker CLI
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - Compiling blueprints into packages (docker build)
    - Running isolated processes with custom ports & environments (docker run)
    - Distinguishing between Foreground vs. Background Detached mode (-d)
    - Inspecting application runtime console streams (docker logs)
    - Accessing and debugging shells inside running containers (docker exec)
    - Cleaning up image layers and stopped containers (docker rm, rmi)

  Why this matters for AI:
    Once you freeze your FastAPI app into an image, you must interact with it.
    If the container starts but returns connection errors, you must check if
    ports are mapped incorrectly or if environment variables are missing.
    Mastering the Docker CLI lets you debug containers in staging and production
    effortlessly.

  Estimated time: 20 minutes

===============================================================================
"""

print("--- 1. THE DOCKER LIFE CYCLE COMMANDS ---")
print("  Compile (build) ──► Spin up (run) ──► Inspect (logs/exec) ──► Tear down (rm)")


# === DOCKER RUN COMMAND PARAMETERS ===========================================
#
# WHAT IS THE DOCKER DAEMON?
#   Think of the Docker Daemon as the invisible supervisor working behind the scenes on your computer.
#   When you type commands in the terminal like `docker run` or `docker build`, you are not running the
#   containers yourself. Instead, you are giving orders to the supervisor (the daemon), who takes care of
#   downloading images, managing hardware resources, and booting the isolated processes for you.
#
# WHAT IS A DOCKER REGISTRY?
#   A Docker Registry is like an App Store or GitHub but specifically for Docker Images.
#   The most famous public registry is Docker Hub. When you type `docker pull python`, the engine connects
#   to Docker Hub, finds the pre-packaged python image, and downloads it to your machine so you don't
#   have to build it from scratch!
#
# WHAT IS A DOCKER TAG?
#   A Docker Tag is a label used to version your images, acting just like Git version tags or release versions.
#   For example, in `python:3.10-slim`, `python` is the name of the image, and `3.10-slim` is the tag.
#   If you don't specify a tag when pulling or building, Docker automatically defaults to the `latest` tag,
#   which can be risky in production since "latest" changes over time!
#
# WHAT IS A DOCKER VOLUME?
#   Imagine a container is a hotel room: you can live in it and rearrange the furniture, but the moment you
#   check out (the container is stopped/deleted), the cleaning staff wipes the room completely clean for the
#   next guest (all your files are lost). A Volume is like a secure storage locker in the hotel lobby.
#   It maps a folder inside the container to a permanent folder on your host machine, ensuring your data
#   (like databases, file uploads, or logs) survives even if the container is destroyed!
#
# WHAT IS PORT BINDING?
#   Think of your computer as a large apartment building with thousands of mailboxes (Ports).
#   A container is like a sub-apartment inside apartment 301. By default, people outside the building
#   cannot mail letters directly to the sub-apartment. Port Binding is like installing a mail slot on the
#   front door: it says "forward any mail sent to Mailbox 8080 on the building's front desk directly to
#   Port 8000 inside the sub-apartment." This is written as `-p 8080:8000`.
#
# The `docker run` command is the workhorse of the Docker engine.
#
# Crucial Parameters:
#   -d                 - Run in "Detached" mode (runs in background, returns terminal focus)
#   -p [host]:[cont]   - Forward connections on host port to container port (e.g. -p 8000:8000)
#   -e [KEY]=[VAL]     - Feed environment configurations at startup (e.g. -e API_KEY="sk-...")
#   --name [my-app]    - Assign a human-readable identifier to the running container
#   -v [host]:[cont]   - Mount host directories (Volumes) for database persistence
#
# Example production command:
#   docker run -d -p 8000:8000 -e OPENAI_API_KEY="sk-123" --name my-ai-service ai-image:latest

# print("\n--- 2. DETAILED DOCKER RUN Mappings ---")
print("  Local Machine (Request on Port 8080) ──► Port Mapping (-p 8080:8000) ──► Container (FastAPI on Port 8000)")


# === SIMULATING DOCKER CLI COMMANDS =========================================
#
# Let's write a highly educational interactive script in Python that translates
# core Docker CLI commands into their exact process translations, helping us understand
# what happens under the hood when we execute them!

# print("\n--- 3. TRANSLATING DOCKER CLI ACTIONS ---")

class DockerCLISimulator:
    def __init__(self, image_repo="ai-classifier"):
        self.image_repo = image_repo
        self.running_containers = {}
        
    def build(self, dockerfile_path, tag="latest"):
        print(f"Executing: docker build -t {self.image_repo}:{tag} {dockerfile_path}")
        print("  - Reading build layers...")
        print("  - Installing packages from requirements.txt (CACHED)...")
        print(f"  - Successfully tagged image: {self.image_repo}:{tag}")
        return f"{self.image_repo}:{tag}"
        
    def run(self, image, name, ports, envs=None, detached=True):
        cmd = f"docker run {'-d ' if detached else ''}-p {ports} "
        if envs:
            for k, v in envs.items():
                cmd += f"-e {k}=\"***\" "
        cmd += f"--name {name} {image}"
        
        print(f"Executing: {cmd}")
        
        # Simulate container state
        container_id = f"cont_{name.lower()}_123"
        self.running_containers[container_id] = {
            "name": name,
            "image": image,
            "ports": ports,
            "envs": envs or {},
            "status": "running"
        }
        print(f"  - Container spawned! ID: {container_id}")
        return container_id
        
    def ps(self):
        print("Executing: docker ps")
        print("  CONTAINER ID   IMAGE                  STATUS    PORTS")
        for cid, details in self.running_containers.items():
            print(f"  {cid[:12]}   {details['image']:<20}   {details['status']:<7}   {details['ports']}")
            
    def exec_bash(self, container_id, command):
        print(f"Executing: docker exec -it {container_id} {command}")
        if container_id not in self.running_containers:
            print("  Error: No such container running.")
            return
        details = self.running_containers[container_id]
        print(f"  - [SSH inside {details['name']}] Running command: {command}")
        print(f"  - Output: bin/python config/main.py active inside {details['image']}")

# Initialize and run CLI flows
cli = DockerCLISimulator()
# 1. Compile image
image_tag = cli.build(".", "v1.0")

# 2. Run backend API in background, passing API secret
env_configs = {"OPENAI_API_KEY": "sk-secret123", "PORT": "8000"}
cid = cli.run(image_tag, "fastapi-backend", "8080:8000", envs=env_configs, detached=True)

# 3. Check status
print("\nChecking active processes:")
cli.ps()

# 4. SSH/Execute code check inside running container
print("\nDebugging files inside container:")
cli.exec_bash(cid, "ls -la config/")


# === CRITICAL INSPECTION COMMANDS ============================================
#
# When debugging containers in production, remember these three diagnostics:
#
#   docker logs [name]
#     Shows console prints. If your FastAPI app crashes due to import errors or
#     missing connection strings at startup, this is where you find the traceback.
#
#   docker exec -it [name] sh
#     Opens a terminal *inside* the container, letting you run `ls`, check files,
#     and print environment variables.
#
#   docker inspect [name]
#     Returns a massive JSON detailing all port mappings, volume paths, and environment bindings.

# print("\n--- 4. EMERGENCY DEBUGGING VERBS ---")
print("  Logs:    docker logs [name]")
print("  Shell:   docker exec -it [name] bash")
print("  Inspect: docker inspect [name]")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Port conflict crash
#   If you try to run a container mapped to port 8000 (`-p 8000:8000`) but another app
#   is already using port 8000 on your host computer, Docker will crash.
#   Map the host port to a different number instead: `-p 8080:8000`.

# MISTAKE 2: Forgetting to stop containers (RAM leaks)
#   If you run containers in detached background mode (`-d`), they keep running forever!
#   They consume RAM and CPU cycles. Always check `docker ps` and run `docker stop [name]`
#   when you are done working.

# MISTAKE 3: Leaving dead container files on disk
#   Stopping a container does NOT delete its temporary layer file. Dead containers
#   consume disk space. Run `docker system prune` periodically to safely wipe dead layers.


# === EXERCISES ================================================================
#
# Exercise 1: In our Python CLI simulator, add a `stop(container_id)` method that
#             checks if the ID exists in `self.running_containers` and deletes it.
#
# Exercise 2: Contrast foreground execution (running standard uvicorn, locks terminal)
#             vs detached background execution (`docker run -d`, releases terminal).

# === SOLUTIONS ================================================================
#
# Exercise 1:
# # (Inside DockerCLISimulator class):
# # def stop(self, container_id):
# #     if container_id in self.running_containers:
# #         del self.running_containers[container_id]
# #         print(f"Successfully stopped and removed container: {container_id}")


# === KEY TAKEAWAYS ============================================================
#
# - docker build tags a frozen image blueprint from a Dockerfile directive.
# - docker run creates a live container instance using process namespace isolation.
# - Port forwarding (-p) maps host computer ports directly to internal container ports.
# - Detached execution (-d) moves container logs to background console buffers.
# - docker exec lets you run debugging commands directly inside active sandboxes.
# - docker logs is the first line of defense to view error tracebacks in containers.
