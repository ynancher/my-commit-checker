import os
import subprocess

# Define the mapping of environment variables to CLI flags
flag_map = {
    "MESSAGE": "--message",
    "BRANCH": "--branch",
    "AUTHOR_NAME": "--author-name",
    "AUTHOR_EMAIL": "--author-email",
    "COMMIT_SIGNOFF": "--commit-signoff"
}

# Build the list of arguments based on which flags are enabled
args = []
for env_var, flag in flag_map.items():
    if os.getenv(env_var, "false").lower() == "true":
        args.append(flag)

# Construct the full command
command = ["commit-check"] + args
print("Running command:", " ".join(command))

# Run the command and capture output
try:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    with open("result.txt", "w") as f:
        f.write(result.stdout)
    print("✅ Commit check passed.")
except subprocess.CalledProcessError as e:
    print("❌ Commit check failed.")
    print(e.stderr)
    exit(1)
