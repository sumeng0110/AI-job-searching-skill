"""Resume parsing helpers for public-safe job matching profiles."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


SUPPORTED_EXTENSIONS = {".md", ".txt"}


def read_resume_text(path: Path) -> str:
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"Unsupported resume type: {path.suffix}. First version supports: {supported}")
    return path.read_text(encoding="utf-8")


def extract_heading(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
        if stripped and len(stripped) <= 80:
            return stripped
    return "Resume Profile"


def collect_profile_terms(text: str, config: dict[str, Any]) -> dict[str, Any]:
    lowered = text.lower()
    tracks: dict[str, Any] = {}
    for track_name, track in config["tracks"].items():
        hits: dict[str, list[str]] = {}
        count = 0
        for group_name, group in track["groups"].items():
            group_hits = [term for term in group["terms"] if term.lower() in lowered]
            if group_hits:
                hits[group_name] = group_hits
                count += len(group_hits)
        tracks[track_name] = {
            "label": track["label"],
            "keyword_hits": count,
            "groups": hits,
        }
    return tracks


def suggest_search_terms(profile: dict[str, Any]) -> list[str]:
    target_roles = profile["target_roles"]
    terms = [
        "finance AI product manager accounting automation",
        "finance FDE AI workflow internal deployment",
        "accounting automation product manager ERP",
        "FP&A automation AI agent product",
        "finance systems AI analyst Power BI SQL",
    ]
    for role in target_roles[:3]:
        normalized = re.sub(r"\s+", " ", role).strip()
        if normalized:
            terms.insert(0, normalized)
    return list(dict.fromkeys(terms))


def build_resume_profile(path: str | Path, config: dict[str, Any]) -> dict[str, Any]:
    resume_path = Path(path)
    text = read_resume_text(resume_path)
    tracks = collect_profile_terms(text, config)
    target_roles = [
        "Finance AI Product Manager",
        "Finance FDE / Internal Deployment Engineer",
        "Accounting Automation Product Manager",
        "Finance Systems / BI Product Analyst",
    ]
    profile = {
        "source_file": str(resume_path),
        "title": extract_heading(text),
        "target_roles": target_roles,
        "tracks": tracks,
        "resume_focus": config.get("resume_focus", {}),
        "search_terms": [],
        "privacy_note": "Keep real resumes and generated profiles out of public Git repositories.",
    }
    profile["search_terms"] = suggest_search_terms(profile)
    return profile


def write_resume_profile(profile: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
