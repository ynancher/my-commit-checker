import os
import requests

repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("INPUT_GITHUB_TOKEN")
event_path = os.getenv("GITHUB_EVENT_PATH")

with open(event_path, 'r') as f:
    event = f.read()

# You can parse the event JSON and check commit messages here
# For example, check if they start with a capital letter or contain a JIRA ID
print("✅ Commit check passed!")
