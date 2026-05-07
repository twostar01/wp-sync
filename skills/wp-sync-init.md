---
name: wp-sync-init
description: Use when setting up WordPress documentation publishing in a new project repo
---

# WP Sync Init

Sets up [wp-sync](https://github.com/twostar01/wp-sync) in the current project: creates the publish workflow, PROJECT.md, BUILDLOG.md, and buildlog scripts. Then walks through what needs to be done manually.

## Step 1 — Gather project info

Use AskUserQuestion to collect what's needed. Infer what you can first:
- **Project title** — suggest from directory name, let user confirm or change
- **WordPress page ID** — required; if they don't have one yet, tell them: WP Admin → Pages → Add New → Publish → note the ID from the URL (`?post=123`)
- **GitHub URL** — run `git remote get-url origin`, confirm with user
- **Project type** — software / hardware / radio / other
- **Project status** — in-progress / working / planning

## Step 2 — Create files

Skip any file that already exists — ask before overwriting.

### `.github/workflows/publish.yml`

```yaml
name: Publish to Website

"on":
  push:
    branches: [main]
    paths:
      - PROJECT.md
      - BUILDLOG.md
  workflow_dispatch:
    inputs:
      note:
        description: 'What changed this publish (optional)'
        required: false
        type: string

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Log publish note
        if: ${{ inputs.note != '' }}
        run: echo "Publishing note -- ${{ inputs.note }}"

      - uses: twostar01/wp-sync@main
        with:
          wp_url: ${{ secrets.WP_URL }}
          wp_user: ${{ secrets.WP_USER }}
          wp_app_password: ${{ secrets.WP_APP_PASSWORD }}
```

### `PROJECT.md`

Replace `{placeholders}` with gathered values:

```
---
title: {title}
type: {type}
status: {status}
wp_page_id: {page_id}
github_url: {github_url}
---

## What It Does

[Describe what this project does]

## How It Works

[Describe the approach]
```

### `BUILDLOG.md`

Use today's actual date:

```
## YYYY-MM-DD — Project initialized

[First build log entry — describe what this project is and why you're building it.]
```

### `scripts/buildlog.sh`

```bash
#!/usr/bin/env bash
# buildlog — start a Claude session to discuss and draft a BUILDLOG.md entry
# Run from project root after a working session.

set -e

if [ ! -d ".git" ]; then
    echo "Error: not a git repository. Run this from a project root."
    exit 1
fi

PROJECT=$(basename "$(git rev-parse --show-toplevel)")
DATE=$(date +%Y-%m-%d)

LAST_BUILDLOG_COMMIT=$(git log --oneline --follow -- BUILDLOG.md 2>/dev/null | head -1 | cut -d' ' -f1)

if [ -n "$LAST_BUILDLOG_COMMIT" ]; then
    COMMITS=$(git log --oneline "${LAST_BUILDLOG_COMMIT}..HEAD" -- . ':(exclude)BUILDLOG.md' 2>/dev/null)
    STAT=$(git diff --stat "${LAST_BUILDLOG_COMMIT}..HEAD" -- . ':(exclude)BUILDLOG.md' 2>/dev/null)
else
    COMMITS=$(git log --oneline -15 2>/dev/null)
    STAT=$(git diff --stat HEAD~5..HEAD -- . ':(exclude)BUILDLOG.md' 2>/dev/null)
fi

if [ -z "$COMMITS" ]; then
    echo "No new commits since last buildlog entry. Nothing to document yet."
    exit 0
fi

PROMPT="I'm working on the '$PROJECT' project and want to add an entry to BUILDLOG.md.

Date: $DATE

Commits since last entry:
${COMMITS}

Files changed:
${STAT}

Ask me a few focused questions to understand the key decisions, what I tried, and what someone building a similar project should know. Then draft a BUILDLOG.md entry in this format:

## ${DATE} — [brief title]

[One or more narrative paragraphs — conversational, practical, written for a builder trying to replicate or learn from this project. Capture the why behind decisions, not just what changed.]

Keep it readable, not a changelog. Aim for the style of a builder's project log — what worked, what didn't, and why you made the calls you did."

claude "$PROMPT"
```

### `scripts/buildlog.ps1`

```powershell
# buildlog — start a Claude session to discuss and draft a BUILDLOG.md entry
# Run from project root after a working session.

if (-not (Test-Path ".git")) {
    Write-Error "Not a git repository. Run this from a project root."
    exit 1
}

$project = Split-Path -Leaf (git rev-parse --show-toplevel)
$date = Get-Date -Format "yyyy-MM-dd"

$lastBuildlogLine = git log --oneline --follow -- BUILDLOG.md 2>$null | Select-Object -First 1
$lastBuildlogCommit = if ($lastBuildlogLine) { ($lastBuildlogLine -split ' ')[0] } else { $null }

if ($lastBuildlogCommit) {
    $commits = git log --oneline "${lastBuildlogCommit}..HEAD" -- . ':(exclude)BUILDLOG.md' 2>$null
    $stat    = git diff --stat "${lastBuildlogCommit}..HEAD" -- . ':(exclude)BUILDLOG.md' 2>$null
} else {
    $commits = git log --oneline -15 2>$null
    $stat    = git diff --stat HEAD~5..HEAD -- . ':(exclude)BUILDLOG.md' 2>$null
}

if (-not $commits) {
    Write-Host "No new commits since last buildlog entry. Nothing to document yet."
    exit 0
}

$prompt = @"
I'm working on the '$project' project and want to add an entry to BUILDLOG.md.

Date: $date

Commits since last entry:
$commits

Files changed:
$stat

Ask me a few focused questions to understand the key decisions, what I tried, and what someone building a similar project should know. Then draft a BUILDLOG.md entry in this format:

## $date --- [brief title]

[One or more narrative paragraphs -- conversational, practical, written for a builder trying to replicate or learn from this project. Capture the why behind decisions, not just what changed.]

Keep it readable, not a changelog. Aim for the style of a builder's project log -- what worked, what didn't, and why you made the calls you did.
"@

$tmp = [System.IO.Path]::GetTempFileName() + ".txt"
$prompt | Out-File -FilePath $tmp -Encoding utf8
try {
    Get-Content $tmp | claude
} finally {
    Remove-Item $tmp -ErrorAction SilentlyContinue
}
```

## Step 3 — Make scripts executable

Run: `git update-index --chmod=+x scripts/buildlog.sh`

## Step 4 — Walk the user through manual steps

Tell the user clearly:

**You need to add three secrets to this GitHub repo before the first publish will work.**

Go to: **GitHub repo → Settings → Secrets and variables → Actions → New repository secret**

Add these three:
| Secret | Value |
|--------|-------|
| `WP_URL` | Your WordPress site URL, e.g. `https://yoursite.com` |
| `WP_USER` | Your WordPress username |
| `WP_APP_PASSWORD` | A WordPress Application Password — generate one at WP Admin → Users → Your Profile → Application Passwords |

**Once secrets are set:** push to main and the workflow fires automatically whenever `PROJECT.md` or `BUILDLOG.md` change.

## Step 5 — Commit everything

Stage all created files and commit with message: `Initialize wp-sync documentation publishing`

Suggest the user push once secrets are added.
