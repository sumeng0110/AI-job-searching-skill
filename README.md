# AI Job Search Skill Kit

An agent-friendly job-search toolkit for finance, accounting automation, AI
product, finance systems, BI, and FDE-style internal deployment roles.

The project is intentionally semi-automated by default. It helps parse a resume,
collect JDs, score role fit, generate outreach copy, and export a shortlist. It
does not save credentials or auto-submit applications.

## What It Does

- Parses a `.md` or `.txt` resume into a structured job-search profile.
- Imports copied JDs from `inbox/` or direct CLI input.
- Scores each job against configurable tracks:
  - Finance AI / FDE
  - AI Product
  - Data / BI
- Flags risk signals such as hard engineering requirements, pure sales/BD
  direction, seniority gaps, or possible local authorization constraints.
- Exports a Markdown or CSV shortlist grouped into:
  - `优先投`
  - `可冲`
  - `不建议`
- Includes a Cursor Agent Skill at `.cursor/skills/finance-job-hunter/` so other
  agents can call the workflow.

## Why Not Fully Auto-Apply

LinkedIn, BOSS, and many career sites may restrict automated login, scraping, or
bulk applications. This project keeps the high-value automation and leaves final
submission under user control:

- No stored passwords or cookies.
- No captcha bypass.
- No auto-apply.
- No high-volume scraping.
- Browser-assisted collection is optional and user-controlled.

## Project Structure

```text
job_hunter/
  job_hunter.py                         # CLI entry point
  profile_config.json                   # Matching rules and resume positioning
  job_hunter_core/                      # Reusable parser, matcher, reports, sources
  .cursor/skills/finance-job-hunter/    # Agent skill instructions
  examples/                             # Public-safe sample resume, JD, report
  inbox/                                # Local JD input, ignored by git
  exports/                              # Local reports, ignored by git
  profiles/                             # Generated resume profile, ignored by git
  sources/                              # Browser-assisted guide/cache, ignored by git
```

## Quick Start

Run commands from this directory:

```powershell
python job_hunter.py init
python job_hunter.py profile --resume examples\sample_resume.md
python job_hunter.py add --title "Finance AI Product Manager" --company "Example FinTech" --location "Remote" --url "https://example.com/jobs/finance-ai-product-manager" --jd-file examples\sample_job.md
python job_hunter.py list
python job_hunter.py export --format md
```

## Resume Profile

First version supports `.md` and `.txt` resumes:

```powershell
python job_hunter.py profile --resume examples\sample_resume.md
```

Default output:

```text
profiles/resume_profile.json
```

The generated profile includes target roles, keyword hits, resume positioning,
and suggested search terms.

## Import Jobs

### Add One Job

```powershell
python job_hunter.py add `
  --title "财务AI产品经理" `
  --company "某某科技" `
  --location "上海" `
  --url "https://example.com/job/123" `
  --jd-file "inbox\example_job.md"
```

### Import From Inbox

Save copied JDs as `.md` or `.txt` files in `inbox/`:

```markdown
---
title: 财务FDE（内部部署工程师）
company: 某某科技
location: 上海
url: https://example.com/jobs/finance-fde
source: company-site
---

这里粘贴完整 JD。
```

Then run:

```powershell
python job_hunter.py import-dir
```

## Browser-Assisted Mode

Generate the safety guide:

```powershell
python job_hunter.py browser-guide
```

This writes:

```text
sources/browser_assisted_guide.md
```

Use this mode when a user wants optional assistance collecting visible jobs from
LinkedIn, BOSS, or company career pages. Keep it user-controlled and do not
auto-apply.

## Export Reports

```powershell
python job_hunter.py export --format md
python job_hunter.py export --format csv
```

Markdown output is grouped as:

- `优先投`: strong match.
- `可冲`: relevant but has location, seniority, domain, or authorization risk.
- `不建议`: likely mismatch or hard gate.

## Agent Skill Usage

The skill lives at:

```text
.cursor/skills/finance-job-hunter/SKILL.md
```

When another Cursor Agent sees a request like "upload my resume and find
matching finance AI jobs", it can load the skill, parse the resume, collect JDs,
score them, and export a shortlist.

## Public Repository Safety

The `.gitignore` excludes local state and private data:

- `jobs.db`
- `inbox/*`
- `exports/*`
- `profiles/*`
- `sources/*`
- `.env` and secret files
- real resumes under `resumes/`

Only public-safe examples should be committed.
