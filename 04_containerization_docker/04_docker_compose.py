# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 30: Multi-Service Orchestration with Docker Compose
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - The limitation of single-container commands in multi-service systems
    - Declarative Architecture: Defining services inside docker-compose.yml
    - Dependency Linking: Mapping boot sequence using the `depends_on` rule
    - Data Persistence: Mounting folder nodes using the `volumes` directive
    - Single-command orchestration: docker compose up / down / logs

  Why this matters for AI:
    Enterprise AI platforms are never single files. They consist of a FastAPI
    backend, a frontend client, and a dedicated Vector Database (e.g. ChromaDB or pgvector).
    Instead of typing complex network commands to link these services, Docker Compose
    lets you declare your entire stack in a single YAML file and spin it up
    with a single command: `docker compose up`.

  Estimated time: 20 minutes

===============================================================================
"""

# === THE MULTI-SERVICE CHALLENGE ============================================
#
# A typical AI product consists of:
#   1. Web UI      - React or HTML/JS frontend (Client port 3000)
#   2. API Backend - FastAPI server (Logic port 8000)
#   3. Vector DB   - ChromaDB or Qdrant search engine (Data port 8000)
#
# Linking these manually requires setting up custom virtual networks, matching
# ports, and manually starting databases before servers. Compose automates this.

# print("--- 1. MULTI-SERVICE ORCHESTRATION ---")
print("  docker compose up  ──► Boots VectorDB ──► Boots FastAPI ──► Boots Web UI")


# === ANATOMY OF A DOCKER-COMPOSE.YML FILE ===================================
#
# WHAT IS ORCHESTRATION?
#   Think of container Orchestration like a conductor leading a classical orchestra.
#   Instead of a chaotic din where 50 musicians play whenever they want, the conductor
#   signals exactly when the drums should start, when the violins should fade in, and
#   keeps everyone in perfect harmony. In cloud engineering, orchestration is the automated
#   coordination, scheduling, and management of multiple active containers.
#
# WHAT IS A SERVICE?
#   In the context of Docker Compose, a "Service" is a configuration template for a container
#   that you want to run. Think of it like a role in a play (like "The DB" or "The Web App").
#   Each service defines which image to use, what ports to map, and what environment variables
#   to inject when launching that role's container.
#
# WHAT IS A DOCKER NETWORK?
#   A Docker Network is like a private walkie-talkie channel that Docker sets up specifically
#   for your containers. Outside programs cannot listen in or disrupt them, but the containers
#   inside the network can talk to each other directly using simple nicknames (like calling Qdrant
#   using the host nickname `vectordb`) instead of complicated IP addresses!
#
# WHAT IS A COMPOSE FILE?
#   A Compose File (usually `docker-compose.yml`) is a declarative blueprint written in YAML that
#   specifies your entire application stack in one place. It is like a complete blueprint of a
#   miniature office park: it defines the buildings (services), the roads connecting them (networks),
#   and the shared storage units (volumes).
#
# Docker Compose uses YAML to declare services, networks, and persistent volumes.
#
# Key Directives:
#   services:   - Declares the containers that make up your application
#   build:      - Path to local folder containing the service's Dockerfile
#   ports:      - Port forwarding arrays (host:container)
#   environment:- Environment variable injections  (Explained in Module 2, Lesson 2 — "Paths, Environments & Permissions")
#   depends_on: - Declares dependencies; starts DBs before API servers
#   volumes:    - Mounts persistent folders from the host computer to the container  (Explained in Module 4, Lesson 3 — "Managing Containers with Docker CLI")

# print("\n--- 2. THE DECLARATIVE COMPOSE ARCHITECTURE ---")

# Let's inspect a production-ready docker-compose.yml layout:
sample_compose_yml = """
version: '3.8'

services:
  vectordb:
    image: chromadb/chroma:0.4.15
    ports:
      - "8000:8000"
    volumes:
      - chroma-data:/chroma/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 10s
      timeout: 5s
      retries: 3

  api:
    build: ./api
    ports:
      - "8080:8000"
    environment:
      - CHROMA_SERVER_HOST=vectordb
      - CHROMA_SERVER_HTTP_PORT=8000
    depends_on:
      vectordb:
        condition: service_healthy

volumes:
  chroma-data:
