import os

import subprocess

import requests
 
# Get the OpenRouter API key from environment variables

api_key = os.getenv("OPENROUTER_API_KEY")
 
# Git diff to show what changed in the pull request

diff_command = ["git", "diff", "origin/main...HEAD"]

diff_output = subprocess.check_output(diff_command).decode("utf-8")
 
# Prepare prompt for the AI

prompt = f"""

You are an expert code reviewer. Review the following code changes and provide:

1. Summary

2. Suggestions

3. Issues

4. Improvements
 
Code diff:

{diff_output}

"""
 
# API URL for OpenRouter

url = "https://openrouter.ai/api/v1/chat/completions"
 
# Send the prompt to OpenRouter

response = requests.post(

    url,

    headers={

        "Authorization": f"Bearer {api_key}",

        "Content-Type": "application/json",

        "HTTP-Referer": "https://github.com/Vignesh-S-24/Ai",  # Change to your repo URL

    },

    json={

        "model": "mistralai/mixtral-8x7b",  # Free and fast model on OpenRouter

        "messages": [

            {"role": "system", "content": "You are a senior code reviewer."},

            {"role": "user", "content": prompt},

        ]

    }

)
 
# Handle response

if response.status_code != 200:

    print("❌ API Error:", response.status_code, response.text)

    exit(1)
 
try:

    review_output = response.json()["choices"][0]["message"]["content"]

except KeyError:

    print("❌ Error: Invalid response format:", response.json())

    exit(1)
 
print("✅ AI Code Review Output:\n")

print(review_output)

 