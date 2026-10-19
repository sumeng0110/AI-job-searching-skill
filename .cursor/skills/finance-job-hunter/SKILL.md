---
name: finance-job-hunter
description: Matches resumes to finance AI, finance systems, accounting automation, BI, and AI product roles. Use when the user asks to upload a resume, find matching jobs, score JDs, create a job shortlist, prepare job-search outreach, or compare finance/AI/product job opportunities.
---

# Finance Job Hunter

## Purpose

Use this skill to turn a resume into a structured job-search profile, collect
finance/AI/product job descriptions, score fit, and produce an actionable
shortlist.

This skill is designed for roles such as:

- Finance AI Product Manager
- Finance FDE / internal deployment engineer
- Accounting automation product manager
- Finance systems / ERP / BI product analyst
- AI workflow or agent implementation consultant for finance teams

## Safety Rules

- Do not upload real resumes, phone numbers, private exports, `jobs.db`, or API
  keys to public repositories.
- Do not auto-submit applications.
- Do not store user credentials, cookies, or passwords.
- Do not bypass captchas, rate limits, or platform access controls.
- For LinkedIn, BOSS, and similar platforms, prefer manual or browser-assisted
  collection over unattended scraping.

## Workflow

1. Parse the resume into a profile:

   ```bash
   python job_hunter.py profile --resume examples/sample_resume.md
   ```

2. Collect jobs:

   - Manual mode: save copied JDs as `.md` files in `inbox/`.
   - Web-assisted mode: use public search, then save selected results to
     `inbox/`.
   - Browser-assisted mode: generate the safety guide and use only visible page
     content:

     ```bash
     python job_hunter.py browser-guide
     ```

3. Import and score jobs:

   ```bash
   python job_hunter.py import-dir
   python job_hunter.py list
   ```

4. Export a shortlist:

   ```bash
   python job_hunter.py export --format md
   ```

## Output Standard

Prefer a short, actionable report with these sections:

- `优先投`: high match, low uncertainty.
- `可冲`: relevant but has seniority, location, visa, or domain gaps.
- `不建议`: clear mismatch, hard engineering gate, local work authorization
  requirement, or unrelated sales/BD direction.

For each job, include:

- Company and title.
- Link.
- Match score and label.
- Why it fits.
- Risk notes.
- Suggested outreach angle.

## When Using External Search

Use search terms that combine role, domain, and work mode:

- `remote finance AI product manager accounting`
- `finance AI automation product manager ERP`
- `accounting automation product manager remote`
- `finance FDE AI workflow internal deployment`
- `FP&A automation AI agent product`

Filter out roles that explicitly require local work authorization unless the
user says they are eligible.

## Additional Examples

See [examples.md](examples.md) for sample prompts and expected outputs.
