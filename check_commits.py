import os
import requests
import sys

token = os.getenv("INPUT_GITHUB_TOKEN")
repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("PR_NUMBER")

# Validate environment variables
if not token:
    raise ValueError("INPUT_GITHUB_TOKEN not found in environment variables")
if not repo:
    raise ValueError("GITHUB_REPOSITORY not found in environment variables")
if not pr_number:
    raise ValueError("PR_NUMBER not found in environment variables")

# GitHub API URL to fetch commits from the pull request
url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/commits"

# Set headers for authentication
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Make the API request
response = requests.get(url, headers=headers)


# Check for successful response
if response.status_code != 200:
    print(f"❌ Failed to fetch PR commits: {response.status_code} {response.text}")
    sys.exit(1)

# # Parse the commits
commits = response.json()


def is_valid_commit_message(message):
    return len(message) >= 10 and message[0].isupper() and len(message) <= 72


# Track validation results
invalid_commits = []

# Validate each commit message
for commit in commits:
    message = commit['commit']['message']
    sha = commit['sha']
    try:
        description = message.splitlines()[2]
        print("This is desc --> %s", description)
    except Exception as e:
        print("Commit Message has no description! :%s", e)
        invalid_commits.append((sha, message))
        break
    if is_valid_commit_message(description):
        print(f"✅ Valid commit ({sha}): {message}")
    else:
        print(f"❌ Invalid commit ({sha}): {message}")
        invalid_commits.append((sha, message))

# Exit with code 1 if any commit is invalid
if invalid_commits:
    sys.exit(1)
else:
    sys.exit(0)
