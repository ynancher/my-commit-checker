import os
import json
import requests
import sys

repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("INPUT_GITHUB_TOKEN")
event_path = os.getenv("GITHUB_EVENT_PATH")

with open(event_path, 'r') as f:
    event = json.load(f)

commits = []

if "commits" in event:
    # Push event
    commits = event["commits"]
elif "pull_request" in event:
    # PR event
    pr_commits_url = event["pull_request"]["commits_url"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(pr_commits_url, headers=headers)
    if response.ok:
        commits = response.json()
    else:
        print(f"❌ Failed to fetch PR commits: {response.status_code} {response.text}")
        sys.exit(1)
else:
    print("❌ Unsupported event type")
    sys.exit(1)

# Now check commit messages
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
