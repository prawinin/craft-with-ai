# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 40: Cloud Deployment & Zero-Downtime Operations
  Difficulty: Intermediate-Advanced
===============================================================================

  What you will learn:
    - Cloud Hosting Environments (Railway, Render, Hugging Face Spaces)
    - Git-Driven Deployment (Git-to-Deploy) vs. Registry-Driven Deployment
    - The concept of Zero-Downtime Deployments (Rolling Updates)
    - Writing a Zero-Downtime Rolling Update Simulator in Python
    - Executing Health Checks to ensure safe traffic redirection

  Why this matters for AI:
    Building an AI application in a local container is outstanding. But the ultimate
    milestone is shipping it to the world. You must understand how cloud hosting
    platforms pull your code, build the container, verify that your FastAPI app is
    running correctly via Health Checks, and transition users to the new version
    with zero interruption. This completes your transformation into an AI Engineer!

  Estimated time: 25 minutes

===============================================================================
"""

import time
import random

# === THE CLOUD HOSTING LANDSCAPE ============================================
#
# WHAT IS A CLOUD PROVIDER AND AN INSTANCE?
#   - A Cloud Provider (like Railway, AWS, or Google Cloud) is a company that rents out access to its massive,
#     global networks of physical data centers and supercomputers.
#   - An Instance is a single virtual slice of those computers (a virtual machine) rented specifically to you
#     to run your container. It's like renting a specific apartment (instance) inside a giant skyscraper
#     owned by a landlord (cloud provider).
#     (Containers explained fully in Module 4, Lesson 1 — "Containerization & Core Docker Concepts")
#
# WHAT ARE PROD VS. DEV ENVIRONMENT VARIABLES?
#   In software engineering, you have two main environments: Development (Dev) where you write and test code
#   on your laptop, and Production (Prod) where your code is running live for real paying users.
#   We use environment variables to switch behavior: for example, you can set `DEBUG=True` on your laptop
#   so you see detailed error messages, but set `DEBUG=False` in production so hackers can't see your system secrets!
#   (Environment Variables explained fully in Module 2, Lesson 2 — "Paths, Environments & Permissions")
#
# WHAT IS SCALING?
#   Imagine a single cashier (one instance) at a grocery store. If 5 customers arrive, the cashier can handle it.
#   If a holiday crowd of 5,000 customers rushes in, the checkout line will back up and crash.
#   Scaling is the solution:
#   - Vertical Scaling means buying a faster, beefier computer for the cashier (more CPU/RAM).
#   - Horizontal Scaling means opening up 20 more registers (spinning up 20 identical copies of your container)
#     and using a load balancer to distribute the customers evenly among them!
#
# Developer-First Clouds (Railway, Render, Fly.io, Hugging Face Spaces):
#   - High abstraction.
#   - You link your GitHub repository, copy-paste your environment variables, and click Deploy.
#   - The cloud automatically detects your Dockerfile, builds the image, and hosts it.
#   - Best for startups, MVPs, and single developers.
#
# Enterprise Infrastructure Clouds (AWS ECS, Google Cloud Run, Azure Container Instances):
#   - Low abstraction, high control.
#   - You compile images locally or via CI/CD, push them to a registry, and configure
#     complex load balancers, VPCs, and scaling rules.
#   - Best for massive scale or strict corporate security guidelines.

# print("--- 1. CLOUD DEPLOYMENT MODES ---")
print("  Git-to-Deploy: Push code ──► Cloud compiles Dockerfile ──► Exposed URL")
print("  Registry-to-Deploy: CI/CD pushes Image ──► Cloud pulls Image ──► Exposed URL")


# === ZERO-DOWNTIME ROLLOUT (ROLLING UPDATES) ===============================
#
# Traditional Deployment (Downtime):
#   - Stop old container version 1.0 (API goes offline - users see 502 error!).
#   - Start new container version 2.0 (Takes 5 seconds to load database/models).
#   - Users experience 5 seconds of complete service disruption.
#
# Zero-Downtime Deployment (Rolling):
#   - Keep container version 1.0 running and active.
#   - Boot container version 2.0 in the background.
#   - Run Health Checks on version 2.0.
#   - Once version 2.0 returns HTTP 200 OK (Healthy), redirect load balancer traffic
#     to version 2.0, and safely terminate version 1.0. No user experiences downtime!

# print("\n--- 2. THE ZERO-DOWNTIME ROLLING UPGRADE TIMELINE ---")
print("  [Step 1]: Traffic ──► [ v1.0 (Running) ]    [ v2.0 (Booting in background) ]")
print("  [Step 2]: Traffic ──► [ v1.0 (Running) ] ◄── [ v2.0 Health check OK ]")
print("  [Step 3]: Traffic ────────────────────────► [ v2.0 (Active) ]  (v1.0 Shut down)")


# === ZERO-DOWNTIME DEPLOYMENT SIMULATOR ======================================
#
# Let's write a complete, interactive Rolling Update Simulator in Python.
# It acts as a cloud Load Balancer routing user requests while upgrading
# our FastAPI service from v1.0 to v2.0, proving that service is never interrupted!

# print("\n--- 3. ZERO-DOWNTIME ROUTER ENGINE ---")

class CloudLoadBalancer:
    def __init__(self, active_container):
        self.active_container = active_container
        self.pending_container = None
        
    def route_request(self, user_name):
        # Route traffic to active container
        resp = self.active_container.handle_api_call(user_name)
        print(f"  [Load Balancer] Request from {user_name} routed to {self.active_container.name}: {resp}")
        
    def execute_rolling_upgrade(self, new_container):
        print(f"\n[DEPLOYMENT STARTED]: Booting {new_container.name} in background...")
        self.pending_container = new_container
        
        # 1. Booting delay
        new_container.boot_up()
        
        # 2. Run Health Checks
        print(f"\n[HEALTH CHECK GATE]: Querying {new_container.name}/healthz...")
        is_healthy = new_container.run_health_check()
        
        if is_healthy:
            print(f"  [HEALTH CHECK PASSED] {new_container.name} is stable!")
            print(f"  [TRAFFIC REDIRECT]: Routing Load Balancer pathways to {new_container.name}...")
            
            # Switch active container pointer
            old_container = self.active_container
            self.active_container = self.pending_container
            self.pending_container = None
            
            print(f"  [TEAR DOWN]: Gracefully terminating {old_container.name}...")
            old_container.terminate()
            print("[DEPLOYMENT SUCCESSFUL] Zero-downtime rolling upgrade complete.")
        else:
            print(f"\n  [HEALTH CHECK FAILED] {new_container.name} is unstable! Triggering Rollback...")
            print(f"  [ROLLBACK]: Aborting deployment. Traffic remains locked on {self.active_container.name}.")
            self.pending_container = None
            new_container.terminate()

class APIContainerInstance:
    def __init__(self, name, version, is_stable=True):
        self.name = name
        self.version = version
        self.is_stable = is_stable
        self.status = "stopped"
        
    def boot_up(self):
        self.status = "booting"
        time.sleep(0.4) # Simulate runtime boot
        self.status = "running"
        
    def handle_api_call(self, user):
        return f"Hello {user}! Served by API {self.version}."
        
    def run_health_check(self):
        # Acts like GET /healthz endpoint
        return self.is_stable
        
    def terminate(self):
        self.status = "stopped"

# 1. Boot up initial system (Version 1.0)
api_v1 = APIContainerInstance("fastapi-v1", "1.0")
api_v1.boot_up()

load_balancer = CloudLoadBalancer(api_v1)

# Route initial user traffic
load_balancer.route_request("Alice")
load_balancer.route_request("Bob")

# 2. Upgrade to Version 2.0 (Stable upgrade)
api_v2_stable = APIContainerInstance("fastapi-v2", "2.0", is_stable=True)
load_balancer.execute_rolling_upgrade(api_v2_stable)

# Route traffic after upgrade (now handled by v2!)
load_balancer.route_request("Charlie")

# 3. Simulate a Failed Upgrade to Version 3.0 (Unstable - fails health checks!)
# print("\n--- Simulating a Failed Upgrade Attempt ---")
api_v3_buggy = APIContainerInstance("fastapi-v3-buggy", "3.0", is_stable=False)
load_balancer.execute_rolling_upgrade(api_v3_buggy)

# Route traffic after failed upgrade (system safely remained on v2!)
load_balancer.route_request("Dave")


# === RECAP: YOUR AI ENGINEERING CORE SKILLS =================================
#
# Congratulations! You have completed the entire 40-lesson curriculum!
# Let's review the complete engineering path you have mastered:
#   1. Python Core Systems (Variables, Loops, Functions, Packages)
#   2. The Developer Workspace (Linux CLI, Git, Codebase Packaging Contexts)
#   3. API Backend Services (HTTP Verbs, Pydantic Schemas, Async/Await, FastAPI)
#   4. Containerization (Dockerfiles, Caching Layers, CLI port maps, Compose)
#   5. The AI Stack (LLM Clients, Backoff Retries, Structured outputs, Vector DBs)
#   6. Autonomous Systems (Tool Calling, ReAct loops, Memory buffers)
#   7. Observability & Deployments (Pipeline Tracing, CI/CD Actions, Cloud rolling updates)

print("\n========================================")
print("  CURRICULUM COMPLETE: CONGRATULATIONS!")
print("========================================")
print("  You possess the complete foundation required to design, test, package,")
print("  and deploy resilient, enterprise-grade AI applications on the cloud.")
print("========================================\n")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Hardcoding configurations instead of using env variables in production
#   If your cloud connection strings are hardcoded, you will crash when deploying.
#   Cloud providers automatically inject database configurations and ports via
#   environment variables. Always read ports dynamically: `PORT = int(os.getenv("PORT", 8000))`.

# MISTAKE 2: Neglecting the Health Check (/healthz) route
#   If you don't expose a clean `/healthz` or `/status` endpoint returning 200 OK,
#   cloud load balancers cannot verify if your container booted correctly, leading
#   to rolling updates failing to deploy or infinite build loops.

# MISTAKE 3: No volume persistence configured in cloud containers
#   Just like local containers, cloud containers are ephemeral. If your cloud container
#   restarts, local SQLite databases are wiped. Bind persistent databases (using Supabase,
#   Pinecone, or cloud volume mounts) to ensure durable records.


# === EXERCISES ================================================================
#
# Exercise 1: In our Load Balancer simulator, add a metric `successful_requests_count`
#             that increments every time `route_request` is triggered.
#
# Exercise 2: Explain why using Git-to-Deploy is superior for small fast setups,
#             while Registry-to-Deploy is preferred for large team pipelines.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# # (Inside CloudLoadBalancer class):
# # def __init__(self, active_container):
# #     self.successful_requests_count = 0
# # (Inside route_request):
# #     self.successful_requests_count += 1


# === KEY TAKEAWAYS ============================================================
#
# - Cloud hosting platforms compile Dockerfiles automatically on GitHub code pushes.
# - Zero-downtime rolling updates keep active versions online during backend upgrades.
# - Health check routes (/healthz) verify database bindings before routing traffic.
# - Unstable upgrades trigger load balancer rollbacks, preserving system health.
# - Always bind external database volumes to ensure durable data persistence on cloud nodes.
