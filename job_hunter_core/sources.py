"""Source collection helpers and browser-assisted safety guidance."""

from __future__ import annotations

from pathlib import Path


BROWSER_ASSISTED_GUIDE = """# Browser-Assisted Job Collection Guide

This project can support browser-assisted job collection, but it should stay
user-controlled and compliance-friendly.

## Safe Workflow

1. The user opens LinkedIn, BOSS, a company career site, or another job board.
2. The user searches with relevant keywords and location/remote filters.
3. The agent or script reads only visible page content that the user has opened.
4. The user confirms selected jobs before saving them into `inbox/`.
5. The CLI imports, scores, and exports a shortlist.

## Guardrails

- Do not store passwords, cookies, sessions, or browser profiles.
- Do not bypass captchas or access controls.
- Do not auto-apply or send messages.
- Do not run high-volume scraping.
- Respect platform terms and stop if the site blocks automation.

## Suggested Search Queries

- finance AI product manager accounting automation
- accounting automation product manager remote
- finance FDE AI workflow internal deployment
- FP&A automation AI agent product
- finance systems AI analyst Power BI SQL

## Inbox Template

```markdown
---
title: Role title
company: Company name
location: Remote / City
url: https://example.com/job
source: browser-assisted
---

Paste visible JD text here.
```
"""


def write_browser_assisted_guide(output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(BROWSER_ASSISTED_GUIDE, encoding="utf-8")
    return path