"""

print(sample_compose_yml)


# === HEALTHCHECKS =============================================================
#
# WHY DEPENDS_ON ISN'T ENOUGH:
#   If you just write `depends_on: - vectordb`, Docker will start the API container
#   the exact millisecond the DB container starts. But databases take time to boot up!
#   Your API will try to connect, fail, and crash.
#
#   A `healthcheck` tells Docker how to test if the DB is actually ready to receive
#   traffic (e.g., by making a curl request). Then, the API's `depends_on` can say
#   `condition: service_healthy`, which forces the API to wait patiently until the DB
#   reports that it has fully booted and is ready for connections.



# === SIMULATING DOCKER COMPOSE ORCHESTRATION =================================
#
# Let's write an interactive parser in Python that reads this YAML architecture,
# traces the services, and prints out a dependency diagram to explain exactly
# how Compose organizes network namespaces and boot sequences!

# print("--- 3. DEPENDENCY LINKAGE INTERPRETER ---")

def interpret_compose_architecture(compose_text):
    lines = compose_text.strip().split("\n")
    current_service = None
    dependencies = {}
    ports_map = {}
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue
            
        # Detect service level
        if line.startswith("  ") and not line.startswith("    ") and line_stripped.endswith(":"):
            current_service = line_stripped[:-1]
            dependencies[current_service] = []
            ports_map[current_service] = []
            
        # Detect depends_on links
        if current_service and line_stripped == "depends_on:":
            continue
        if current_service and line.startswith("      - ") and not line.startswith("        "):
            val = line_stripped[2:]
            # If it's under depends_on, add dependency
            dependencies[current_service].append(val)
            
        # Detect port mappings
        if current_service and line.startswith("      - \""):
            val = line_stripped.replace('"', '').replace('-', '').strip()
            ports_map[current_service].append(val)
            
    # Print Dependency Tracing Diagram
    print("\nTracing Service Dependencies:")
    for service, deps in dependencies.items():
        ports = ports_map.get(service, [])
        port_str = f" Ports: {ports}" if ports else ""
        if deps:
            print(f"  Container [{service}]{port_str} relies on base: {', '.join(deps)}")
            print(f"    ↳ Boot Action: Boot [{', '.join(deps)}] first, wait for healthcheck, then boot [{service}]")
        else:
            print(f"  Container [{service}]{port_str} (Base Service - boots instantly)")

interpret_compose_architecture(sample_compose_yml)


# === DOCKER COMPOSE COMMAND CHEAT SHEET ======================================
#
# To manage your multi-container stack, run these commands inside your project folder:
#
#   docker compose up -d
#     Launches all services in the background, creates networks, and maps ports.
#
#   docker compose logs -f
#     Combines console streams from all running services into a single color-coded
#     output view in real-time.
#
#   docker compose down
#     Safely stops containers, releases network interfaces, and unbinds mapped ports
#     without losing your persistent volumes.
#
#   docker compose watch
#     💡 PRO TIP: The modern way to develop! Instead of rebuilding your container
#     when you change a Python file, `watch` auto-syncs your file saves directly 
#     into the running container instantly.

# print("\n--- 4. DOCKER COMPOSE CLI VERBS ---")
print("  Launch:   docker compose up -d")
print("  Tear Down: docker compose down")
print("  Logs:     docker compose logs -f")
print("  Live Sync: docker compose watch  (💡 PRO TIP)")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Using "localhost" to call databases inside docker networks
#   When your FastAPI app runs inside a docker container, `localhost` refers to
#   that container. If it tries to reach ChromaDB using `localhost:8000`, it will fail!
#   In Compose, containers share a virtual network. You can call other containers
#   directly using their **Service Name** (e.g. `http://vectordb:8000`).

# MISTAKE 2: Forgetting to mount volumes for persistence
#   If you launch pgvector or ChromaDB without the `volumes` directive, database entries
#   will be wiped clean every time you run `docker compose down`.
#   Always map a local directory or named volume to persist database records.

# MISTAKE 3: Invalid YAML indentation spacing
#   YAML relies on exact, consistent spacing (never mix tabs and spaces!).
#   If your compose file has indentation errors, the parser will crash.
#   Always verify your files using a YAML validator or an IDE extension.


# === EXERCISES ================================================================
#
# Exercise 1: Write an additional service declaration block for a Redis caching service
#             running image `redis:7-alpine` exposed on host port `6379:6379`.
#
# Exercise 2: Explain why using the `depends_on` directive is essential for preventing
#             API crashes at system startup.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# # Add under services:
# #   cache:
# #     image: redis:7-alpine
# #     ports:
# #       - "6379:6379"


# === KEY TAKEAWAYS ============================================================
#
# - Docker Compose orchestrates multi-service applications using YAML blueprints.
# - Virtual bridge networks are automatically created, linking containers safely.
# - Services call each other directly by using their service names as hosts.
# - Depends_on governs start sequence; volumes guarantee database persistent health.
# - Docker compose up and down handles entire stack operations with single command verbs.
