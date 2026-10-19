#!/usr/bin/env python3
"""Local job search assistant.

This is intentionally semi-automated: it helps collect, score, and prepare
applications, but does not log in to platforms or auto-submit applications.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

from job_hunter_core.matcher import (
    best_tracks as core_best_tracks,
    count_terms as core_count_terms,
    generate_pitch as core_generate_pitch,
    normalize_text as core_normalize_text,
    score_job as core_score_job,
)
from job_hunter_core.reports import write_bucketed_markdown, write_jobs_csv
from job_hunter_core.resume_parser import build_resume_profile, write_resume_profile
from job_hunter_core.sources import write_browser_assisted_guide


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "jobs.db"
CONFIG_PATH = ROOT / "profile_config.json"
EXPORT_DIR = ROOT / "exports"
INBOX_DIR = ROOT / "inbox"
PROFILE_DIR = ROOT / "profiles"
SOURCE_DIR = ROOT / "sources"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(verbose: bool = False) -> None:
    INBOX_DIR.mkdir(exist_ok=True)
    EXPORT_DIR.mkdir(exist_ok=True)
    PROFILE_DIR.mkdir(exist_ok=True)
    SOURCE_DIR.mkdir(exist_ok=True)
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT DEFAULT '',
                url TEXT DEFAULT '',
                source TEXT DEFAULT 'manual',
                jd TEXT NOT NULL,
                status TEXT DEFAULT 'new',
                score INTEGER DEFAULT 0,
                fit_label TEXT DEFAULT '',
                score_detail TEXT DEFAULT '{}',
                pitch TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(company, title, url)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                note TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                FOREIGN KEY(job_id) REFERENCES jobs(id)
            )
            """
        )
    if verbose:
        print(f"initialized: {DB_PATH}")


def normalize_text(text: str) -> str:
    return core_normalize_text(text)


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def count_terms(text: str, terms: list[str]) -> tuple[int, list[str]]:
    return core_count_terms(text, terms)


def score_job(title: str, jd: str, config: dict[str, Any]) -> dict[str, Any]:
    return core_score_job(title, jd, config)


def best_tracks(detail: dict[str, Any]) -> list[tuple[str, int, str]]:
    return core_best_tracks(detail)


def generate_pitch(title: str, company: str, jd: str, score_result: dict[str, Any], config: dict[str, Any]) -> str:
    return core_generate_pitch(title, company, jd, score_result, config)


def add_event(job_id: int, event_type: str, note: str = "") -> None:
    with connect() as conn:
        conn.execute(
            "INSERT INTO events(job_id, event_type, note, created_at) VALUES (?, ?, ?, ?)",
            (job_id, event_type, note, now()),
        )


def add_job(args: argparse.Namespace) -> None:
    init_db()
    config = load_config()
    jd = args.jd or ""
    if args.jd_file:
        jd = read_text(args.jd_file)
    if not jd.strip():
        raise SystemExit("JD is required. Use --jd or --jd-file.")

    title = args.title.strip()
    company = args.company.strip()
    result = score_job(title, jd, config)
    pitch = generate_pitch(title, company, jd, result, config)
    timestamp = now()

    with connect() as conn:
        try:
            cur = conn.execute(
                """
                INSERT INTO jobs(title, company, location, url, source, jd, score, fit_label,
                                 score_detail, pitch, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    title,
                    company,
                    args.location or "",
                    args.url or "",
                    args.source or "manual",
                    jd,
                    result["score"],
                    result["fit_label"],
                    json.dumps(result["detail"], ensure_ascii=False),
                    pitch,
                    timestamp,
                    timestamp,
                ),
            )
            job_id = int(cur.lastrowid)
        except sqlite3.IntegrityError:
            raise SystemExit("Duplicate job: same company/title/url already exists.")

    add_event(job_id, "created", f"{result['fit_label']} {result['score']}")
    print(f"added #{job_id}: {company} - {title} | {result['fit_label']} {result['score']}")
    print_pitch(job_id)


def import_dir(args: argparse.Namespace) -> None:
    init_db()
    directory = Path(args.dir or INBOX_DIR)
    files = sorted([p for p in directory.glob("*") if p.suffix.lower() in {".txt", ".md"}])
    if not files:
        print(f"No .txt/.md files found in {directory}")
        return
    for path in files:
        raw = read_text(path)
        meta, jd = parse_frontmatter(raw)
        ns = argparse.Namespace(
            title=meta.get("title") or path.stem,
            company=meta.get("company") or "Unknown",
            location=meta.get("location") or "",
            url=meta.get("url") or "",
            source=meta.get("source") or "inbox",
            jd=jd,
            jd_file=None,
        )
        try:
            add_job(ns)
        except SystemExit as exc:
            print(f"skip {path.name}: {exc}")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta_text = parts[1]
    body = parts[2].strip()
    meta: dict[str, str] = {}
    for line in meta_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, body


def rescore(_: argparse.Namespace) -> None:
    init_db()
    config = load_config()
    with connect() as conn:
        jobs = conn.execute("SELECT * FROM jobs").fetchall()
        for job in jobs:
            result = score_job(job["title"], job["jd"], config)
            pitch = generate_pitch(job["title"], job["company"], job["jd"], result, config)
            conn.execute(
                """
                UPDATE jobs
                SET score=?, fit_label=?, score_detail=?, pitch=?, updated_at=?
                WHERE id=?
                """,
                (
                    result["score"],
                    result["fit_label"],
                    json.dumps(result["detail"], ensure_ascii=False),
                    pitch,
                    now(),
                    job["id"],
                ),
            )
    print(f"rescored {len(jobs)} jobs")


def list_jobs(args: argparse.Namespace) -> None:
    init_db()
    min_score = args.min_score if args.min_score is not None else 0
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, company, title, location, score, fit_label, status, url
            FROM jobs
            WHERE score >= ?
            ORDER BY score DESC, updated_at DESC
            """,
            (min_score,),
        ).fetchall()
    if not rows:
        print("No jobs yet.")
        return
    for row in rows:
        url = f" | {row['url']}" if row["url"] else ""
        print(
            f"#{row['id']:>3} {row['score']:>3} {row['fit_label']:<5} "
            f"{row['status']:<10} {row['company']} - {row['title']} "
            f"({row['location'] or 'N/A'}){url}"
        )


