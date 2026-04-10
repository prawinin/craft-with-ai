# ─────────────────────────────────────────────────────────────────────────────
# Copyright (c) 2026 Prawin Kumar. All rights reserved.
# Licensed under CC BY-NC-ND 4.0 — learn freely, but do not sell or rebrand.
# See LICENSE file for full terms. GitHub: https://github.com/prawinin
# ─────────────────────────────────────────────────────────────────────────────

"""
===============================================================================
  PYTHON FOR AI -- Lesson 16: Working with APIs
  Difficulty: Intermediate
===============================================================================

  What you will learn:
    - What APIs are and why they matter
    - Making HTTP requests with the requests library
    - Understanding JSON responses
    - Building functions that call APIs
    - Working with query parameters
    - Error handling for network requests
    - Building a complete weather data tool

  Why this matters for AI:
    Modern AI applications rarely work in isolation. They call APIs to:
    - Get data (weather, stock prices, news articles)
    - Use AI services (OpenAI, Hugging Face, Google Cloud)
    - Send results (Slack notifications, database writes)
    Every AI agent, chatbot, and data pipeline depends on API calls.

  Estimated time: 30 minutes

  Prerequisites: pip install requests

===============================================================================
"""


# === WHAT IS AN API? ==========================================================
#
# API = Application Programming Interface
#
# Real-world analogy:
#   You go to a restaurant. You do not walk into the kitchen and cook.
#   Instead, you give your order to a WAITER (the API). The waiter takes
#   your request to the kitchen (the server), and brings back your food
#   (the response).
#
#   In programming:
#   - Your code is the customer
#   - The API is the waiter
#   - The server is the kitchen
#   - The response is the food
#
# APIs let your program talk to other programs over the internet.
# You send a REQUEST, the server processes it, and sends back a RESPONSE.


# === YOUR FIRST API CALL =====================================================

import requests

# Let's call a real API -- the Open-Meteo weather API (free, no key needed)
latitude = 48.85     # Paris
longitude = 2.35

url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m"

# Make the GET request:
response = requests.get(url)

# Check if it worked:
print(f"Status code: {response.status_code}")  # 200 = success
print(f"Response type: {type(response)}")

# Parse the JSON response into a Python dictionary:
data = response.json()
print(f"\nFull response:\n{data}")


# === UNDERSTANDING THE RESPONSE ===============================================
#
# The API sends back data in JSON format -- which Python reads as a dictionary.
#
# A typical weather API response looks like:
# {
#     "latitude": 48.84,
#     "longitude": 2.36,
#     "current": {
#         "time": "2026-08-01T08:30",
#         "temperature_2m": 20.0
#     },
#     "current_units": {
#         "temperature_2m": "C"
#     }
# }
#
# The temperature is NESTED inside the "current" section.
# To access it, you chain dictionary keys:

temperature = data["current"]["temperature_2m"]
print(f"\nCurrent temperature in Paris: {temperature}°C")

# What is JSON?
# JSON (JavaScript Object Notation) is a text format for structured data.
# It looks almost identical to Python dictionaries and lists.
# APIs universally use JSON to send and receive data.


# === BUILDING A REUSABLE FUNCTION ============================================

import requests

