import os
import json
import requests
from google import genai
from google.genai import types

repo = os.getenv("GITHUB_REPOSITORY")
issue_number = os.getenv("ISSUE_NUMBER")
issue_title = os.getenv("ISSUE_TITLE")
issue_body = os.getenv("ISSUE_BODY", "")
github_token = os.getenv("GITHUB_TOKEN")
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are an expert open-source repository maintainer. 
Analyze the following GitHub issue.
1. Determine the appropriate labels (e.g., 'bug', 'enhancement', 'question', 'needs-repro', 'documentation').
2. Write a polite, helpful comment. If it's a bug missing steps to reproduce or logs, ask for them. If it looks like a bug, briefly guess which part of the codebase might be responsible.
"""

user_prompt = f"Title: {issue_title}\n\nBody: {issue_body}"

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=user_prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json",
        response_schema={
            "type": "OBJECT",
            "properties": {
                "labels": {"type": "ARRAY", "items": {"type": "STRING"}},
                "comment": {"type": "STRING"}
            },
            "required": ["labels", "comment"]
        }
    )
)

ai_decision = json.loads(response.text)
headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

# Post Comment
requests.post(f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments", headers=headers, json={"body": ai_decision["comment"]})

# Post Labels
requests.post(f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels", headers=headers, json={"labels": ai_decision["labels"]})

print(f"Successfully processed issue #{issue_number}")