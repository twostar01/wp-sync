# wp-sync

A GitHub Action that publishes `PROJECT.md` and `BUILDLOG.md` from any repo to a WordPress page via the REST API. Commit your docs, push, and the page updates automatically — no manual editing needed.

Built for builders and tinkerers who want to share their process, not just the finished product.

## How it works

Each project repo has:
- `PROJECT.md` — project description and metadata (frontmatter)
- `BUILDLOG.md` — dated narrative entries, newest first
- `.github/workflows/publish.yml` — triggers on push to main when either file changes

When `PROJECT.md` or `BUILDLOG.md` are pushed, the action converts them to HTML and updates the corresponding WordPress page via the REST API.

## Install the setup skill (recommended)

The easiest way to wire up a new project is the `/wp-sync-init` Claude Code skill.

```powershell
# Windows — run once from this repo root
.\install.ps1
```

```bash
# Mac/Linux — run once from this repo root
bash install.sh
```

Then open any project in Claude Code and run:

```
/wp-sync-init
```

Claude will ask a few questions, create all the files, and walk you through the two manual steps (WordPress page + GitHub secrets).

## Manual setup

If you prefer to set things up yourself:

1. Copy `templates/publish.yml` to `.github/workflows/publish.yml` in your project repo
2. Add a `PROJECT.md` with at minimum:
   ```yaml
   ---
   title: My Project
   wp_page_id: 123
   ---
   ```
3. Add three repository secrets (Settings → Secrets → Actions):
   - `WP_URL` — your WordPress site URL
   - `WP_USER` — your WordPress username
   - `WP_APP_PASSWORD` — a WordPress Application Password (generate at WP Admin → Users → Profile → Application Passwords)
4. Push — the workflow fires automatically on the first push that includes `PROJECT.md`

## Build log workflow

After a working session, run the buildlog script from your project root:

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
