#!/usr/bin/env bash
# Install wp-sync-init skill to Claude Code
# Run once from the wp-sync repo root.
# After install, use /wp-sync-init in any project terminal.

DEST="$HOME/.claude/commands"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$DEST"
cp "$SCRIPT_DIR/skills/wp-sync-init.md" "$DEST/wp-sync-init.md"

echo ""
echo "Installed /wp-sync-init to Claude Code."
echo "Open any project in Claude Code and run: /wp-sync-init"
echo ""
