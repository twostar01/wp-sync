#!/usr/bin/env python3
"""Sync PROJECT.md and BUILDLOG.md to a WordPress page via REST API."""

import base64
import os
import sys

import frontmatter
import markdown
import requests


def load_project():
    if not os.path.exists("PROJECT.md"):
        print("ERROR: PROJECT.md not found in repo root.")
        sys.exit(1)

    with open("PROJECT.md", "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    if not post.get("title"):
        print("ERROR: PROJECT.md is missing required field: title")
        sys.exit(1)

    if not post.get("wp_page_id"):
        print("ERROR: PROJECT.md is missing wp_page_id.")
        print("  Add wp_page_id to PROJECT.md frontmatter.")
        print("  Find the page ID in WordPress Admin > Pages (hover over the page title to see the ID in the URL).")
        sys.exit(1)

    return post


def load_buildlog():
    if not os.path.exists("BUILDLOG.md"):
        return ""
    with open("BUILDLOG.md", "r", encoding="utf-8") as f:
        return f.read()


def to_html(text):
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "nl2br"],
    )


def build_content(project, buildlog_md):
    status = project.get("status", "in-progress")
    github_url = project.get("github_url", "")
    project_type = project.get("type", "")

    parts = []

    # Status bar
    github_link = f' &nbsp;·&nbsp; <a href="{github_url}">View on GitHub →</a>' if github_url else ""
    type_label = f" &nbsp;·&nbsp; {project_type}" if project_type else ""
    parts.append(
        f'<p><strong>Status:</strong> {status}{type_label}{github_link}</p>'
    )

    # Main project content
    body = project.content.strip()
    if body:
        parts.append(to_html(body))

    # Build log
    if buildlog_md.strip():
        parts.append("<hr>")
        parts.append(to_html(buildlog_md))

    return "\n\n".join(parts)


def update_wordpress(page_id, title, content, wp_url, wp_user, wp_password):
    endpoint = f"{wp_url.rstrip('/')}/wp-json/wp/v2/pages/{page_id}"

    credentials = base64.b64encode(f"{wp_user}:{wp_password}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json",
    }

    payload = {
        "title": title,
        "content": content,
        "status": "publish",
    }

    response = requests.put(endpoint, headers=headers, json=payload, timeout=30)

    if response.status_code in (200, 201):
        data = response.json()
        print(f"Published: {data.get('link', endpoint)}")
    else:
        print(f"ERROR: WordPress API returned {response.status_code}")
        print(response.text[:500])
        sys.exit(1)


def main():
    wp_url = os.environ.get("WP_URL", "")
    wp_user = os.environ.get("WP_USER", "")
    wp_password = os.environ.get("WP_APP_PASSWORD", "")

    if not all([wp_url, wp_user, wp_password]):
        missing = [k for k, v in {"WP_URL": wp_url, "WP_USER": wp_user, "WP_APP_PASSWORD": wp_password}.items() if not v]
        print(f"ERROR: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)

    project = load_project()
    buildlog = load_buildlog()

    page_id = project["wp_page_id"]
    title = project["title"]
    content = build_content(project, buildlog)

    print(f"Syncing '{title}' to WordPress page {page_id}...")
    update_wordpress(page_id, title, content, wp_url, wp_user, wp_password)


if __name__ == "__main__":
    main()
