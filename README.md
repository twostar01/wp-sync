# wp-sync

A GitHub Action that publishes `PROJECT.md` and `BUILDLOG.md` from any repo to a WordPress page via the REST API. Commit your docs, push, and the page updates automatically — no manual editing needed.

Built for builders and tinkerers who want to share their process, not just the finished product.

## How it works

Each project repo has:
- `PROJECT.md` — project description and metadata (frontmatter)
- `BUILDLOG.md` — dated narrative entries, newest first
- `.github/workflows/publish.yml` — triggers on push to main when either file changes

When `PROJECT.md` or `BUILDLOG.md` are pushed, the action converts them to HTML and updates the corresponding WordPress page via the REST API.

## Setup

### Step 1 — Install the skill (one time)

Clone this repo and run the install script to add the `/wp-sync-init` command to Claude Code:

```powershell
# Windows
git clone https://github.com/twostar01/wp-sync.git
cd wp-sync
.\install.ps1
```

```bash
# Mac/Linux
git clone https://github.com/twostar01/wp-sync.git
cd wp-sync
bash install.sh
```

### Step 2 — Initialize any project

Open the project in Claude Code and run:

```
/wp-sync-init
```

Claude will ask a few questions, create all the required files, and walk you through the two things that require browser access: creating the WordPress page and adding the GitHub secrets.

That's it — after secrets are set, every push that changes `PROJECT.md` or `BUILDLOG.md` publishes automatically.

## Build log workflow

After a working session, run from your project root:

```powershell
# Windows
.\scripts\buildlog.ps1
```

```bash
# Mac/Linux
bash scripts/buildlog.sh
```

This starts a Claude session with your recent git context. Claude asks what decisions were made and why, then drafts a dated `BUILDLOG.md` entry. Commit it and the page updates on push.

## PROJECT.md frontmatter fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | yes | Page title on WordPress |
| `wp_page_id` | yes | WordPress page ID |
| `status` | no | Shown on the page (e.g. `working`, `in-progress`) |
| `type` | no | Project type (e.g. `software`, `hardware`) |
| `github_url` | no | Adds a "View on GitHub" link |
