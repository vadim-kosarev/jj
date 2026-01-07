# Script to prepare and show changes for commit

# Add all changes (already done, but for completeness)
git add .

# Show status
Write-Host "Git Status:"
git status

# Show diff of staged changes
Write-Host "`nStaged Changes Diff:"
git diff --cached

# Optionally save to file
git diff --cached > changes.diff
Write-Host "`nChanges saved to changes.diff"
