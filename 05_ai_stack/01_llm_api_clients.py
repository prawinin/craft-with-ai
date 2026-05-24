# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 31: Robust LLM API Clients & Reliability
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - Connecting securely to model APIs (OpenAI, Anthropic, Gemini)
    - Handling rate limits (HTTP 429) and network dropouts gracefully
    - Exponential Backoff & Retries: The standard pattern for API reliability
    - Real-time token streaming: Reducing perceived latency using generators
    - Implementing a custom exponential retry wrapper in standard Python

  Why this matters for AI:
    In a local notebook, when an API call fails due to a rate limit or a network hiccup,
    you just run the cell again. In a production app with paying users, an unhandled
    API error crashes the session and results in a terrible user experience.
    To build enterprise-grade apps, your backend must be highly resilient
    against remote server failures.

  Estimated time: 20 minutes

===============================================================================
"""

import time
import random
import sys

# === THE PRODUCTION API REALITY ==============================================
#
# WHAT IS AN LLM?
#   LLM stands for Large Language Model (like GPT-4, Claude, or Gemini). Think of an LLM like an incredibly
#   well-read digital librarian. It has analyzed billions of pages of internet text, books, and code.
#   It doesn't "think" in a human sense; instead, it uses advanced statistics to predict the most likely next
#   words in a sentence, behaving like a supercharged autocomplete that can write software!
#
# WHAT IS A RATE LIMIT?
#   Imagine a popular ice cream stand that can only serve 5 customers per minute. If a crowd of 100 people
#   rushes the stand all at once, the vendor yells "Stop! Wait in line!" and turns people away.
#   A Rate Limit is that exact limit set by API providers: it restricts how many requests (or words/tokens)
#   you are allowed to send to their servers per minute to prevent their system from crashing under heavy load.
#   (Tokens are word-chunks explained in Module 2, Lesson 4 — "Context-Driven AI")
#
# Production AI pipelines depend on remote cloud servers. These servers:
#   1. Enforce strict Rate Limits (number of requests or tokens per minute).
#   2. Periodically return HTTP 503 (Server Overloaded) during peak hours.
#   3. Occasionally drop connections due to internet latency spikes.
#
# To handle this, we use the Exponential Backoff pattern:
#   On failure, wait a short time (e.g. 1s). If it fails again, double the wait (2s, 4s, 8s)
#   and add a small random variation ("jitter") to prevent all crashed clients from retrying
#   at the exact same microsecond (the "thundering herd" problem).

# print("--- 1. API RELIABILITY PIPELINE ---")
print("  Request ──► [ Rate Limit (429) ] ──► Backoff (1s) ──► Backoff (2s) ──► Success!")


# === EXPONENTIAL BACKOFF RETRY IMPLEMENTATION ================================
#
# WHAT IS EXPONENTIAL BACKOFF AND JITTER?
#   - Exponential Backoff is like trying to call a busy phone line. If they don't answer, you wait 1 second
#     before calling again. If they still don't answer, you wait 2 seconds, then 4 seconds, then 8 seconds.
#     By doubling your wait time after each failure, you give the overloaded server breathing room to recover.
#   - Jitter is adding a tiny bit of random variation to that wait time (e.g. waiting 4.2 seconds instead of
#     exactly 4.0 seconds). This ensures that if 1,000 servers all crashed at once, they don't all retry at the
#     exact same microsecond, which would instantly crash the API again!
#
# Let's write a robust, production-ready retry decorator in standard Python.
# It captures simulated rate-limit errors and retries with backoff and jitter!

# print("\n--- 2. PROGRAMMATIC RETRY WITH EXPONENTIAL BACKOFF ---")

def retry_with_backoff(max_retries=3, initial_delay=1.0, backoff_factor=2.0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(1, max_retries + 1):
                try:
                    # Attempt to run the target function
                    return func(*args, **kwargs)
                except Exception as e:
                    # In a real app, you would check: if e.status_code == 429
                    print(f"  [Attempt #{attempt} FAILED]: Captured error: {e}")
                    
                    if attempt == max_retries:
                        print("  [ERROR] Max retries reached. Raising exception.")
                        raise e
                    
                    # Calculate exponential delay with random jitter (+/- 10%)
                    jitter = random.uniform(-0.1, 0.1) * delay
                    sleep_time = max(0.1, delay + jitter)
                    
                    print(f"    ↳ Retrying in {sleep_time:.2f}s (Backoff delay: {delay}s)...")
                    time.sleep(sleep_time)
                    
                    # Double the delay for the next attempt
                    delay *= backoff_factor
        return wrapper
    return decorator

# Let's create a simulated API caller that fails twice before succeeding:
fail_counter = 0

@retry_with_backoff(max_retries=4, initial_delay=0.5)
def call_llm_api(prompt):
    global fail_counter
    fail_counter += 1
    
    if fail_counter < 3:
        # Simulate rate-limiting (HTTP 429)
        raise ConnectionError("HTTP 429: Too Many Requests (Rate Limit Exceeded)")
        
    return f"Success! LLM Completion for: '{prompt}'"

print("Triggering API request with backoff decorator:")
result = call_llm_api("Analyze database index layouts")
print(f"\nFinal Result: {result}")


# === REAL-TIME TOKEN STREAMING (GENERATORS) =================================
#
# WHAT IS A GENERATOR AND YIELD?
#   A standard function is like ordering a full 10-course meal: you sit and wait for the kitchen to cook
#   everything, and then they bring all the food to your table at once (high latency). A Generator (using the
#   `yield` keyword) is like a sushi conveyor belt: the chef makes one piece of sushi and immediately slides
#   it to you, then makes the next one. This lets you start eating (reading text) instantly while the rest of
#   the meal is still being prepared!
#
# Waiting 5 seconds for a model to finish writing a long response makes the app feel slow.
# Streaming lets the backend yield tokens as they are generated, making the interface
# feel instant.
#
# In Python, this is implemented using **Generators** and the `yield` keyword.

# print("\n--- 3. MOCKING TOKEN STREAMING GENERATOR ---")

# A generator yields items one at a time, pausing execution between yields
def stream_model_response(prompt):
    tokens = ["The", " key", " to", " robust", " AI", " is", " system", " resiliency."]
    
    print(f"Streaming response for prompt: '{prompt}'")
    for token in tokens:
        time.sleep(0.15) # Simulate token generation delay
        yield token

# Consume the stream
for token in stream_model_response("What is the key to AI?"):
    # Print immediately without adding a newline (acts like streaming console)
    sys.stdout.write(token)
    sys.stdout.flush()
print() # Final newline


# === KEY CLIENT SDK PATTERNS ================================================
#
# Modern SDKs (OpenAI, Anthropic, Gemini) include built-in retry mechanics:
#
#   client = OpenAI(
#       api_key=os.environ.get("OPENAI_API_KEY"),
#       max_retries=3,  # Built-in backoff!
#       timeout=20.0    # Built-in connection timeouts
#   )
#
# Streaming in SDKs:
#   response = client.chat.completions.create(
#       model="gpt-4",
#       messages=[{"role": "user", "content": "Write code"}],
#       stream=True  # Yields chunks as they compile!
#   )

# print("\n--- 4. SDK BEST PRACTICES SUMMARY ---")
print("  Always: 1. Set explicit timeout limits | 2. Declare max retry counts | 3. Secure keys via environment")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Hardcoding API keys in code files
#   If you type `api_key = "sk-..."` in your source code, you will eventually commit
#   it to Github. Your account will be locked, and your budget will be drained.
#   Always load keys using `os.getenv("OPENAI_API_KEY")`.

# MISTAKE 2: Indefinite wait loops (Hanging threads)
#   If you don't configure request timeout limits, your backend thread can hang
#   forever waiting for an unresponsive model server, locking up your CPU resources.
#   Always set a `timeout` (e.g. 15-30 seconds).

# MISTAKE 3: Omit jitter in custom backoff scripts
#   If multiple servers fail at once and retry at exact integer intervals (e.g. exactly 2.0s),
#   they hit the API at the exact same millisecond, triggering rate limits again.
#   Always add a small random offset (jitter) to distribute request volumes.


# === EXERCISES ================================================================
#
# Exercise 1: Write an async generator coroutine `async_stream_response(prompt)`
#             that yields three tokens, awaiting `asyncio.sleep(0.1)` between each.
#
# Exercise 2: Modify `retry_with_backoff` to print a custom log if the failure caught
#             is specifically a `ConnectionError`.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# async def async_stream_response(prompt):
#     tokens = ["Async", " Stream", " Done"]
#     for t in tokens:
#         await asyncio.sleep(0.1)
#         yield t


# === KEY TAKEAWAYS ============================================================
#
# - Production API clients must be resilient against rate limits and network drops.
# - Exponential backoff delays retries incrementally to avoid hammering servers.
# - Adding random jitter prevents multiple client retries from colliding in spikes.
# - Streaming generators yield tokens progressively, reducing user-perceived latency.
# - Never hardcode API keys; load them dynamically from secure environment variables.
