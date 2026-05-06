## 2026-05-06 — Building the documentation loop

The whole point of wp-sync is reducing the friction between building something and writing about it. I got tired of projects sitting undocumented because writing up what I did felt like a second job after the actual work. This repo is the first piece of that — a GitHub Action that reads `PROJECT.md` and `BUILDLOG.md` from any project and pushes them to the corresponding WordPress page automatically.

The design is intentionally minimal: one Python script (`sync.py`), one action definition (`action.yml`), one workflow template (`templates/publish.yml`). Consumer repos just copy the template, add three secrets (WP_URL, WP_USER, WP_APP_PASSWORD), and they get a "Publish to Website" button in GitHub Actions. No packages to install, no config files to maintain.

The trickier question was how to actually capture build notes without it becoming overhead. The answer we landed on: a `buildlog` script (in `scripts/`) that pulls recent git context and starts an interactive Claude session to discuss what was decided and why. Claude asks a few questions, you answer in plain English, and it drafts the entry in the right format. Then you commit BUILDLOG.md alongside your code. The script detects the last BUILDLOG.md commit and only shows you commits since then, so it always picks up where you left off.

Format for entries is intentionally narrative — what you tried, what the tradeoffs were, what someone replicating the project should know. Not a changelog. The audience is another ham who wants to build something similar and is trying to understand the reasoning, not just the end state.

Next up: test the full loop end-to-end (commit → buildlog session → publish to WordPress), then wire up a project or two as real consumers.
