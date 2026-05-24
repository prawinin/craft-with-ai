# Copyright (c) 2026 Prawin Kumar

"""
===============================================================================
  PYTHON FOR AI -- Lesson 32: Structured Outputs & JSON Self-Correction
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - The problem with raw text completions (Markdown blocks, invalid formatting)
    - Structured Outputs: Enforcing strict JSON Schemas at the API level
    - Cleaning "dirty" raw strings returned by models (stripping markdown backticks)
    - Validating JSON schemas dynamically using Pydantic models
    - The Self-Correction Loop: Forcing the LLM to heal its own validation errors

  Why this matters for AI:
    If your AI pipeline extracts information or routes actions, you cannot parse
    free-form paragraphs. You need a clean, standard JSON payload. If the model returns
    broken syntax (like trailing commas or markdown wraps), your backend code will crash.
    Combining Pydantic validation with a self-correction prompt loop creates
    100% resilient structured AI integrations.

  Estimated time: 25 minutes

===============================================================================
"""

import json
import re
try:
    from pydantic import BaseModel, Field, ValidationError
    pydantic_installed = True
except ImportError:
    pydantic_installed = False

# === THE UNRELIABLE TEXT PROBLEM =============================================
#
# WHAT IS A STRUCTURED OUTPUT?
#   Imagine asking a chef to write a recipe. They might write a poetic story about their grandmother
#   and lists of ingredients in different places (unstructured). If you ask them to write it on a strict,
#   numbered recipe card with specific boxes for "Time", "Ingredients", and "Steps", that is a Structured Output.
#   In AI, structured output is forcing the LLM to output its response in a strict data format (like JSON)
#   matching a pre-defined schema, so your code can read it instantly without cracking.
#
# WHAT IS A JSON SCHEMA?
#   Think of a JSON Schema like an application form with strict formatting instructions.
#   It doesn't just say "Write your name"; it says "Your name must be a string between 2 and 50 characters,
#   and your birth year must be an integer between 1900 and 2026." It defines the exact keys, types, and
#   rules that a JSON document must follow to be considered valid.
#   (Schema and Validation explained fully in Module 3, Lesson 2 — "Data Schemas & Validation with Pydantic")
#
# WHAT IS AN AI HALLUCINATION?
#   Think of a hallucination like an overconfident candidate in an interview who doesn't know the answer
#   to a question, but instead of saying "I don't know," they confidently make up a completely fake,
#   highly detailed story that sounds incredibly convincing. Because LLMs are predictive engines (word autocompletes),
#   they are designed to write what sounds correct, which sometimes leads to them confidently generating
#   fake facts, fictitious variables, or invalid JSON properties!
#
# If you ask an LLM: "Return a JSON object with keys name and score", it will often
# return text wrapped in markdown blocks:
#
#   ```json
#   {
#     "name": "Alice",
#     "score": 90
#   }
#   ```
#
# Calling `json.loads()` on this raw string will raise a `json.JSONDecodeError`!
# We must clean this output before parsing it.

# print("--- 1. STRIP-CLEANING DIRTY LLM JSON OUTPUT ---")

dirty_llm_output = """
Here is the JSON you requested:
```json
{
  "name": "Chatbot Agent",
  "version": "1.0",
  "active": true
}
```
Let me know if you need anything else!
"""

# Let's write a robust parser function to extract only the JSON block!
def clean_and_extract_json(raw_string):
    # Regex 1: Search for text enclosed between ```json and ```
    match = re.search(r"```json\s*(.*?)\s*```", raw_string, re.DOTALL)
    if match:
        return match.group(1).strip()
        
    # Regex 2: Fallback to match text enclosed between ``` and ```
    match = re.search(r"```\s*(.*?)\s*```", raw_string, re.DOTALL)
    if match:
        return match.group(1).strip()
        
    # Fallback 3: Return raw string stripped
    return raw_string.strip()

cleaned_json = clean_and_extract_json(dirty_llm_output)
print(f"Raw String Length: {len(dirty_llm_output)}")
print(f"Cleaned JSON String:\n{cleaned_json}")

# Parse into standard dictionary
data_dict = json.loads(cleaned_json)
print(f"Parsed Dict: {data_dict} (Active: {data_dict['active']})")


# === SCHEMA ENFORCEMENT & SELF-CORRECTION ====================================
#
# If the parsed JSON dictionary is missing required fields or has incorrect types,
# our system fails. In a Self-Correction Loop:
#   1. We parse incoming JSON and validate it using Pydantic.
#   2. If it raises a `ValidationError`, we capture the error message.
#   3. We send the error message *back* to the LLM as a new prompt:
#      "Your previous JSON was invalid for rule X. Please rewrite it."
#   4. The model corrects itself, resulting in a self-healing pipeline!

