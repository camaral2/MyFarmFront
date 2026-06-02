import requests
import os

api_url = "http://127.0.0.1:8000"
endpoint = "/cost_credit"

try:
    print(f"Testing {api_url}{endpoint}...")
    response = requests.get(f"{api_url}{endpoint}")
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Content: {response.text[:500]}") # Print first 500 chars
except Exception as e:
    print(f"Error: {e}")

print("-" * 20)
endpoint_slash = "/cost_credit/"
try:
    print(f"Testing {api_url}{endpoint_slash}...")
    response = requests.get(f"{api_url}{endpoint_slash}")
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Content: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
