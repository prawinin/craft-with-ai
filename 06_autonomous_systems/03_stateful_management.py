# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 37: Stateful Agent Management & Memory
  Difficulty: Intermediate-Advanced
===============================================================================

  What you will learn:
    - Stateless vs. Stateful Architecture (Why memory is the holy grail of agents)
    - Memory Classification: Short-Term, Long-Term, and Working Memory
    - Storing conversation history dynamically in list buffers
    - Implementing a "Stateful Agent Scratchpad" to track sub-task completion
    - Simulating dynamic state mutations across multi-step execution paths

  Why this matters for AI:
    LLM APIs are fundamentally stateless—they forget everything the millisecond
    they finish responding to a prompt. To build an agent that can hold a conversation
    or work on a multi-day coding task, your Python backend must act as the "brain's state."
    It must persist conversation history, track what sub-tasks are finished,
    and save variables across successive API cycles.

  Estimated time: 20 minutes

===============================================================================
"""

import json

# === STATELESS VS. STATEFUL ARCHITECTURE ====================================
#
# WHAT ARE STATE AND SESSION?
#   - Think of State like a board game in progress. The "state" is the exact position of all the pieces,
#     who has how many points, and whose turn it is. If you take a photo of the board, you have frozen the state.
#   - A Session is the timeline of one complete play-through from setup to packing up the box. In web apps,
#     a session is the period of time a specific user spends interacting with your app. Maintaining
#     session state means remembering what the user did in step 1 when they are on step 5!
#
# WHAT IS SHORT-TERM VS. LONG-TERM MEMORY?
#   - Short-Term (or Working) Memory is like a scratchpad on your desk. When holding a conversation, you keep the
#     last few exchanged messages right in front of you so you can follow the dialogue. In AI, this is passed
#     directly inside the active prompt context window.
#     (Context Window explained in Module 2, Lesson 4 — "Context-Driven AI")
#   - Long-Term Memory is like a massive filing cabinet in the basement. It stores permanent facts (like user
#     profiles, past purchase history, or vector database indexes) that you don't need to read every second,
#     but want to fetch on-demand when a specific topic is brought up.
#     (Vector Databases explained in Module 5, Lesson 4 — "Vector Databases")
#
# Stateless (Standard APIs):
#   - Every request is independent.
#   - The server has no memory of past requests (like standard HTTP).
#
# Stateful (Agents & Chatbots):
#   - The system maintains a persistent record of past interactions and variables.
#   - It references old decisions, remembers user names, and tracks project progress.

# print("--- 1. STATEFUL MEMORY STRUCTURES ---")
print("  Short-Term: Conversation History (e.g. Chat history lists passed to LLM)")
print("  Working:    Agent Scratchpad (e.g. Current plan progress: [Task 1 Done, Task 2 Todo])")
print("  Long-Term:  Database Storage (e.g. User settings, vector indexes)")


# === IMPLEMENTING AN AGENT WORKING MEMORY SCRATCHPAD =========================
#
# Let's build a highly educational, interactive Stateful Agent Scratchpad class.
# It tracks short-term chat logs, maintains a list of sub-tasks, and updates
# variables dynamically as the agent progresses through a multi-step operation!

# print("\n--- 2. PROGRAMMATIC AGENT SCRATCHPAD ---")

class StatefulAgentScratchpad:
    def __init__(self, task_description):
        self.task_description = task_description
        # Working Memory: Checklist tracking sub-tasks
        self.sub_tasks = {}
        # Working Memory: Variables dictionary to store results
        self.variables = {}
        # Short-Term Memory: Chat history buffer
        self.chat_history = []
        
    def add_sub_task(self, name, description):
        self.sub_tasks[name] = {"description": description, "status": "todo"}
        
    def update_task_status(self, name, status):
        if name in self.sub_tasks:
            self.sub_tasks[name]["status"] = status
            print(f"  [State Shift]: Sub-task '{name}' updated to: {status.upper()}")
        else:
            print(f"  [Warning]: Tried to update unknown sub-task '{name}'!")
            
    def store_variable(self, key, value):
        self.variables[key] = value
        print(f"  [Memory Store]: Saved '{key}' = {value}")
        
    def append_chat(self, role, message):
        self.chat_history.append({"role": role, "content": message})
        
    def print_scratchpad_state(self):
        print("\n========================================")
        print("  AGENT CURRENT WORKING SCRATCHPAD STATE")
        print("========================================")
        print(f"  Core Goal: {self.task_description}")
        print("\n  Sub-tasks Checklist:")
        for name, details in self.sub_tasks.items():
            status_icon = " [x] " if details["status"] == "done" else " [ ] "
            print(f"   {status_icon} {name:<12}: {details['description']}")
            
        print("\n  Stored Memory Variables:")
        for k, v in self.variables.items():
            print(f"    - {k}: {v}")
        print("========================================\n")

    def save_state_to_disk(self, filename="agent_state.json"):
        """Serializes the entire scratchpad to disk for persistence."""
        state = {
            "task_description": self.task_description,
            "sub_tasks": self.sub_tasks,
            "variables": self.variables,
            "chat_history": self.chat_history
        }
        with open(filename, "w") as f:
            json.dump(state, f, indent=4)
        print(f"  [Persistence]: Saved agent state to {filename}")

    def load_state_from_disk(self, filename="agent_state.json"):
        """Deserializes the scratchpad from disk, restoring memory."""
        try:
            with open(filename, "r") as f:
                state = json.load(f)
                self.task_description = state.get("task_description", "")
                self.sub_tasks = state.get("sub_tasks", {})
                self.variables = state.get("variables", {})
                self.chat_history = state.get("chat_history", [])
            print(f"  [Persistence]: Restored agent state from {filename}")
        except FileNotFoundError:
            print(f"  [Persistence]: No saved state found at {filename}")


# 1. Initialize our stateful scratchpad for a deployment task
agent_brain = StatefulAgentScratchpad("Deploy FastAPI backend server to cloud")

# 2. Add structural sub-tasks to working checklist
agent_brain.add_sub_task("dockerize", "Write Dockerfile and test local build")
agent_brain.add_sub_task("test_api", "Run pytest checks on server routes")
agent_brain.add_sub_task("cloud_deploy", "Trigger cloud build hook and verify port")

# Print initial state
agent_brain.print_scratchpad_state()

# 3. Simulate step-by-step state transitions
# print("--- 3. SIMULATING MULTI-STEP STATE MUTATIONS ---")
agent_brain.append_chat("user", "Start deployment pipeline")

# Step 1: Dockerize
agent_brain.update_task_status("dockerize", "done")
agent_brain.store_variable("docker_image_tag", "backend:v1.0.2")

# Step 2: Test API
agent_brain.update_task_status("test_api", "done")
agent_brain.store_variable("test_status", "passed (12/12 routes OK)")

# Print intermediate state
agent_brain.print_scratchpad_state()

# Step 3: Deploy
agent_brain.update_task_status("cloud_deploy", "done")
agent_brain.store_variable("deployment_url", "https://api-backend.railway.app")

# Print final state
agent_brain.print_scratchpad_state()

# 4. Simulate a server crash by saving and reloading state
# print("--- 4. STATE PERSISTENCE DEMO ---")
agent_brain.save_state_to_disk("mock_deployment_state.json")

# Imagine the Python script crashed here...
# Now we start a fresh script and restore the brain:
rebooted_brain = StatefulAgentScratchpad("Empty Task")
rebooted_brain.load_state_from_disk("mock_deployment_state.json")


# === THE DANGER OF STATE DRIFT ===============================================
#
# If multiple agents write to the same state simultaneously, you get **Race Conditions**
# or **State Drift** (e.g. Agent A overwrites variables calculated by Agent B).
#
# Resolving State Drift:
#   1. Lock mechanism: Ensure only one agent can modify a specific state key at a time.
#   2. Structured Graph Routers: Use state-graph frameworks (like LangGraph) where state transitions
#      are explicitly defined as nodes and edges, preventing erratic mutations.

# print("--- 4. THE STATE MUTATION GATE ---")
print("  Agent Command ──► [ Graph Validation Gate ] ──► Safe State Mutation")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Relying on the LLM to remember state internally
#   If you don't save variables (like `user_id` or `price`) in Python, and just hope
#   the LLM will remember it in the chat history, it will eventually lose it as the
#   conversation grows. Always store key variables in an explicit backend state.

# MISTAKE 2: Unbounded chat history (Context Window limits)
#   Appending every user chat to an infinite list will eventually exceed the model's
#   token limits. Implement a sliding window buffer (e.g. keep only the last 10 messages)
#   or summarize older chats to conserve tokens.

# MISTAKE 3: No state persistence on server crashes
#   If you store agent state strictly in local memory variables (like our dictionary),
#   and your server restarts or crashes, your active agents lose their memory completely!
#   In production, persist the state JSON into a Redis or Postgres database.


# === EXERCISES ================================================================
#
# Exercise 1: In our `StatefulAgentScratchpad` class, write a method `get_chat_prompt_context()`
#             that formats the `chat_history` list into a single clean string suitable
#             for injecting into an LLM prompt.
#
# Exercise 2: Explain why short-term memory (conversation buffer) is passed in the prompt
#             on every request, while long-term memory (databases) is retrieved on-demand.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# # (Inside StatefulAgentScratchpad class):
# # def get_chat_prompt_context(self):
# #     return "\n".join(f"{c['role'].upper()}: {c['content']}" for c in self.chat_history)


# === KEY TAKEAWAYS ============================================================
#
# - LLM APIs are stateless; developers must manage persistent states in Python.
# - Memory is divided into short-term (chat), working (checklist), and long-term (DB).
# - Working scratchpads allow agents to track goals and sub-tasks systematically.
# - Explicit state management prevents models from losing variable reference bindings.
# - In production, save state variables to external databases to prevent data loss.