def get_weather(latitude, longitude):
    """
    Get current temperature for a location.

    Args:
        latitude: Geographic latitude (e.g., 48.85 for Paris)
        longitude: Geographic longitude (e.g., 2.35 for Paris)

    Returns:
        Current temperature in Celsius, or None if the request failed.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,wind_speed_10m"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: API returned status {response.status_code}")
        return None

    data = response.json()
    return data["current"]["temperature_2m"]


# Fetch temperatures for multiple cities:
cities = {
    "Paris": (48.85, 2.35),
    "London": (51.50, -0.12),
    "Tokyo": (35.68, 139.69),
    "New York": (40.71, -74.01),
    "Sydney": (-33.87, 151.21),
}

print("\n--- Current Temperatures ---")
for city, (lat, lon) in cities.items():
    temp = get_weather(lat, lon)
    if temp is not None:
        print(f"  {city}: {temp}°C")


# === HTTP METHODS =============================================================
#
# GET:    Retrieve data (weather, user info, search results)
# POST:   Send data to create something (submit form, upload file)
# PUT:    Update existing data
# DELETE: Remove data
#
# For most data fetching, you use GET. For AI API calls (like sending
# a prompt to GPT), you typically use POST.

# GET example:
response = requests.get("https://api.github.com")
print(f"\nGitHub API status: {response.status_code}")

# POST example (conceptual -- needs a real API endpoint):
# response = requests.post(
#     "https://api.openai.com/v1/chat/completions",
#     headers={"Authorization": "Bearer YOUR_API_KEY"},
#     json={
#         "model": "gpt-4",
#         "messages": [{"role": "user", "content": "Hello!"}]
#     }
# )


# === QUERY PARAMETERS =========================================================
#
# Instead of building URLs manually, use the params argument:

# Manual URL building (error-prone):
url = f"https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current=temperature_2m"

# Better -- using params dict:
base_url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 48.85,
    "longitude": 2.35,
    "current": "temperature_2m,wind_speed_10m",
}
response = requests.get(base_url, params=params)
print(f"\nUsing params: {response.status_code}")
print(f"Actual URL: {response.url}")


# === ERROR HANDLING FOR API CALLS =============================================
#
# Network requests can fail for many reasons: no internet, server down,
# invalid API key, rate limiting. Always handle errors.

def safe_api_call(url, params=None):
    """Make an API call with proper error handling."""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()    # Raises exception for 4xx/5xx codes
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server")
        return None
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {e.response.status_code}")
        return None
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not valid JSON")
        return None

# Use it:
data = safe_api_call("https://api.open-meteo.com/v1/forecast", {
    "latitude": 48.85,
    "longitude": 2.35,
    "current": "temperature_2m"
})
if data:
    print(f"Temperature: {data['current']['temperature_2m']}°C")


# === WORKING WITH HISTORICAL DATA ============================================

from datetime import datetime, timedelta

# Calculate date range:
today = datetime.now()
week_ago = today - timedelta(days=7)

start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

# Get past week's weather for Paris:
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 48.85,
    "longitude": 2.35,
    "start_date": start_date,
    "end_date": end_date,
    "daily": "temperature_2m_max,temperature_2m_min"
}

response = requests.get(url, params=params)
if response.status_code == 200:
    weather_data = response.json()
    daily = weather_data.get("daily", {})
    dates = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])

    print(f"\n--- Paris Weather: Past 7 Days ---")
    print(f"{'Date':<12} {'Max':>6} {'Min':>6}")
    print("-" * 26)
    for date, max_t, min_t in zip(dates, max_temps, min_temps):  # zip() was covered in 07_loops.py
        if max_t is not None and min_t is not None:
            print(f"{date:<12} {max_t:>5.1f}° {min_t:>5.1f}°")


# === REAL-WORLD EXAMPLE: BUILDING A WEATHER DASHBOARD ========================

def get_weather_report(city_name, lat, lon):
    """Get a comprehensive weather report for a city."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
    }

    data = safe_api_call("https://api.open-meteo.com/v1/forecast", params)
    if data is None:
        return None

    current = data.get("current", {})
    return {
        "city": city_name,
        "temperature": current.get("temperature_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "humidity": current.get("relative_humidity_2m"),
    }


def display_dashboard(reports):
    """Display weather reports in a formatted table."""
    print("\n" + "=" * 55)
    print("            WEATHER DASHBOARD")
    print("=" * 55)
    print(f"{'City':<15} {'Temp':>7} {'Wind':>8} {'Humidity':>10}")
    print("-" * 55)
    for r in reports:
        if r:
            temp = f"{r['temperature']}°C" if r['temperature'] else "N/A"
            wind = f"{r['wind_speed']} km/h" if r['wind_speed'] else "N/A"
            hum = f"{r['humidity']}%" if r['humidity'] else "N/A"
            print(f"{r['city']:<15} {temp:>7} {wind:>8} {hum:>10}")
    print("=" * 55)


# Build the dashboard:
cities_to_check = {
    "Paris": (48.85, 2.35),
    "London": (51.50, -0.12),
    "New York": (40.71, -74.01),
    "Tokyo": (35.68, 139.69),
}

reports = []
for city, (lat, lon) in cities_to_check.items():
    report = get_weather_report(city, lat, lon)
    reports.append(report)

display_dashboard(reports)


# === COMMON MISTAKES ==========================================================

# MISTAKE 1: Not checking the status code
# Wrong:
#   data = requests.get(url).json()  # Crashes if request failed
# Right:
#   response = requests.get(url)
#   if response.status_code == 200:
#       data = response.json()

# MISTAKE 2: Not handling network errors
# Always use try/except for network calls, or use the safe_api_call pattern.

# MISTAKE 3: Hardcoding API keys in your code
# Wrong:
#   headers = {"Authorization": "Bearer sk-abc123..."}
# Right: use environment variables
#   import os
#   api_key = os.getenv("OPENAI_API_KEY")
#   headers = {"Authorization": f"Bearer {api_key}"}

# MISTAKE 4: Not setting a timeout
# Wrong:
#   requests.get(url)      # Could hang forever
# Right:
#   requests.get(url, timeout=10)  # Timeout after 10 seconds

# MISTAKE 5: Naming your file "requests.py"
# This creates a circular import. Python imports YOUR file instead of
# the real requests library. Name your files descriptively.


# === EXERCISES ================================================================
#
# Exercise 1: Modify get_weather() to also return wind speed and humidity.
#             Print a formatted report for 3 cities of your choice.
#
# Exercise 2: Write a function that takes a city name and returns its
#             coordinates using a geocoding API:
#             https://geocoding-api.open-meteo.com/v1/search?name=Paris
#
# Exercise 3: Combine Exercise 1 and 2: write a function that takes just
#             a city NAME (string), finds its coordinates, then gets the
#             weather. One function call for everything.
#
# Exercise 4: Add error handling to your functions: handle connection
#             errors, invalid city names, and missing data in responses.


# === SOLUTIONS ================================================================
#
# Exercise 1:
# def get_full_weather(lat, lon):
#     params = {
#         "latitude": lat, "longitude": lon,
#         "current": "temperature_2m,wind_speed_10m,relative_humidity_2m"
#     }
#     data = safe_api_call("https://api.open-meteo.com/v1/forecast", params)
#     if data:
#         c = data["current"]
#         return c["temperature_2m"], c["wind_speed_10m"], c["relative_humidity_2m"]
#     return None, None, None
#
# for city, (lat, lon) in [("Delhi", 28.61, 77.23), ("Berlin", 52.52, 13.41)]:
#     temp, wind, hum = get_full_weather(lat, lon)
#     print(f"{city}: {temp}C, {wind} km/h wind, {hum}% humidity")
#
# Exercise 2:
# def geocode(city_name):
#     data = safe_api_call("https://geocoding-api.open-meteo.com/v1/search",
#                          {"name": city_name, "count": 1})
#     if data and "results" in data:
#         result = data["results"][0]
#         return result["latitude"], result["longitude"]
#     return None, None
#
# lat, lon = geocode("Tokyo")
# print(f"Tokyo: {lat}, {lon}")
#
# Exercise 3:
# def weather_by_name(city_name):
#     lat, lon = geocode(city_name)
#     if lat is None:
#         return f"Could not find {city_name}"
#     temp = get_weather(lat, lon)
#     return f"{city_name}: {temp}C"
#
# print(weather_by_name("Mumbai"))


# === KEY TAKEAWAYS ============================================================
#
# - APIs let your code communicate with remote services over the internet
# - Use requests.get() for fetching data, requests.post() for sending data
# - response.json() converts the JSON response to a Python dictionary
# - Always check response.status_code (200 = success)
# - Always handle errors (try/except) and set timeouts
# - Use params dict instead of manually building URLs
# - Never hardcode API keys -- use environment variables
# - JSON is the standard data format for API communication


# === WHAT'S NEXT? =============================================================
#
# In the next lesson (17_working_with_data.py), you will learn how to work
# with tabular data using pandas and create visualizations with matplotlib.
# This is where your AI journey starts getting tangible -- working with
# real datasets and seeing patterns in data.
