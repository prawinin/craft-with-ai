# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 24: Data Schemas & Validation with Pydantic
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - Why data validation is crucial for system boundary security
    - Declaring Pydantic Models using standard Python type hints
    - Enforcing strict constraints (string lengths, value ranges)
    - Handling ValidationErrors and extracting clean error dictionaries
    - Serializing Pydantic models to dicts and JSON strings (.model_dump())
    - Why Pydantic is the absolute core to LLM Structured Outputs

  Why this matters for AI:
    LLMs are highly descriptive but notoriously unpredictable. They might return
    missing fields, incorrect data types, or invalid formats. By defining
    a Pydantic schema, you establish a contract. You can validate LLM outputs
    instantly, catch invalid responses at the boundary, and tell the LLM exactly
    what validation rule it broke so it can correct itself.

  Estimated time: 20 minutes

===============================================================================
"""

print("--- 1. THE VALIDATION CONTRACT BOUNDARY ---")
print("Incoming Data (Untrusted) ──► [ Pydantic Schema Validation ] ──► System Logic (Safe)")

try:
    from pydantic import BaseModel, Field, ValidationError, EmailStr
    from typing import List, Optional
    
    # We will declare a schema representing an AI Prompt Configuration:
    class ModelConfig(BaseModel):
        model_name: str = Field(..., description="The ID of the target LLM")
        temperature: float = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
        max_tokens: int = Field(500, gt=0, description="Max generated tokens limit")
        stop_sequences: Optional[List[str]] = Field(None, description="Optional stop sequences")
        
    # We will declare a schema representing a structured response from an AI Review Agent:
    class CodeReview(BaseModel):
        file_path: str
        has_bugs: bool
        complexity_score: int = Field(..., ge=1, le=10)
        bug_descriptions: List[str] = Field(default_factory=list)
        suggested_fix: Optional[str] = None
        
    pydantic_installed = True
except ImportError:
    # Safe fallback explanation if executed before pip installation
    pydantic_installed = False
    print("\n[Dependency Notice]: Pydantic must be installed using 'pip install pydantic' to execute this script.")


# === DECLARING AND USING PYDANTIC SCHEMAS ====================================
#
# WHAT IS A SCHEMA?
#   Think of a schema as a mold or a cookie cutter. If you want to bake stars, you press the star
#   cookie cutter down. Any dough that doesn't fit in the shape is squeezed out. In data science
#   and APIs, a schema is a blueprint that defines exactly what shape your data must take: which
#   keys must be present, what types of values are allowed, and what bounds they must stay within.
#
# WHAT IS VALIDATION?
#   Validation is like a security guard at an exclusive nightclub. The guard checks every guest
#   against a strict list of rules: "Are you wearing shoes? Are you over 21? Is your name on the list?"
#   If any guest breaks a rule, they are rejected immediately at the door. Data validation is doing
#   this to incoming data before it gets anywhere near your application's core logic or database!
#
# WHAT IS A TYPE ANNOTATION?
#   In Python, variables are normally highly flexible: a variable named `x` could hold a number now,
#   and a string later. A Type Annotation is like putting a label on a storage box that says "CANNED SOUP ONLY".
#   It tells Python (and developers) that a specific variable or function parameter is only supposed to
#   hold a specific type of data (like `int`, `str`, or `float`).
#
# A Pydantic model is a class that inherits from BaseModel.
# It automatically parses input dictionaries, converts types where possible
# (e.g. converting string "500" to integer 500), and validates constraints.

if pydantic_installed:
    print("\n--- 2. PARSING & VALIDATING MODELS ---")
    
    valid_input = {
        "model_name": "gpt-4o",
        "temperature": "1.2",  # Pydantic will automatically cast this string to float!
        "max_tokens": 1000
    }
    
    try:
        config = ModelConfig(**valid_input)
        print("Success! Model parsed successfully:")
        print(f"  Model: {config.model_name}")
        print(f"  Temperature (Casted to float): {config.temperature}")
        print(f"  Max Tokens: {config.max_tokens}")
    except ValidationError as e:
        print(f"Unexpected Validation Error: {e}")


# === HANDLING VALIDATION ERRORS ==============================================
#
# If the input data violates any rule (e.g., negative token count, temperature
# out of range, missing fields), Pydantic raises a ValidationError containing
# the exact location and reason for the crash.

if pydantic_installed:
    print("\n--- 3. CATCHING VALIDATION CRASHES ---")
    
    invalid_input = {
        "model_name": "gemini-1.5",
        "temperature": 2.5,  # Invalid: must be <= 2.0
        "max_tokens": -50   # Invalid: must be > 0
    }
    
    try:
        config = ModelConfig(**invalid_input)
    except ValidationError as e:
        print("Caught validation error successfully! Detailed error details:")
        # We can extract errors as a clean list of dictionaries:
        error_details = e.errors()
        for idx, err in enumerate(error_details, start=1):
            field = " -> ".join(str(p) for p in err["loc"])
            message = err["msg"]
            print(f"  Error #{idx}: Field '{field}' failed validation: {message}")


# === SERIALIZATION (model_dump & model_dump_json) ===========================
#
# WHAT IS SERIALIZATION?
#   Serialization is the process of flattening a complex 3D object into a 1D flat pack for shipping.
#   In memory, your Python program might have a complex web of interconnected classes and objects (3D).
#   To send it over the internet via HTTP, you must convert it into a flat, readable string (like a JSON
#   text file). Converting an object into text is "Serialization" (or "Marshalling"); rebuilding the 3D
#   object from the text on the receiving end is "Deserialization".
#
# Once validated, you can serialize Pydantic objects back to standard Python
# dictionaries or JSON strings:
#   .model_dump()      - Converts model to a standard dict
#   .model_dump_json() - Converts model to a minified JSON string

if pydantic_installed:
    print("\n--- 4. DATA SERIALIZATION ---")
    
    review = CodeReview(
        file_path="src/auth.py",
        has_bugs=True,
        complexity_score=8,
        bug_descriptions=["Plaintext password exposure on line 12", "Missing token validation"],
        suggested_fix="Use bcrypt for hashing and verify JWT signature."
    )
    
    # Dump to dict:
    review_dict = review.model_dump()
    print(f"Dumped Dict Type: {type(review_dict)}")
    print(f"Dumped Dict Content: {review_dict}")
    
    # Dump to JSON String (for web endpoints or logs):
    review_json = review.model_dump_json(indent=2)
    print(f"Dumped JSON string:\n{review_json}")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Modifying fields directly without validation
#   Pydantic objects by default allow mutability, but mutating values (e.g. config.max_tokens = -100)
#   doesn't trigger validation checks again. Always validate at creation or use validation modes.

# MISTAKE 2: Passing raw data payloads directly to databases
#   Never save request dicts directly. Load them into Pydantic models first. This sanitizes
#   the input data, filters out malicious unexpected columns, and guarantees database health.

# MISTAKE 3: Using generic type hints when constraints exist
#   Don't just use `temperature: float`. Use `Field(..., ge=0.0, le=2.0)` to enforce boundaries.
#   It prevents bad LLM tokens from crashing your production servers.


# === EXERCISES ================================================================
#
# Exercise 1: Create a Pydantic schema `UserAccount` containing `username` (min length 3),
#             `email` (string), and `is_active` (boolean, default True).
#             Test it with valid and invalid inputs, catching the ValidationError.
#
# Exercise 2: Write a python expression to load a JSON string representing a code review
#             directly into the `CodeReview` Pydantic model.

# === SOLUTIONS ================================================================
#
# Exercise 1:
# class UserAccount(BaseModel):
#     username: str = Field(..., min_length=3)
#     email: str
#     is_active: bool = True
#
# Exercise 2:
# # string_json = '{"file_path": "main.py", "has_bugs": false, "complexity_score": 3}'
# # review = CodeReview.model_validate_json(string_json)


# === KEY TAKEAWAYS ============================================================
#
# - Pydantic provides runtime type enforcement and constraints checking for Python.
# - Validation at boundaries filters out corrupted data and ensures database security.
# - casting allows strings and floats to bridge gracefully across request layers.
# - Pydantic models serialize effortlessly into standard dicts and JSON payloads.
# - Pydantic schemas are the absolute best way to programmatically force LLMs to output JSON.
