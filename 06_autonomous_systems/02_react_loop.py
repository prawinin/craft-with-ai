# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 36: The ReAct Loop (Autonomous Agent Foundations)
  Difficulty: Intermediate-Advanced
===============================================================================

  What you will learn:
    - Moving beyond single-shot prompting to multi-step autonomous behavior
    - The ReAct Paradigm: Thought ──► Action ──► Observation loops
    - Managing Agent State and appending historical memory buffers
    - Preventing Runway Loops: Enforcing strict maximum iteration bounds
    - Building a complete ReAct loop engine from scratch in pure Python

  Why this matters for AI:
    Complex user requests (like: "Find the customer's purchase history, check
    if their order was shipped, and if not, process a 10% coupon refund") cannot
    be solved in one prompt. An agent must think, query a tool, look at the results
    (observation), think again, query a second tool, and synthesize the outcome.
    By learning to build a ReAct loop, you unlock true agentic capabilities
    without relying on complex, bloated frameworks.

  Estimated time: 25 minutes

===============================================================================
"""

import json
import time

# === THE ReAct PARADIGM =====================================================
#
# WHAT IS THE REACT PARADIGM?
#   ReAct stands for "Reasoning + Acting". Think of it like a detective solving a mystery.
#   Instead of guessing the suspect immediately (single-shot prompt), the detective writes in their
#   notebook: "I need to find out where the victim was (Thought). I will check the security cameras (Action)."
#   They view the footage showing the victim at a grocery store (Observation).
#   Then they write: "Ah! Now I need to search the grocery receipts (Thought)."
#   By alternating between logical reasoning (Thoughts) and gathering evidence (Actions/Observations),
#   the AI can solve highly complex, multi-step problems!
#
# ReAct combines "reasoning" (thoughts) with "acting" (tool execution).
# (Tool Calling explained in Module 6, Lesson 1 — "LLM Tool Calling & Function Binding")
#
# The loop operates in four distinct phases:
#   1. Thought     - The model reasons: "The user wants X. First, I need to fetch Y.
#                    I will use tool Z to get it."
#   2. Action      - The model outputs a structured tool execution call.
#   3. Observation - The Python environment runs the tool and returns the text result.
#   4. Repeat/End  - The model reads the observation. If it has the final answer,
#                    it prints it to the user. Otherwise, it generates a new Thought!

# print("--- 1. THE ReAct CYCLE ---")
print("  User Query ──► [ Thought ──► Action ──► Observation ] ──► Final Answer")


# === BUILDING A ReAct ENGINE FROM SCRATCH ====================================
#
# WHAT IS A REASONING TRACE AND AN OBSERVATION?
#   - A Reasoning Trace (or Thought) is the AI "muttering under its breath" to explain to itself what it is
#     doing and why before it executes a command. This has been proven to make LLMs significantly smarter!
#   - An Observation is the concrete result or output that the Python environment returns after running
#     the AI's requested tool (e.g. database query outputs, file content strings, or API response status).
#
# WHAT IS AN AGENT LOOP?
#   An Agent Loop is the circular conveyor belt of an autonomous AI. Unlike a standard script that runs
#   from start to finish and stops, an Agent Loop runs in a continuous circle: it evaluates the current
#   state, decides on an action, runs the tool, looks at the results, and decides whether it needs to run
#   another circle or if the goal is fully achieved. It keeps looping autonomously until it succeeds or hits
#   a safety cutoff limit!
#
# Let's write a complete, lightweight ReAct loop engine in Python.
# We will simulate a customer support agent solving a multi-step user problem:
#   "Calculate the refund for customer Bob (ID 101) after checking his credit balance."
#
# Available Tools:
#   - `get_user_db_id(name)`  -> Returns user_id
#   - `get_user_balance(uid)` -> Returns balance

# print("\n--- 2. THE ReAct AGENT RUNTIME ENGINE ---")

# Mock Tools
def get_user_db_id(name: str):
    database = {"bob": 101, "alice": 202}
    return f"Database ID for {name} is {database.get(name.lower(), 'None')}"

def get_user_balance(user_id: int):
    balances = {101: 150.00, 202: 890.00}
    return f"Balance for User ID {user_id} is ${balances.get(user_id, 0.00)}"

# Simulated LLM "Brain"
# In a real app, this method would query a live LLM (like GPT-4)
def simulate_agent_brain(iteration, history):
    # Depending on the history, the model decides what to do next:
    if iteration == 1:
        return {
            "thought": "The user wants the balance refund status for Bob. First, I need to find Bob's unique database user ID. I will call the 'get_user_db_id' tool.",
            "action": {"name": "get_user_db_id", "args": {"name": "Bob"}},
            "final_answer": None
        }
    elif iteration == 2:
        return {
            "thought": "I have successfully retrieved Bob's database ID, which is 101. Now, I need to check his balance using 'get_user_balance'.",
            "action": {"name": "get_user_balance", "args": {"user_id": 101}},
            "final_answer": None
        }
    elif iteration == 3:
        return {
            "thought": "I have checked the balance. Bob has a balance of $150.00. I have gathered all necessary information to solve the user prompt.",
            "action": None,
            "final_answer": "Bob (User ID 101) has a current credit balance of $150.00. Your refund has been approved for the full amount."
        }

# The ReAct Execution Loop
def execute_react_loop(user_query, max_iterations=4):
    print(f"User Query: '{user_query}'")
    
    # Initialize history memory buffer
    history = [f"User Query: {user_query}"]
    
    # Define tool maps
    tools = {
        "get_user_db_id": get_user_db_id,
        "get_user_balance": get_user_balance
    }
    
    for iteration in range(1, max_retries_cutoff := max_iterations + 1):
        print(f"\n--- [Iteration #{iteration}] ---")
        
        # 1. Ask the LLM "Brain" what to do next
        llm_response = simulate_agent_brain(iteration, history)
        
        # Print Thought
        print(f"  Thought: {llm_response['thought']}")
        history.append(f"Thought: {llm_response['thought']}")
        
        # 2. Check if we have the final answer
        if llm_response["final_answer"]:
            print(f"\n[FINAL ANSWER] {llm_response['final_answer']}")
            return llm_response["final_answer"]
            
        # 3. Otherwise, execute the requested action
        action = llm_response["action"]
        tool_name = action["name"]
        tool_args = action["args"]
        
        if tool_name not in tools:
            raise ValueError(f"Agent requested non-existent tool: {tool_name}")
            
        # Execute tool (mimics tool calling execution layer)
        tool_func = tools[tool_name]
        print(f"  Action: Call '{tool_name}' with args {tool_args}")
        
        # Call function unpacking args
        observation = tool_func(**tool_args)
        
        # Print Observation
        print(f"  Observation: {observation}")
        history.append(f"Action: {tool_name}({tool_args}) -> Observation: {observation}")
        
        # Small loop pace pause
        time.sleep(0.5)
        
    print(f"\n[ALERT] Agent terminated because it exceeded maximum iteration cutoff ({max_iterations}).")
    return None

# Run our agent loop!
execute_react_loop("Find Bob's credit balance and approve refund.", max_iterations=3)


# === RUNWAY CYCLES & INFINITE LOOP SAFESTOPS ================================
#
# If an LLM misinterprets a tool result (e.g. tool returns "User not found",
# and the agent generates a thought: "Let me try searching 'User' again" in an
# infinite loop), it will burn thousands of tokens in seconds.
#
# Rule of Agent Loops:
#   Always declare a strict `max_iterations` (typically 3-5 is optimal) and a
#   `time_limit` check. If the agent does not solve the task in that time, halt,
#   output the history log, and ask the user for clarification.

# print("\n--- 3. RUNWAY PROTECTION GATE ---")
print("  Loop Iteration Counter (1 -> 2 -> 3 -> 4) ──► [ Limit Check (Max 4) ] ──► Safestop Kill")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Infinite loops due to unhandled exceptions
#   If your tool function crashes and returns an empty string or raises an error,
#   and you don't feed the error back as an observation, the agent might keep trying
#   to call the exact same tool endlessly. Feed errors back to the agent as observations!

# MISTAKE 2: Storing massive history context
#   Every loop iteration appends thoughts and observations to the LLM prompt.
#   By iteration 10, your context window will be bloated with redundant logs.
#   Summarize history buffers or enforce a strict iteration cutoff to conserve tokens.

# MISTAKE 3: Using agents when simple scripts suffice
#   Do not use an autonomous agent to perform simple, predictable, linear operations
#   (like standard forms processing). Linear code is 100% reliable and costs zero tokens.
#   Only use agents for complex, open-ended tasks requiring dynamic decision branches.


# === EXERCISES ================================================================
#
# Exercise 1: Extend our `execute_react_loop` simulation with an active stopwatch
#             that records and prints the total elapsed time of the agent cycle.
#
# Exercise 2: Contrast linear programming (standard scripts) vs dynamic agentic loops
#             (ReAct) in terms of cost, latency, and reliability.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# # Add start_time = time.time() at start, elapsed = time.time() - start_time at return.


# === KEY TAKEAWAYS ============================================================
#
# - ReAct agents combine reasoning (thoughts) with execution actions (tools).
# - The loop iterates through Thought -> Action -> Observation cycles progressively.
# - Observations feed tool execution results back to the agent as new evidence.
# - Setting a strict maximum iteration cutoff prevents runaway loop token drainage.
# - Only deploy agentic loops for open-ended, complex decision-making tasks.