if pydantic_installed:
    print("\n--- 2. THE SELF-CORRECTION PIPELINE ---")
    
    # Declare target schema representing a Customer Support Lead ticket
    class SupportTicket(BaseModel):
        customer_name: str = Field(..., min_length=2)
        category: str = Field(..., description="Must be either 'billing', 'technical', or 'general'")
        urgency_score: int = Field(..., ge=1, le=5)
        summary: str
        
    # Simulate a corrupted LLM response (category is invalid, urgency is out of range)
    invalid_llm_json = '{"customer_name": "Bob", "category": "refund_please", "urgency_score": 10, "summary": "Charged twice"}'
    
    # Let's write our Self-Correction validator simulation:
    def validate_or_request_correction(raw_json_str):
        print(f"Validating payload: {raw_json_str}")
        try:
            # Attempt parsing and validation
            ticket = SupportTicket.model_validate_json(raw_json_str)
            print("  [SUCCESS] Validation passed!")
            return ticket, None
        except ValidationError as e:
            # Capture errors
            errors = e.errors()
            error_msgs = []
            for err in errors:
                field = " -> ".join(str(p) for p in err["loc"])
                msg = err["msg"]
                error_msgs.append(f"Field '{field}': {msg}")
                
            error_report = "; ".join(error_msgs)
            print(f"  [VALIDATION FAILED]: {error_report}")
            
            # Formulate correction instruction to send back to LLM
            correction_prompt = (
                f"Your output was invalid against the required JSON schema.\n"
                f"Validation Errors: {error_report}\n"
                f"Please correct the JSON and return it strictly matching the schema."
            )
            return None, correction_prompt

    # First attempt: Fails
    ticket, correction_instruction = validate_or_request_correction(invalid_llm_json)
    
    print(f"\nPrompt generated to send back to LLM for Self-Healing:\n{correction_instruction}")
    
    # Simulate the LLM self-correcting and returning the corrected JSON
    corrected_llm_json = '{"customer_name": "Bob", "category": "billing", "urgency_score": 5, "summary": "Charged twice"}'
    
    # Second attempt: Succeeds!
    print("\nSimulating LLM Self-Healed Second Response:")
    ticket_fixed, _ = validate_or_request_correction(corrected_llm_json)
    print(f"Final Validated Object: {ticket_fixed.customer_name} - Category: {ticket_fixed.category} (Urgency: {ticket_fixed.urgency_score})")


# === MODERN SDK STRUCTURED OUTPUTS ===========================================
#
# Modern APIs (like OpenAI's `response_format` or Gemini's `response_schema`)
# enforce Pydantic structures natively at the token level, preventing syntactical failures.
#
# Example OpenAI configuration:
#   class Recipe(BaseModel):
#       name: str
#       ingredients: list[str]
#
#   completion = client.beta.chat.completions.parse(
#       model="gpt-4o",
#       messages=[{"role": "user", "content": "Suggest a soup"}],
#       response_format=Recipe,  # Enforces schema validation at API boundaries!
#   )
#   recipe = completion.choices[0].message.parsed
#   print(recipe.name)

# print("\n--- 3. 💡 PRO TIP: NATIVE API STRUCTURED OUTPUTS ---")
print("  Always prefer using native response_format or function calling configurations")
print("  (like client.beta.chat.completions.parse) to enforce JSON schemas at the API level.")


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Relying on prompt engineering alone for JSON output
#   Writing "Return ONLY JSON" in your prompt does NOT guarantee JSON. Under load,
#   the model will eventually output markdown or trailing text. Always use structured
#   output API settings or parse with robust cleaners.

# MISTAKE 2: Not cleaning markdown wrappers before parsing
#   Directly calling `json.loads(response_text)` without checking for ` ```json ` blocks
#   will crash your server on 30% of standard model responses.

# MISTAKE 3: Infinite self-correction loops
#   If your self-correction loop has no limit, and the model struggles to validate a rule,
#   it might run in an infinite loop, consuming all your API credits.
#   Always set a maximum retry threshold (e.g. limit to 2 correction attempts).


# === EXERCISES ================================================================
#
# Exercise 1: Extend `clean_and_extract_json` to handle cases where the JSON has leading
#             or trailing whitespace/paragraphs, extracting the substring starting
#             with `{` and ending with `}`.
#
# Exercise 2: Design a Pydantic schema `ClassificationResult` representing an email classifier,
#             with fields: `label` (spam, social, primary), `confidence` (float),
#             and `reason` (string, minimum 15 characters).

# === SOLUTIONS ================================================================
#
# Exercise 1:
# def find_bracket_json(raw):
#     start = raw.find("{")
#     end = raw.rfind("}")
#     if start != -1 and end != -1:
#         return raw[start:end+1]
#     return raw


# === KEY TAKEAWAYS ============================================================
#
# - Raw LLM text completions cannot be safely parsed without cleanup regex.
# - Structured outputs enforce JSON validation at the compilers token level.
# - Pydantic models act as runtime validation gates for unstructured LLM data.
# - Self-correction loops send validation errors back to LLMs to auto-heal payloads.
# - Limit retry attempts in correction pipelines to avoid credit drain loops.
