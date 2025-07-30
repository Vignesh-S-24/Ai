import os
import subprocess
import requests

# Get OpenRouter API key from environment
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ OPENROUTER_API_KEY is not set. Aborting.")
    exit(1)

# Ensure base branch exists for diff comparison
try:
    subprocess.run(["git", "fetch", "origin", "main"], check=True)
except subprocess.CalledProcessError as e:
    print("❌ Failed to fetch origin/main:", e)
    exit(1)

# Generate git diff (between origin/main and current HEAD)
try:
    diff_output = subprocess.check_output(["git", "diff", "origin/main...HEAD"]).decode("utf-8")
except subprocess.CalledProcessError as e:
    print("❌ Failed to get git diff:", e)
    exit(1)

# Truncate large diffs to avoid model token limits
MAX_DIFF_LENGTH = 15000
if len(diff_output) > MAX_DIFF_LENGTH:
    diff_output = diff_output[:MAX_DIFF_LENGTH] + "\n\n...[diff truncated due to length]"

# Improved AI prompt for structured review
prompt = f"""
You are a senior software engineer and expert code reviewer.

Please review the following Git diff and return a structured analysis with:

### 1. Summary
- Brief overview of what the change does

### 2. Code Quality Suggestions
- Suggestions for improving readability, maintainability, or performance

### 3. Potential Issues
- Highlight bugs, edge cases, or logic errors (if any)

### 4. Best Practice Compliance
- Mention if the code follows or violates known best practices

### 5. Optional Improvements
- Any optional design or architectural improvements

Use a professional tone. Be concise. Do not include generic advice. Only comment on what you see in the diff.

--- Begin Git Diff ---
{diff_output}
--- End Git Diff ---
"""

# OpenRouter API call setup
url = "https://openrouter.ai/api/v1/chat/completions"

try:
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/Vignesh-S-24/Ai",  # your repo URL
        },
        json={
            "model": "mistralai/mixtral-8x7b",
            "messages": [
                {"role": "system", "content": "You are a senior code reviewer."},
                {"role": "user", "content": prompt},
            ]
        },
        timeout=60
    )
except requests.exceptions.RequestException as e:
    print("❌ Request failed:", e)
    exit(1)

# Handle API response
if response.status_code != 200:
    print("❌ API Error:", response.status_code, response.text)
    exit(1)

try:
    review_output = response.json()["choices"][0]["message"]["content"]
except (KeyError, IndexError):
    print("❌ Error: Invalid response format:", response.json())
    exit(1)

# Print AI review
print("✅ AI Code Review Output:\n")
print(review_output)
