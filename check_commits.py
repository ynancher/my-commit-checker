import os
import requests

# Get the token from environment
token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("GITHUB_TOKEN not found in environment variables")

# Get repo and PR info from environment
repo = os.getenv("GITHUB_REPOSITORY")  # e.g., "owner/repo"
pr_number = os.getenv("PR_NUMBER")     # You may need to pass this explicitly

# GitHub API URL to fetch commits from a PR
url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/commits"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"❌ Failed to fetch PR commits: {response.status_code} {response.text}")
    exit(1)

commits = response.json()
for commit in commits:
    print(f"✅ Commit: {commit['commit']['message']}")
