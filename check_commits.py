import os
import json
import requests
import sys

repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("INPUT_GITHUB_TOKEN")
event_path = os.getenv("GITHUB_EVENT_PATH")

# Load the event payload
with open(event_path, 'r') as f:
    event = json.load(f)

# Get commits from push or pull request
commits = []
if "commits" in event:
    commits = event["commits"]
elif "pull_request" in event:
    pr_commits_url = event["pull_request"]["commits_url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(pr_commits_url, headers=headers)
    if response.ok:
        commits = response.json()
    else:
        print("❌ Failed to fetch PR commits")
        sys.exit(1)

# Check each commit message
failed = False
for commit in commits:
    msg = commit["message"]
    print(f"➡️ Checking: {msg}")
    if not msg[0].isupper():
        print(f"❌ Commit message must start with a capital letter: {msg}")
        failed = True

if failed:
    sys.exit(1)
else:
    print("✅ All commit messages passed!")
