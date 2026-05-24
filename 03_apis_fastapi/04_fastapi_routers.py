# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 26: Building APIs with FastAPI & Routers
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - Instantiating a FastAPI application
    - Declaring routes and mapping HTTP methods (@app.get, @app.post)
    - Automatically binding Pydantic schemas for input request validation
    - Configuring CORS (Cross-Origin Resource Sharing) middleware
    - Running the API server locally using Uvicorn
    - Navigating and using the auto-generated Swagger Docs (/docs)

  Why this matters for AI:
    FastAPI is the industry standard for exposing Python-based AI models.
    Because it relies on standard Python type hints, modern AI coding assistants
    (like Copilot, Claude, or Gemini) can write accurate, bug-free FastAPI routers
    with zero boilerplate. It is the ultimate tool to ship your AI pipeline.

  Estimated time: 25 minutes

===============================================================================
"""

print("--- 1. FASTAPI HIGH-LEVEL ARCHITECTURE ---")
print("  FastAPI app  ──► Router Endpoints ──► Pydantic schemas ──► Uvicorn Server")

try:
    from fastapi import FastAPI, HTTPException, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
    from typing import List, Dict
    
    # 1. Instantiate the Core API application
    app = FastAPI(
        title="AI Automation Backend",
        description="Enterprise API endpoint for LLM prompt processing",
        version="1.0.0"
    )
    
    # 2. CORS Middleware Setup
    # CORS (Cross-Origin Resource Sharing) is a security standard enforced by browsers.
    # Without this middleware, if a frontend (React/HTML on port 3000) tries to call
    # your backend (Python on port 8000), the browser will block the call with a CORS error!
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],       # Allows all domains (use specific domains in production)
        allow_credentials=True,
        allow_methods=["*"],       # Allows all HTTP methods (GET, POST, etc.)
        allow_headers=["*"],       # Allows all headers
    )
    
    # 3. Define Input and Output Validation Schemas
    class CompletionRequest(BaseModel):
        prompt: str = Field(..., min_length=5, description="Input prompt for the model")
        max_tokens: int = Field(150, gt=0, le=1000)
        temperature: float = Field(0.7, ge=0.0, le=1.0)

    class CompletionResponse(BaseModel):
        prompt_received: str
        completion: str
        tokens_used: int
        status: str = "success"

    fastapi_installed = True
except ImportError:
    fastapi_installed = False
    print("\n[Dependency Notice]: FastAPI and Uvicorn must be installed to run this endpoint.")


# === DECLARING ROUTE PATHS & REQUEST BINDING =================================
#
# WHAT IS A ROUTER?
#   Think of a router like a switchboard operator at a company's front desk. When a customer calls and
#   says "I want to talk to Billing" (POST /billing), the switchboard operator routes the call to the
#   Billing department. In web frameworks, a router directs incoming HTTP requests to the exact Python
#   function written to handle that specific URL path.
#
# WHAT IS AN ENDPOINT?
#   An endpoint is a specific URL that a web service exposes, acting like a direct phone number or mailbox
#   for a particular department. For example, `http://api.com/api/generate` is the exact "endpoint" where
#   you send prompts to get AI predictions.
#
# WHAT IS MIDDLEWARE?
#   Middleware is like a security checkpoint in an airport lobby. Before a passenger (HTTP request)
#   can reach their gate (your router endpoint), they must walk through security. The security officers
#   inspect their bags, check their passports, and verify their boarding pass. If anything is wrong,
#   they reject them before they even step foot inside the terminal. Middleware runs before and after
#   every request, handling cross-cutting issues like CORS security, logging, or authentication!
#
# FastAPI routes are declared using Python decorators.
# When a client makes a POST request to '/api/generate', FastAPI automatically:
#   1. Reads the raw JSON body from the request.
#   2. Validates it against our `CompletionRequest` Pydantic model.
#   3. Passes the parsed model directly as the `payload` argument to our function!
#   4. If validation fails, it automatically returns a 422 error detailing the issues.

if fastapi_installed:
    # 1. Root diagnostic endpoint (GET /)
    @app.get("/", tags=["Diagnostics"])
    async def read_root():
        return {
            "status": "online",
            "service": "AI Engine Core Backend API",
            "documentation": "/docs"  # Path to auto-generated interactive swagger UI!
        }
        
    # 2. Core AI completion route (POST /api/generate)
    # FastAPI automatically serializes the returned dict or Pydantic model into JSON!
    @app.post("/api/generate", response_model=CompletionResponse, tags=["AI Core"])
    async def generate_text_completion(payload: CompletionRequest):
        print(f"Received completion request for prompt: '{payload.prompt}'")
        
        # Simulate AI generation pipeline
        mock_completion = f"Processed text output for prompt: '{payload.prompt}' under temp {payload.temperature}"
        
        # Return response matching our CompletionResponse Pydantic validation schema
        return CompletionResponse(
            prompt_received=payload.prompt,
            completion=mock_completion,
            tokens_used=len(payload.prompt.split()) + 30
        )

    # 3. Dynamic Path Parameters (GET /api/models/{model_id})
    @app.get("/api/models/{model_id}", tags=["Models"])
    async def get_model_metadata(model_id: str, detailed: bool = False):
        # 'detailed' is a query parameter, e.g. /api/models/gpt-4?detailed=true
        valid_models = {"gpt-4", "gemini-1.5", "claude-3"}
        if model_id not in valid_models:
            # Raise an HTTPException, returning a clean 404 response to the user
            raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found.")
            
        metadata = {
            "model_id": model_id,
            "provider": "OpenAI" if "gpt" in model_id else "Google/Anthropic",
            "context_window": 128000
        }
        
        if detailed:
            metadata["supported_features"] = ["text", "vision", "tool-calling"]
            
        return metadata

    # 4. Dependency Injection (Security Example)
    # 
    # WHAT IS DEPENDENCY INJECTION?
    #   Imagine you are a chef. Instead of fetching ingredients yourself every time,
    #   a kitchen assistant hands you exactly what you need as you start cooking.
    #   In FastAPI, `Depends` tells the framework to run a helper function FIRST,
    #   and hand its result to your endpoint. We use this heavily for authentication!
    
    from fastapi import Header
    
    async def verify_api_key(x_api_key: str = Header(...)):
        """A dependency function that checks for a valid API key header."""
        if x_api_key != "sk-my-secret-ai-key":
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
        return x_api_key

    @app.get("/api/secure-data", tags=["Security"])
    async def get_secure_data(api_key: str = Depends(verify_api_key)):
        # If we reach this line, the dependency passed!
        return {"message": "You have accessed the secure AI enclave.", "key_used": api_key}


# === RUNNING THE FASTAPI SERVER WITH UVICORN =================================
#
# Unlike standard Django or Flask scripts that you just "run", FastAPI relies on
# an ASGI server called `Uvicorn`. If you run this file directly via `python`,
# it will just print diagnostic text and exit. You must host it via Uvicorn!
#
# HOW TO RUN THIS SERVER:
#   1. Save this file locally as `main.py`
#   2. Open your terminal in the same folder.
#   3. Run the following command:
#
#      uvicorn main:app --reload --port 8000
#
#   Explanation:
#   - `main`: The name of your python file (without .py)
#   - `app`: The name of the FastAPI() instance variable inside that file
#   - `--reload`: Auto-restarts the server whenever you save code changes!
#
#   4. Open your browser and navigate to:
#      - http://127.0.0.1:8000/      (Returns the diagnostic JSON)
#      - http://127.0.0.1:8000/docs  (Launches the fully interactive Swagger Playground!)


if __name__ == "__main__":
    print("\n--- 2. RUNNING THE SERVER ---")
    print("To run the FastAPI server, use uvicorn in your terminal:")
    print("  uvicorn main:app --reload --port 8000")
    print("\nOnce started, navigate to http://127.0.0.1:8000/docs to interact with your endpoints.")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Forgetting to return a value in async endpoints
#   If you omit a `return` statement in your route functions, FastAPI will return
#   `null` with status `200 OK`, which will crash frontends expecting a JSON dictionary.

# MISTAKE 2: Not using HTTPException for errors
#   Do not use raw `raise ValueError` inside your routers. Pydantic/FastAPI will capture
#   unhandled exceptions and return a `500 Internal Server Error`. Always wrap known errors
#   in `raise HTTPException(status_code=..., detail=...)`.

# MISTAKE 3: Omitting CORS config when connecting to web applications
#   If your React or Vue frontend gets `Blocked by CORS policy` errors, verify that
#   you added the `CORSMiddleware` and allowed the origin domains inside your `app` configuration.


# === EXERCISES ================================================================
#
# Exercise 1: Declare a new POST endpoint at `/api/sentiment` that takes an input
#             schema with a single string field `text` (min length 10), processes it,
#             and returns a response dict: `{"sentiment": "positive", "score": 0.85}`.
#
# Exercise 2: Add a path parameter endpoint `/api/status/{service}` that returns
#             `{"service": service, "online": true}` if service is "api" or "db",
#             and raises a 400 Bad Request exception otherwise.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# class SentimentRequest(BaseModel):
#     text: str = Field(..., min_length=10)
#
# @app.post("/api/sentiment")
# async def check_sentiment(payload: SentimentRequest):
#     return {"sentiment": "positive", "score": 0.85}
#
# Exercise 2:
# @app.get("/api/status/{service}")
# async def get_service_status(service: str):
#     if service not in {"api", "db"}:
#         raise HTTPException(status_code=400, detail="Invalid service component")
#     return {"service": service, "online": True}


# === KEY TAKEAWAYS ============================================================
#
# - FastAPI leverages type hints to automate request parsing and schema validation.
# - `@app.get` and `@app.post` map routes directly to asynchronous python operations.
# - CORS middleware bridges communication across different browser domains.
# - Interactive API docs are generated out-of-the-box at `/docs` (using Swagger UI).
# - Uvicorn acts as the high-concurrency execution layer that hosts the FastAPI application.