def get_job(job_id: int) -> sqlite3.Row:
    with connect() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    if row is None:
        raise SystemExit(f"Job not found: {job_id}")
    return row


def print_pitch(job_id: int) -> None:
    job = get_job(job_id)
    print("\n--- pitch ---")
    print(job["pitch"])
    print("-------------\n")


def show_job(args: argparse.Namespace) -> None:
    init_db()
    job = get_job(args.id)
    detail = json.loads(job["score_detail"] or "{}")
    print(f"#{job['id']} {job['company']} - {job['title']}")
    print(f"score: {job['score']} ({job['fit_label']}) | status: {job['status']}")
    if job["url"]:
        print(f"url: {job['url']}")
    print("\nTop tracks:")
    for key, score, label in best_tracks(detail):
        if score:
            print(f"- {label}: {score}")
    if detail.get("risks"):
        print("\nRisks:")
        for name, item in detail["risks"].items():
            print(f"- {name}: -{item['penalty']} ({', '.join(item['hits'])})")
    print_pitch(args.id)


def update_status(args: argparse.Namespace) -> None:
    init_db()
    with connect() as conn:
        cur = conn.execute(
            "UPDATE jobs SET status=?, updated_at=? WHERE id=?",
            (args.status, now(), args.id),
        )
        if cur.rowcount == 0:
            raise SystemExit(f"Job not found: {args.id}")
    add_event(args.id, "status", args.status)
    print(f"updated #{args.id}: {args.status}")


def profile_resume(args: argparse.Namespace) -> None:
    init_db()
    config = load_config()
    output = Path(args.output) if args.output else PROFILE_DIR / "resume_profile.json"
    profile = build_resume_profile(args.resume, config)
    path = write_resume_profile(profile, output)
    print(f"profile saved: {path}")
    print("\nTarget roles:")
    for role in profile["target_roles"]:
        print(f"- {role}")
    print("\nSuggested search terms:")
    for term in profile["search_terms"]:
        print(f"- {term}")


def browser_guide(args: argparse.Namespace) -> None:
    init_db()
    output = Path(args.output) if args.output else SOURCE_DIR / "browser_assisted_guide.md"
    path = write_browser_assisted_guide(output)
    print(f"browser-assisted guide saved: {path}")


def export(args: argparse.Namespace) -> None:
    init_db()
    EXPORT_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M")
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT id, company, title, location, score, fit_label, status, url, pitch
            FROM jobs
            ORDER BY score DESC, updated_at DESC
            """
        ).fetchall()
    if args.format == "csv":
        path = EXPORT_DIR / f"jobs_{stamp}.csv"
        write_jobs_csv(rows, path)
    else:
        path = EXPORT_DIR / f"jobs_{stamp}.md"
        write_bucketed_markdown(rows, path, now())
    print(f"exported: {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local job search assistant")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="initialize database and folders").set_defaults(func=lambda args: init_db(verbose=True))

    add = sub.add_parser("add", help="add one job")
    add.add_argument("--title", required=True)
    add.add_argument("--company", required=True)
    add.add_argument("--location", default="")
    add.add_argument("--url", default="")
    add.add_argument("--source", default="manual")
    add.add_argument("--jd", default="")
    add.add_argument("--jd-file", default="")
    add.set_defaults(func=add_job)

    imp = sub.add_parser("import-dir", help="import .txt/.md jobs from inbox")
    imp.add_argument("--dir", default=str(INBOX_DIR))
    imp.set_defaults(func=import_dir)

    sub.add_parser("rescore", help="rescore all jobs").set_defaults(func=rescore)

    profile = sub.add_parser("profile", help="parse a .md/.txt resume into a job-search profile")
    profile.add_argument("--resume", required=True, help="path to a .md or .txt resume")
    profile.add_argument("--output", default="", help="optional output JSON path")
    profile.set_defaults(func=profile_resume)

    guide = sub.add_parser("browser-guide", help="write browser-assisted collection guide")
    guide.add_argument("--output", default="", help="optional output markdown path")
    guide.set_defaults(func=browser_guide)

    ls = sub.add_parser("list", help="list jobs")
    ls.add_argument("--min-score", type=int, default=0)
    ls.set_defaults(func=list_jobs)

    show = sub.add_parser("show", help="show one job")
    show.add_argument("id", type=int)
    show.set_defaults(func=show_job)

    pitch = sub.add_parser("pitch", help="print pitch for one job")
    pitch.add_argument("id", type=int)
    pitch.set_defaults(func=lambda args: (init_db(), print_pitch(args.id)))

    status = sub.add_parser("status", help="update job status")
    status.add_argument("id", type=int)
    status.add_argument("status", choices=["new", "saved", "applied", "interview", "rejected", "offer", "paused"])
    status.set_defaults(func=update_status)

    exp = sub.add_parser("export", help="export jobs")
    exp.add_argument("--format", choices=["md", "csv"], default="md")
    exp.set_defaults(func=export)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
