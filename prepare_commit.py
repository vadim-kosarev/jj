#!/usr/bin/env python3
"""
Script to prepare and analyze git changes for commit.
Gathers data, saves to tmp/ directory. Does NOT perform commit.

Execution flow:
1. Stage all changes (git add .)
2. Get git status and diff
3. Save all info to tmp/ for processing
"""

import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime


def ensure_tmp_dir() -> None:
    """Create tmp directory if it doesn't exist."""
    tmp_dir = Path("tmp")
    tmp_dir.mkdir(exist_ok=True)


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
    run_command("git add -A")


def get_git_status() -> str:
    """Get current git status."""
    return run_command("git status --porcelain")


def get_git_diff() -> str:
    """Get staged changes diff."""
    return run_command("git diff --cached")


def save_diff_to_file(diff_content: str) -> None:
    """Save diff content to tmp/changes.diff."""
    with open("tmp/changes.diff", "w") as f:
        f.write(diff_content)


def extract_changed_files(status: str) -> list:
    """Extract list of changed files from git status."""
    files = []
    for line in status.strip().split("\n"):
        if line:
            parts = line.split(maxsplit=1)
            if len(parts) > 1:
                status_code = parts[0]
                filename = parts[1]
                files.append((status_code, filename))
    return files


def save_preparation_data(status: str, diff: str) -> None:
    """Save preparation data to tmp/commit_prep_data.txt for AI processing."""
    data = f"""STATUS:
{status}

DIFF:
{diff}"""
    with open("tmp/commit_prep_data.txt", "w") as f:
        f.write(data)


def main() -> None:
    """Main execution flow."""
    try:
        # Create tmp directory
        ensure_tmp_dir()

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

        # Save preparation data
        save_preparation_data(status, diff)

        sys.exit(0)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

