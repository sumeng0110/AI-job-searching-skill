# Finance Job Hunter Examples

## Example 1: Resume to Job Profile

User request:

```text
Upload this resume and build a job-search profile for finance AI roles.
```

Agent action:

```bash
python job_hunter.py profile --resume path/to/resume.md
```

Expected output:

- Structured profile saved to `profiles/resume_profile.json`.
- Summary of target tracks, keywords, and suggested search terms.

## Example 2: Score Copied JDs

User request:

```text
I copied several LinkedIn and company-site JDs into inbox. Rank them.
```

Agent action:

```bash
python job_hunter.py import-dir
python job_hunter.py export --format md
```

Expected output:

- Markdown shortlist in `exports/`.
- Jobs grouped as `优先投`, `可冲`, and `不建议`.

## Example 3: Browser-Assisted Collection

User request:

```text
Open LinkedIn/BOSS manually and help me collect visible jobs safely.
```

Agent action:

```bash
python job_hunter.py browser-guide
```

Expected output:

- Safety guide in `sources/browser_assisted_guide.md`.
- User manually confirms any copied content before import.
