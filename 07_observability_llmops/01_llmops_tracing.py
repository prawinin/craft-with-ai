# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 38: Observability & Pipeline Tracing (LLMOps)
  Difficulty: Intermediate-Advanced
===============================================================================

  What you will learn:
    - Why standard system monitoring fails to debug AI applications
    - The concept of Telemetry and Tracing inside agent pipelines
    - Recording latency, token usages, and API pricing programmatically
    - Capturing prompt inputs and model responses for audit trails
    - Building a structured JSON pipeline tracer from scratch in Python

  Why this matters for AI:
    When a customer reports: "The chatbot gave me a weird, incorrect answer,"
    checking standard server logs (which show HTTP 200 OK) is completely useless.
    You need to inspect the *exact* prompt sent to the LLM, the *exact* variables
    injected, the model response time, the tokens consumed, and the cost.
    Mastering tracing (LLMOps) is the absolute key to debugging and improving
    AI systems in production.

  Estimated time: 20 minutes

===============================================================================
"""

import time
import json
import uuid

# === THE SYSTEM TELEMETRY GAPS ===============================================
#
# WHAT IS LLMOPS?
#   LLMOps stands for Large Language Model Operations. Just like DevOps is the practice of keeping
#   traditional software running smoothly on servers, LLMOps is the set of practices and tools used
#   specifically to deploy, monitor, evaluate, and maintain AI models in production so they remain
#   reliable, secure, and cost-effective over time.
#
# WHAT IS TELEMETRY?
#   Telemetry is the automatic collection of system measurements (like speeds, performance, error rates,
#   and costs) and sending them off to a remote logging dashboard so developers can inspect and debug
#   their systems in real-time.
#
# Standard Monitoring (Datadog, Prometheus):
#   - Tracks: CPU usage, RAM footprint, network bandwidth, and HTTP status codes.
#   - Report: "Everything is healthy (Status 200, CPU 5%)."
#
# LLMOps Observability (Langfuse, Arize Phoenix):
#   - Tracks: System prompts, user inputs, tool observations, token counts, pricing,
#             response latency, and model hallucinations.  (Hallucinations explained in Module 5, Lesson 2 — "Structured Outputs & JSON Self-Correction")
#   - Report: "Warning: User query 'Check balance' cost $0.05, took 4.2s, and returned
#              hallucinated answers because database query returned empty."

# print("--- 1. THE PRODUCTION MONITORING GAP ---")
print("  Standard: Request (GET /api) ──► Server Response (200 OK) [System says: Healthy!]")
print("  LLMOps:   User Input ──► Prompt Template ──► LLM Call (Token Cost / Latency) ──► [Audit Trace]")


# === BUILDING A PIPELINE TRACE LOGGER FROM SCRATCH ===========================
#
# WHAT IS A TRACE AND A SPAN?
#   - A Trace is a complete map of a single request's journey through your entire application. Think of it
#     like a package tracking log showing every facility your parcel visited on its way to your door.
#   - A Span is a single leg or chapter inside that journey. For example, if a user queries an AI agent,
#     the entire process is the TRACE, and "database lookup", "vector search", and "LLM completion" are
#     individual SPANS inside that trace.
#
# WHAT IS LATENCY?
#   Latency is simply the wait time or "delay" between sending a command and receiving the response.
#   For example, if you press "Enter" on a prompt and it takes exactly 4.2 seconds for the first token
#   to appear on your screen, that 4.2 seconds is the latency!
#
# Let's write a beautiful, production-ready Pipeline Trace Logger class in Python.
# It automatically tracks execution spans, timestamps, prompt structures,
# response latencies, and token expenditures, outputting a complete, audit-friendly JSON trace!

# print("\n--- 2. THE AGENT TELEMETRY TRACER ---")

class LLMPipelineTracer:
    def __init__(self, trace_name):
        self.trace_id = str(uuid.uuid4())
        self.trace_name = trace_name
        self.spans = []
        self.total_tokens = 0
        self.total_cost = 0.0
        self.start_time = time.perf_counter()
        
    def start_span(self, name, inputs):
        # Starts a nested execution span (e.g. database query, LLM call)
        span_id = str(uuid.uuid4())[:8]
        span = {
            "span_id": span_id,
            "name": name,
            "inputs": inputs,
            "start_time": time.perf_counter(),
            "status": "active"
        }
        self.spans.append(span)
        print(f"  [Trace Span Started]: '{name}' (ID: {span_id})")
        return span_id
        
    def end_span(self, span_id, outputs, token_usage=None):
        end_time = time.perf_counter()
        
        # Locate active span
        for span in self.spans:
            if span["span_id"] == span_id and span["status"] == "active":
                span["status"] = "success"
                span["outputs"] = outputs
                # Calculate precision latency
                span["latency_seconds"] = round(end_time - span["start_time"], 4)
                
                # If LLM tokens were consumed, calculate costs (e.g. GPT-4 pricing)
                if token_usage:
                    prompt_t = token_usage.get("prompt_tokens", 0)
                    completion_t = token_usage.get("completion_tokens", 0)
                    
                    # Mock pricing: $5 per million prompt tokens, $15 per million completion tokens
                    cost = (prompt_t * 0.000005) + (completion_t * 0.000015)
                    
                    span["token_usage"] = token_usage
                    span["cost_usd"] = round(cost, 6)
                    self.total_tokens += (prompt_t + completion_t)
                    self.total_cost += cost
                    
                print(f"  [Trace Span Finished]: '{span['name']}' (Took {span['latency_seconds']}s) [Cost: ${span.get('cost_usd', 0.0):.6f}]")
                return
                
    def compile_trace_report(self):
        total_latency = round(time.perf_counter() - self.start_time, 4)
        report = {
            "trace_id": self.trace_id,
            "trace_name": self.trace_name,
            "total_latency_seconds": total_latency,
            "total_tokens": self.total_tokens,
            "total_cost_usd": round(self.total_cost, 6),
            "spans": self.spans
        }
        return report

# 1. Initialize tracer for a Customer Search pipeline
tracer = LLMPipelineTracer("Customer Support Agent Run")

# 2. Simulate Step 1: Database retrieval
span_db = tracer.start_span("database_lookup", {"user_id": 101})
time.sleep(0.3) # Simulate query latency
db_result = {"user_id": 101, "name": "Bob", "tier": "premium"}
tracer.end_span(span_db, db_result)

# 3. Simulate Step 2: LLM API Completion
prompt_template = "Generate welcome greeting for customer {name} (Tier: {tier})."
prompt_filled = prompt_template.format(**db_result)

span_llm = tracer.start_span("llm_completion", {"prompt": prompt_filled, "model": "gpt-4o"})
time.sleep(1.2) # Simulate LLM API completion delay
mock_completion = "Welcome back Bob! Thank you for being a premium subscriber."

# Track tokens returned by API metadata
tokens_meta = {"prompt_tokens": 45, "completion_tokens": 12}
tracer.end_span(span_llm, {"completion": mock_completion}, token_usage=tokens_meta)

# 4. Compile and print final telemetry report
report = tracer.compile_trace_report()
print("\n========================================")
print("     COMPILED AGENT TELEMETRY TRACE LOG")
print("========================================")
print(json.dumps(report, indent=2))
print("========================================\n")


# === EVALUATION & HALLUCINATION CHECKERS =================─────────────────────
#
# Once telemetry traces are saved, you can run automated evaluation rules:
#   - Latency checks: Alert if LLM calls take longer than 8 seconds.
#   - Cost alerts: Alert if single prompts consume more than $0.10.
#   - Hallucination checks: Run a secondary, cheap model to cross-examine if the
#     retrieved database facts match the LLM generated response exactly.

# print("--- 3. THE LLMops AUDIT LAYER ---")
print("  Save Trace ──► [ Check Latency / Costs ] ──► [ Secondary Eval Check ] ──► Deploy safely")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Overlooking telemetry logs when debugging
#   Don't waste time trying to guess why your LLM returned bad answers by changing the prompt
#   randomly. Pull the trace from your log dashboard, inspect the exact variables that went in,
#   and debug the context systematically.

# MISTAKE 2: Storing plain text prompts inside GDPR-sensitive regions
#   User prompts often contain private emails, names, or keys. In production, ensure
#   your tracing endpoints redact private information (PII) before uploading to external servers.

# MISTAKE 3: Running synchronous tracing blocking API requests
#   Logging telemetry should never make your app slow. Make sure your tracing SDKs
#   run asynchronously in the background (`async` or thread pool queues) so they don't delay
#   the response returned to the user.


# === EXERCISES ================================================================
#
# Exercise 1: Extend our `LLMPipelineTracer` to catch and record exceptions. Add a
#             `fail_span(span_id, error_message)` method that switches status to "failed"
#             and stores the error.
#
# Exercise 2: Explain why measuring prompt token costs vs completion token costs is
#             necessary (completion tokens are typically 3x more expensive!).

# === SOLUTIONS ================================================================
#
# Exercise 1:
# # (Inside LLMPipelineTracer class):
# # def fail_span(self, span_id, error):
# #     for span in self.spans:
# #         if span["span_id"] == span_id:
# #             span["status"] = "failed"
# #             span["error"] = error
# #             span["latency_seconds"] = round(time.perf_counter() - span["start_time"], 4)


# === KEY TAKEAWAYS ============================================================
#
# - AI observability demands deep tracing of prompts, inputs, and tokens inside loops.
# - Telemetry tracers partition pipelines into logical segments called spans.
# - Response timing (latency) and token cost calculations isolate bottleneck loops.
# - Logging detailed inputs and outputs creates durable audit trails for safety.
# - Asynchronous logging ensures monitoring utilities never delay front-end response times.
