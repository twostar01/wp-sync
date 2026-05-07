# Install wp-sync-init skill to Claude Code
# Run once from the wp-sync repo root.
# After install, use /wp-sync-init in any project terminal.

$dest = "$env:USERPROFILE\.claude\commands"

if (-not (Test-Path $dest)) {
    New-Item -ItemType Directory -Path $dest | Out-Null
}

Copy-Item "$PSScriptRoot\skills\wp-sync-init.md" "$dest\wp-sync-init.md" -Force

Write-Host ""
Write-Host "Installed /wp-sync-init to Claude Code."
Write-Host "Open any project in Claude Code and run: /wp-sync-init"
Write-Host ""
