import os
import subprocess
import requests
from crewai.tools import tool  # ✅ decorator-based import

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Format: username/repo

@tool  # ✅ this turns your function into a Tool object
def git_commit_and_pr(commit_message="Auto-commit from AI agent") -> str:
    """
    Commits all changes to the GitHub repo and creates a pull request to the main branch.
    """
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

        # Create Pull Request
        url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        data = {
            "title": commit_message,
            "head": "main",
            "base": "main",
            "body": "This PR was created by an autonomous AI agent."
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code in [200, 201]:
            return f"✅ Code committed and PR created: {response.json().get('html_url')}"
        else:
            return f"❌ Commit done, but PR failed: {response.text}"

    except subprocess.CalledProcessError as e:
        return f"❌ Git command failed: {e}"
