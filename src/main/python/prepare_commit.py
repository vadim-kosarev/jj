#!/usr/bin/env python3
"""
Script to prepare git commit by analyzing changes and generating commit message.
Execution flow:
1. Stage all changes (git add .)
2. Get git status and diff
3. Generate commit message based on changes
4. Perform commit with generated message
"""

import subprocess
import os
import sys
from pathlib import Path
from typing import Optional


def run_command(cmd: str, shell: bool = False) -> str:
    """Execute shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error executing command: {str(e)}"


def stage_changes() -> None:
    """Stage all changes for commit."""
    print("Staging all changes...")
    run_command("git add -A")
    print("[+] All changes staged")


def get_git_status() -> str:
    """Get current git status."""
    return run_command("git status --porcelain")


def get_git_diff() -> str:
    """Get staged changes diff."""
    return run_command("git diff --cached")


def save_diff_to_file(diff_content: str, output_file: str = "changes.diff") -> None:
    """Save diff content to file."""
    with open(output_file, "w") as f:
        f.write(diff_content)
    line_count = len(diff_content.splitlines())
    print(f"[+] Staged changes saved to {output_file} ({line_count} lines)")


def extract_changed_files(status: str) -> list[str]:
    """Extract list of changed files from git status."""
    files = []
    for line in status.strip().split("\n"):
        if line:
            # Format: "M  src/file.py" or "A  src/file.py"
            parts = line.split(maxsplit=1)
            if len(parts) > 1:
                files.append(parts[1])
    return files


def generate_commit_message(status: str, diff: str) -> str:
    """
    Generate commit message based on changes.
    Analyzes file changes and creates concise message (max 5 lines).
    """
    files = extract_changed_files(status)

    if not files:
        return "Minor updates"

    # Categorize changes
    categories = {
        "config": [],
        "schema": [],
        "code": [],
        "doc": [],
        "other": []
    }

    for file in files:
        if any(x in file.lower() for x in ["config", "docker", "yml", "yaml"]):
            categories["config"].append(file)
        elif any(x in file.lower() for x in ["schema", "sql"]):
            categories["schema"].append(file)
        elif any(x in file.lower() for x in [".java", ".py", ".kt"]):
            categories["code"].append(file)
        elif any(x in file.lower() for x in [".md", ".txt"]):
            categories["doc"].append(file)
        else:
            categories["other"].append(file)

    # Build message
    lines = []

    if categories["schema"]:
        lines.append(f"Update ClickHouse schema: {', '.join([Path(f).name for f in categories['schema']])}")
    if categories["code"]:
        lines.append(f"Refactor core logic: {len(categories['code'])} file(s)")
    if categories["config"]:
        lines.append(f"Update configuration: {', '.join([Path(f).name for f in categories['config']])}")
    if categories["doc"]:
        lines.append(f"Update documentation")
    if categories["other"]:
        lines.append(f"Minor updates: {len(files)} file(s)")

    # Combine and truncate to 5 lines max
    message = "\n".join(lines[:5])
    return message if message else "Update files"


def save_commit_info(status: str, diff: str, message: str) -> None:
    """Save commit information for reference."""
    info = f"""=== COMMIT INFO ===
Generated: {subprocess.run('date', shell=True, capture_output=True, text=True).stdout.strip()}

=== COMMIT MESSAGE ===
{message}

=== FILES CHANGED ===
{status}

=== DIFF SUMMARY ===
Lines changed: {len(diff.splitlines())}
"""
    with open("commit_info.txt", "w") as f:
        f.write(info)
    print("[+] Commit info saved to commit_info.txt")


def perform_commit(message: str) -> bool:
    """Perform git commit with generated message."""
    print(f"\n=== COMMIT MESSAGE ===\n{message}\n")

    cmd = f'git commit -m "{message}"'
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("[+] Commit created successfully")
        print(result.stdout)
        return True
    else:
        print("[-] Commit failed")
        print(result.stderr)
        return False


def main() -> None:
    """Main execution flow."""
    try:
        # Stage all changes
        stage_changes()

        # Get status and diff
        status = get_git_status()
        diff = get_git_diff()

        if not status.strip():
            print("No changes to commit")
            sys.exit(0)

        # Save diff
        save_diff_to_file(diff)

        # Generate message
        message = generate_commit_message(status, diff)

        # Save commit info
        save_commit_info(status, diff, message)

        # Perform commit
        if perform_commit(message):
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

