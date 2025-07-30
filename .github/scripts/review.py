import os

import requests
 
API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = "openchat/openchat-3.5-0106"  # You can choose other models
 
diff = os.popen('git diff origin/main...HEAD').read()
 
prompt = f"Review the following code diff and suggest improvements:\n\n{diff}"
 
headers = {

    "Authorization": f"Bearer {API_KEY}",

    "Content-Type": "application/json"

}
 
data = {

    "model": MODEL,

    "messages": [

        {"role": "user", "content": prompt}

    ]

}
 
response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
 
review_output = response.json()["choices"][0]["message"]["content"]
 
print("✅ AI Code Review Suggestion:\n")

print(review_output)

 