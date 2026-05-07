---
title: WP Sync
type: software
status: working
wp_page_id: 219
wp_slug: wp-sync
github_url: https://github.com/twostar01/wp-sync
tags: [wordpress, automation, github-actions, python]
---

## What It Does

Reusable GitHub Action that syncs a project's `PROJECT.md` and `BUILDLOG.md` to a WordPress page via the REST API. Drop it into any project repo and get a one-click publish button in GitHub Actions — no manual website editing needed.

Designed to keep project documentation on [mygeekywebsite.com](https://www.mygeekywebsite.com) up to date as projects evolve, with a narrative build log that captures discoveries and gotchas alongside the technical details — useful for any builder or tinkerer who wants to share their process, not just the finished product.

## How It Works

Each project repo contains:
- `PROJECT.md` — project metadata (frontmatter) and content in Markdown
- `BUILDLOG.md` — dated build log entries, newest first
- `.github/workflows/publish.yml` — calls this action on manual trigger

When you click **Run workflow** in GitHub Actions, `sync.py` reads both files, converts them to HTML, and updates the corresponding WordPress page via the REST API using an Application Password.

## Setup

**In the shared `wp-sync` repo** — already done, nothing to configure.

**In each project repo:**

1. Copy `templates/publish.yml` to `.github/workflows/publish.yml`
2. Add three repository secrets: `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`
3. Add `PROJECT.md` with `wp_page_id` set to the WordPress page ID
4. Go to Actions → Publish to Website → Run workflow

## Build Log
