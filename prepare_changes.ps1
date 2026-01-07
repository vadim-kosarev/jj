# Script to prepare and show changes for commit

# Add all changes (including untracked)
git add -A

# Show status without pager
Write-Host "Git Status:"
git --no-pager status

# Show diff of staged changes without pager and save to file
git --no-pager diff --cached > changes.diff
Write-Host "`nStaged changes saved to changes.diff"

# Show summary
$lineCount = (Get-Content changes.diff | Measure-Object -Line).Lines
Write-Host "Changes.diff has $lineCount lines."
