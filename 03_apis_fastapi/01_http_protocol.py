# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 23: Service Layers & The HTTP Protocol
  Difficulty: Beginner-Intermediate
===============================================================================

  What you will learn:
    - The Request-Response cycle of the World Wide Web
    - HTTP Verbs / Methods (GET, POST, PUT, DELETE)
    - Request components: Headers, URL Query parameters, and JSON payloads
    - Response components: Headers, Data, and standard Status Codes
    - Simulating and calling REST APIs using Python's standard libraries

  Why this matters for AI:
    Your AI models cannot live in isolation. To build a chat interface,
    retrieve live data, or connect your AI pipeline to a React frontend,
    you must expose your Python models as web services. Understanding how HTTP
    transfers structured JSON data is the first step to API building.

  Estimated time: 20 minutes

===============================================================================
"""

import urllib.request
import urllib.parse
import json
import socket

# === THE REQUEST-RESPONSE CYCLE =============================================
#
# WHAT IS A PROTOCOL?
#   Think of a protocol as a polite agreement on social etiquette. If two people meet,
#   they agree on a protocol: make eye contact, say "Hello", shake hands. If one person
#   starts singing in opera while the other tries to speak sign language, communication breaks down.
#   In networking, a protocol is a strict set of rules that computers agree to follow so they
#   can exchange information without getting confused.
#
# WHAT IS HTTP?
#   HTTP (HyperText Transfer Protocol) is the language that browsers and servers
#   use to talk to each other. Think of it like ordering food at a restaurant:
#   you (the client) place an ORDER (request), and the kitchen (server) sends
#   back your DISH (response). Every time you open a webpage, that's HTTP.
#
# WHAT IS A REST API?
#   REST (Representational State Transfer) is a style of building APIs where
#   each URL represents a "resource" (like a user, a product, an AI model) and
#   you use HTTP methods (GET, POST, etc.) to interact with it. It's the most
#   common way AI backends expose their capabilities to frontends.
#
# Web services communicate via HTTP. A client (e.g. your browser or an AI agent)
# sends a REQUEST, and a server returns a RESPONSE.
#
# Anatomy of an HTTP Request:
#   1. Method/Verb : What action are we performing? (GET, POST)
#   2. URL Path    : Where is the resource? (e.g. /api/predict)
#   3. Headers     : Metadata (e.g. Content-Type: application/json, Authorization)
#   4. Body        : Optional payload data (typically a JSON string)

# print("--- 1. HTTP METHOD VERBS & ACTIONS ---")
print("  GET    - Retrieve data (e.g., fetch agent status)")
print("  POST   - Create/Send data (e.g., send prompt to LLM to get completion)")
print("  PUT    - Update existing data (e.g., adjust model configurations)")
print("  DELETE - Remove data (e.g., delete chat session memory)")


# === HTTP STATUS CODES =======================================================
#
# WHAT IS AN HTTP STATUS CODE?
#   An HTTP Status Code is like a quick thumbs-up or thumbs-down signal from the server's kitchen.
#   Instead of writing a long letter, the server returns a three-digit code:
#   200 means "Got it, here's your food!", 404 means "We checked the menu, we don't serve that!",
#   and 500 means "The kitchen is on fire!"
#
# Every response includes a numeric status code indicating the outcome:
#   200 OK           - Action succeeded
#   201 Created      - Resource successfully created
#   400 Bad Request  - Client error (validation failed or malformed JSON)
#   401 Unauthorized - Authentication required (missing API key)
#   404 Not Found    - Resource path does not exist
#   500 Server Error - The server crashed while processing the request

# print("\n--- 2. COMMON HTTP STATUS CODES ---")
# 1xx: Informational | 2xx: Success | 3xx: Redirect | 4xx: Client Error | 5xx: Server Error


# === CALLING AN API PROGRAMMATICALLY ========================================
#
# WHAT IS AN HTTP HEADER?
#   HTTP Headers are like the shipping label on a cardboard box. The box itself contains
#   the actual cargo (the body/payload), but the shipping label (headers) tells the server
#   crucial details: who sent it, what kind of cargo is inside (e.g. JSON vs. an image),
#   and any security badges (API keys) required to open it.
#
# WHAT IS A JSON PAYLOAD?
#   A "payload" or "body" is the actual cargo or message inside our HTTP box.
#   JSON (JavaScript Object Notation) is the format we write this message in. Think of JSON
#   like a standard shipping manifest written in a language that every programming language in
#   the world understands. It's organized in clean key-value pairs, just like a Python dictionary!
#
# Let's perform a real GET and POST request in pure Python using the built-in
# `urllib` library. This is extremely robust and requires zero dependencies.

# print("\n--- 3. LIVE GET & POST API CALLS ---")

# Let's write a safe function that fetches data (GET) with a connection timeout
def fetch_mock_todo(todo_id):
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
    print(f"GET Request to: {url}")
    
    try:
        # Open URL with a 5-second timeout (prevents hanging if offline)
        with urllib.request.urlopen(url, timeout=5) as response:
            status = response.status
            body = response.read().decode("utf-8")
            data = json.loads(body)
            return status, data
    except Exception as e:
        # Fallback if connection fails (e.g., offline mode)
        return 200, {
            "id": todo_id,
            "title": "[Offline Mode] Mock AI Task description",
            "completed": False,
            "offline": True
        }

status_code, todo_item = fetch_mock_todo(1)
print(f"Response Status: {status_code}")
print(f"Todo Data: {todo_item['title']} (Completed: {todo_item['completed']})")

# Let's perform a POST request (simulates sending a prompt input to an AI endpoint)
def send_mock_prompt(prompt, max_tokens=150):
    url = "https://jsonplaceholder.typicode.com/posts"
    headers = {"Content-Type": "application/json"}
    payload = {
        "title": "LLM_Prompt",
        "body": prompt,
        "max_tokens": max_tokens,
        "userId": 1
    }
    
    # Encode payload to bytes
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            body = response.read().decode("utf-8")
            return status, json.loads(body)
    except Exception:
        # Fallback offline mode
        payload["id"] = 101 # Mocked database ID returned by post
        return 201, payload

print("\nSending mock AI POST request:")
post_status, response_data = send_mock_prompt("Translate 'Hello World' to French", max_tokens=50)
print(f"Response Status: {post_status} (Created)")
print(f"Returned Data: {response_data}")


# === MOCKING AN API ROUTER IN PYTHON =======================================
#
# When building an API backend, your code parses incoming requests and routes
# them based on path rules. Let's see how simple routing works conceptually:

# print("\n--- 4. MOCKING AN API ROUTER ---")

class MockServer:
    def handle_request(self, method, path, headers, body=None):
        print(f"Mock Server Routing: {method} {path}")
        
        # Route 1: Get active models
        if method == "GET" and path == "/api/models":
            return 200, {"models": ["gpt-4o", "gemini-1.5-pro", "claude-3-sonnet"]}
            
        # Route 2: Generate completions
        if method == "POST" and path == "/api/completion":
            if not body:
                return 400, {"error": "Missing JSON request body"}
            
            try:
                data = json.loads(body)
                prompt = data.get("prompt", "")
                return 200, {
                    "completion": f"Mock response for prompt: '{prompt}'",
                    "tokens_used": 15
                }
            except json.JSONDecodeError:
                return 400, {"error": "Invalid JSON format"}
                
        # Route 3: Not Found fallback
        return 404, {"error": f"Endpoint {path} not found"}

server = MockServer()
# Test GET request
status, data = server.handle_request("GET", "/api/models", {})
print(f"GET /api/models: Status {status} -> {data}")

# Test POST request with body
body_json = '{"prompt": "Explain APIs simply"}'
status, data = server.handle_request("POST", "/api/completion", {}, body_json)
print(f"POST /api/completion: Status {status} -> {data['completion']}")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Forgetting to set Content-Type header on POST
#   If you send JSON data but omit the header `Content-Type: application/json`,
#   backend APIs will fail to parse your requests and return a 400 or 415 error.

# MISTAKE 2: Trying to send a request body inside a GET request
#   While technically possible in some configurations, HTTP standards specify
#   that GET requests should NOT have bodies. Use query params (e.g. /api?q=text) instead.

# MISTAKE 3: Using status 200 for every response (even errors!)
#   Never return `{"error": "Failed"}` alongside a `200 OK` status. If something fails,
#   return an appropriate `400` or `500` status so clients can handle it properly.


# === EXERCISES ================================================================
#
# Exercise 1: Write a function `build_query_string(base_url, params)` that takes a URL
#             string and a dict of parameters, and returns a fully formatted GET URL.
#             Example: build_query_string("http://api.com", {"q": "python", "p": 1})
#                      -> "http://api.com?q=python&p=1"
#
# Exercise 2: Extend the `MockServer` class to support a DELETE route at `/api/session`
#             that returns status 200 and a message `{"status": "Session wiped"}`.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# def build_query_string(base_url, params):
#     if not params:
#         return base_url
#     query = urllib.parse.urlencode(params)
#     return f"{base_url}?{query}"
#
# Exercise 2:
# # (Add inside class router):
# # if method == "DELETE" and path == "/api/session":
# #     return 200, {"status": "Session wiped"}


# === KEY TAKEAWAYS ============================================================
#
# - APIs (Application Programming Interfaces) are the glue of modern web systems.
# - GET is for read-only retrieval; POST is for modifications or data transfers.
# - Headers store critical metadata, authorization keys, and payload content types.
# - Clean JSON serialization is the language of communication between modern platforms.
# - Status codes provide standard structural protocols to tell clients if calls succeeded.
