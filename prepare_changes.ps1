# Script to prepare and show changes for commit

# Disable pager for git commands
$env:GIT_PAGER = 'cat'

# Add all changes (including untracked)
git add -A

# Show status
Write-Host "Git Status:"
git status

# Show diff of staged changes and save to file
git diff --cached > changes.diff
Write-Host "`nStaged changes saved to changes.diff"

# Show summary
$lineCount = (Get-Content changes.diff | Measure-Object -Line).Lines
Write-Host "Changes.diff has $lineCount lines."
