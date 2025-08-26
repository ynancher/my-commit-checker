import os
import requests
import sys
import re

# Environment variables
token = os.getenv("INPUT_GITHUB_TOKEN")
repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("PR_NUMBER")

# Input flags
check_message = os.getenv("INPUT_MESSAGE", "true") == "true"
check_branch = os.getenv("INPUT_BRANCH", "true") == "true"
check_author_name = os.getenv("INPUT_AUTHOR_NAME", "true") == "true"
check_author_email = os.getenv("INPUT_AUTHOR_EMAIL", "true") == "true"
check_signoff = os.getenv("INPUT_COMMIT_SIGNOFF", "true") == "true"
check_merge_base = os.getenv("INPUT_MERGE_BASE", "true") == "true"
check_imperative = os.getenv("INPUT_IMPERATIVE", "true") == "true"
char_limit = int(os.getenv("INPUT_CHAR_LIMIT", "72"))

# Validate required env vars
if not token or not repo or not pr_number:
    print("❌ Missing required environment variables.")
    sys.exit(1)

# GitHub API URL to fetch commits from the pull request
url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/commits"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"❌ Failed to fetch PR commits: {response.status_code} {response.text}")
    sys.exit(1)

commits = response.json()
invalid_commits = []

def is_imperative(text):
    # Naive check: first word is a verb in base form (e.g., "Fix", "Add", "Update")
    return bool(re.match(r"^[A-Z][a-z]+", text.strip()))

for commit in commits:
    sha = commit['sha']
    message = commit['commit']['message']
    author = commit['commit']['author']
    lines = message.splitlines()
    subject = lines[2] if lines else ""
    description = lines[4] if len(lines) > 2 else ""

    errors = []

    if check_message:
        if len(subject) > char_limit:
            errors.append(f"Subject exceeds {char_limit} characters.")
        if len(description) > char_limit:
            errors.append(f"Description exceeds {char_limit} characters.")

    if check_author_name and not author.get("name"):
        errors.append("Missing author name.")

    if check_author_email and not author.get("email"):
        errors.append("Missing author email.")

    if check_signoff and "Signed-off-by:" not in message:
        errors.append("Missing 'Signed-off-by' line.")

    if check_imperative and not is_imperative(subject):
        errors.append("Subject line is not in imperative mood.")

    if errors:
        print(f"\n❌ Commit {sha} failed checks:")
        for err in errors:
            print(f"   - {err}")
        invalid_commits.append((sha, errors))
    else:
        print(f"✅ Commit {sha} passed all checks.")

# Final result
if invalid_commits:
    print(f"\n❌ {len(invalid_commits)} commit(s) failed validation.")
    sys.exit(1)
else:
    print("\n✅ All commits passed validation.")
    sys.exit(0)
