# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 25: Concurrency with Async/Await (Event Loops)
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - Synchronous vs. Asynchronous execution (Blocking vs. Non-blocking I/O)
    - The Event Loop: How Python manages concurrent execution without threads
    - Coroutines: Declaring async functions with `async def`
    - Co-operation: Yielding control to the loop using the `await` keyword
    - Multi-request concurrency: Running tasks in parallel with `asyncio.gather`

  Why this matters for AI:
    LLM API queries are notoriously slow. A typical call to GPT-4 or Claude can
    take anywhere from 2 to 10 seconds. In a synchronous server, if User A makes
    a request, the entire server locks up and freezes for User B until User A's
    model responds! Using `async/await` ensures your server handles hundreds
    of active AI completions concurrently without any freeze.

  Estimated time: 25 minutes

===============================================================================
"""

import asyncio
import time

# === BLOCKING VS. NON-BLOCKING I/O ==========================================
#
# WHAT IS CONCURRENCY VS. PARALLELISM?
#   Imagine a single juggler throwing three balls in the air. The juggler is dealing with multiple
#   balls at the same time, but they only have two hands, so they are switching between balls rapidly.
#   That is CONCURRENCY (managing multiple tasks by switching back and forth during pauses).
#   Now imagine three jugglers standing side-by-side, each juggling their own ball.
#   That is PARALLELISM (running multiple tasks at the exact same physical moment on separate CPUs).
#
# WHAT IS AN EVENT LOOP?
#   Think of the Event Loop like an energetic waiter in a busy restaurant. The waiter goes to Table A,
#   takes their order, and passes it to the kitchen. Instead of standing at Table A for
#   15 minutes waiting for the food to cook (blocking), the waiter immediately runs to Table B to
#   take their order. When the kitchen rings the bell saying Table A's food is ready, the waiter
#   picks it up and delivers it. A single waiter (one thread) can easily serve 50 tables!
#
# Synchronous (Blocking):
#   Code runs top-to-bottom. If a line waits for a network request, CPU execution
#   halts completely. The thread is blocked.
#
# Asynchronous (Non-blocking):
#   Instead of freezing during waits, Python registers a callback and jumps to
#   process other tasks. When the network response returns, Python resumes the task.

# print("--- 1. THE CONCURRENT EVENT LOOP CONCEPT ---")
print("Sync:  Task A (Wait 2s) ──► Task B (Wait 2s) [Total: 4s]")
print("Async: Task A (Start) ─┐")
print("       Task B (Start) ─┼─► (Wait 2s concurrently) [Total: 2s]")


# === WRITING COROUTINES (async def) =========================================
#
# WHAT IS A COROUTINE?
#   A standard Python function is like a slide at a playground: once you start sliding down, you
#   must go all the way to the bottom without stopping. A Coroutine (declared with `async def`)
#   is like a video game that you can PAUSE at any time, save your progress, walk away, and resume
#   exactly where you left off later.
#
# WHAT IS ASYNC/AWAIT?
#   `async` is a warning flag you put on a function that says: "Attention! This function is a coroutine
#   and has permission to pause and wait."
#   `await` is the actual pause button. When you type `await fetch()`, you are telling the computer:
#   "I am going to wait for this network request to finish. Event loop, you are free to go do other
#   work while I am waiting!"
#
# To build asynchronous systems, you use two fundamental keywords:
#   async def - Declares an asynchronous function (coroutine). Calling it returns
#               a coroutine object but does NOT run the code yet.
#   await     - Suspends execution until the awaited coroutine finishes, giving
#               control back to the event loop to run other tasks.

# Let's simulate a slow LLM API query (GET completion)
async def fetch_llm_completion(prompt: str, delay_seconds: float = 1.5):
    print(f"  [LLM] Query started: '{prompt}'")
    # asyncio.sleep is a non-blocking wait (acts like a network timeout).
    # Using time.sleep() would block the entire thread, preventing concurrency!
    await asyncio.sleep(delay_seconds)
    print(f"  [LLM] Query finished: '{prompt}'")
    return f"Response to '{prompt}'"


# === RUNNING COROUTINES CONCURRENTLY =========================================
#
# To execute coroutines concurrently, we group them into tasks and run them
# on the Event Loop using `asyncio.gather()`.

async def run_async_pipeline():
    print("\n--- 2. CONCURRENT COMPLETIONS PIPELINE ---")
    start_time = time.time()
    
    # We will trigger three slow LLM completions concurrently:
    task1 = fetch_llm_completion("Summarize AI history", 1.5)
    task2 = fetch_llm_completion("Translate coding keys", 1.0)
    task3 = fetch_llm_completion("Draft API endpoints", 2.0)
    
    # Run all three concurrently. Total wait is determined by the slowest task (2.0s)!
    results = await asyncio.gather(task1, task2, task3)
    
    elapsed = time.time() - start_time
    print(f"\nAll completions received! Results:")
    for res in results:
        print(f"  - {res}")
    print(f"Total time elapsed: {elapsed:.2f} seconds (Sequential would be 4.5 seconds!)")

# Run the async pipeline using the asyncio runner:
if __name__ == "__main__":
    # In Jupyter or notebooks, the event loop is already active.
    # In standard Python, we boot the loop using asyncio.run():
    try:
        asyncio.run(run_async_pipeline())
    except RuntimeError:
        # Fallback if an event loop is already running in this environment
        loop = asyncio.get_event_loop()
        loop.create_task(run_async_pipeline())


# === THE BLOCKING TRAP =======================================================
#
# If you place a blocking call (like a CPU-intensive math loop or `time.sleep()`)
# inside an async function, you block the entire event loop. No other tasks
# will progress. Let's see the distinction:

async def blocking_trap_simulation():
    print("\n--- 3. THE BLOCKING TRAP WARNING ---")
    
    # This async function calls time.sleep internally (A major bug!)
    async def bad_async_task():
        print("  [BAD] Started task")
        time.sleep(1.0) # WARNING: CPU-blocking sleep! Locks the loop!
        print("  [BAD] Finished task")

    async def normal_async_task():
        print("  [GOOD] Normal task runs...")
        
    await asyncio.gather(bad_async_task(), normal_async_task())

# (We omit running this in standard flow to keep our course runner responsive)


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Forgetting the "await" keyword when calling async functions
#   If you run `result = fetch_llm_completion("prompt")` without `await`,
#   Python does not execute the function. It simply returns a `<coroutine object>`.
#   Always prefix coroutine invocations with `await`.

# MISTAKE 2: Calling sync library operations inside async endpoints
#   Using a synchronous database driver (like standard sqlite3 or requests)
#   inside a FastAPI async router blocks the server thread, neutralizing the async advantage.
#   Use async drivers (e.g. `httpx` instead of `requests`) for non-blocking I/O.

# MISTAKE 3: Confusing async with true multi-threading CPU parallelism
#   Async/Await is outstanding for waiting operations (network, disk, databases).
#   It does NOT speed up CPU-bound mathematical operations (like training models).
#   For CPU-heavy pipelines, use `multiprocessing`.


# === EXERCISES ================================================================
#
# Exercise 1: Write an async function `download_webpage(url, delay)` that simulates
#             downloading a file. It should print a start message, await a delay,
#             and return the HTML body mock string.
#
# Exercise 2: Build a coroutine pipeline that downloads three webpages concurrently
#             using `asyncio.gather` and prints their total elapsed time.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# async def download_webpage(url, delay=1.0):
#     print(f"Downloading {url}...")
#     await asyncio.sleep(delay)
#     return f"<html>{url} content</html>"
#
# Exercise 2:
# async def run_downloader():
#     t1 = download_webpage("google.com", 0.5)
#     t2 = download_webpage("github.com", 1.2)
#     t3 = download_webpage("fastapi.tiangolo.com", 0.8)
#     pages = await asyncio.gather(t1, t2, t3)
#     print(f"Downloaded {len(pages)} pages successfully.")


# === KEY TAKEAWAYS ============================================================
#
# - Async/Await is a cooperation model; tasks voluntarily yield execution.
# - Coroutines are declared with `async def` and executed by prepending `await`.
# - A single-threaded event loop processes hundreds of active connections concurrently.
# - asyncio.sleep() yields control, whereas time.sleep() freezes the entire server.
# - asyncio.gather() enables simultaneous parallel execution of waiting operations.
