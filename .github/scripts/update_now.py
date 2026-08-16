#!/usr/bin/env python3
"""Refresh the "Recently Pushed" block in README.md and README.ru.md.

The block is delimited by ``<!-- NOW:START -->`` / ``<!-- NOW:END -->`` markers.
Run with ``--selftest`` to check the rendering and replacement logic offline.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

USER = "Fgeeha"
LIMIT = 5
SKIP = {USER}  # the profile repository itself
ROOT = Path(__file__).resolve().parents[2]

START = "<!-- NOW:START -->"
END = "<!-- NOW:END -->"

HEADERS = {
    "README.md": ("Repository", "Description", "Updated"),
    "README.ru.md": ("Репозиторий", "Описание", "Обновлён"),
}


def fetch_repos() -> list[dict[str, Any]]:
    """Return the most recently pushed own repositories, newest first."""
    url = f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=100&type=owner"
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def render(repos: list[dict[str, Any]], header: tuple[str, str, str]) -> str:
    """Render repositories as a Markdown table."""
    picked = [
        repo
        for repo in repos
        if not repo["fork"] and not repo["archived"] and repo["name"] not in SKIP
    ][:LIMIT]
    lines = [f"| {header[0]} | {header[1]} | {header[2]} |", "| --- | --- | --- |"]
    for repo in picked:
        description = (repo.get("description") or "—").replace("|", "\\|")
        lines.append(
            f"| [{repo['name']}]({repo['html_url']}) | {description} | {repo['pushed_at'][:10]} |"
        )
    return "\n".join(lines)


def replace_block(text: str, body: str) -> str:
    """Replace everything between the NOW markers with ``body``."""
    if START not in text or END not in text:
        raise ValueError("NOW markers not found")
    pattern = re.compile(re.escape(START) + ".*?" + re.escape(END), re.DOTALL)
    return pattern.sub(lambda _: f"{START}\n{body}\n{END}", text, count=1)


def main() -> None:
    repos = fetch_repos()
    for name, header in HEADERS.items():
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        updated = replace_block(text, render(repos, header))
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def selftest() -> None:
    repos = [
        {
            "name": "Fgeeha",
            "fork": False,
            "archived": False,
            "description": "profile",
            "html_url": "u",
            "pushed_at": "2026-08-16T00:00:00Z",
        },
        {
            "name": "forked",
            "fork": True,
            "archived": False,
            "description": "x",
            "html_url": "u",
            "pushed_at": "2026-08-16T00:00:00Z",
        },
        {
            "name": "kept",
            "fork": False,
            "archived": False,
            "description": "a | b",
            "html_url": "https://example.com/kept",
            "pushed_at": "2026-08-15T10:00:00Z",
        },
        {
            "name": "empty-desc",
            "fork": False,
            "archived": False,
            "description": None,
            "html_url": "https://example.com/empty",
            "pushed_at": "2026-08-14T10:00:00Z",
        },
    ]
    table = render(repos, HEADERS["README.md"])
    assert "Fgeeha" not in table, "profile repo must be skipped"
    assert "forked" not in table, "forks must be skipped"
    assert "[kept](https://example.com/kept)" in table
    assert "a \\| b" in table, "pipes must be escaped"
    assert "| — |" in table, "missing description falls back to a dash"
    assert "| 2026-08-15 |" in table

    text = f"before\n{START}\nold | junk\n{END}\nafter"
    out = replace_block(text, "NEW")
    assert out == f"before\n{START}\nNEW\n{END}\nafter", out
    assert replace_block(out, "NEW") == out, "replacement must be idempotent"

    try:
        replace_block("no markers here", "NEW")
    except ValueError:
        pass
    else:
        raise AssertionError("missing markers must raise")

    print("selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()
