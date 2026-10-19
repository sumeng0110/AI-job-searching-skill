"""Report writers for job shortlists."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable, Mapping


def row_value(row: Mapping[str, Any], key: str) -> Any:
    return row[key]


def bucket_name(score: int) -> str:
    if score >= 55:
        return "优先投"
    if score >= 42:
        return "可冲"
    return "不建议"


def risk_summary(row: Mapping[str, Any]) -> str:
    title = str(row_value(row, "title")).lower()
    location = str(row_value(row, "location") or "").lower()
    url = str(row_value(row, "url") or "").lower()
    text = f"{title} {location} {url}"
    risks = []
    if "remote - us" in text or "united states" in text or "usa" in text:
        risks.append("可能要求当地工作授权")
    if "senior" in text or "lead" in text or "principal" in text:
        risks.append("可能年限偏高")
    if not row_value(row, "url"):
        risks.append("缺少原始链接")
    return "；".join(risks) if risks else "暂无明显风险，仍需投递前确认地点/工签/年限要求。"


def write_jobs_csv(rows: Iterable[Mapping[str, Any]], path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["id", "company", "title", "location", "score", "fit_label", "status", "url", "pitch"]
    with output.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        for row in rows:
            writer.writerow([row_value(row, field) for field in fields])
    return output


def write_bucketed_markdown(rows: list[Mapping[str, Any]], path: str | Path, generated_at: str) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    buckets = {"优先投": [], "可冲": [], "不建议": []}
    for row in rows:
        buckets[bucket_name(int(row_value(row, "score")))].append(row)

    with output.open("w", encoding="utf-8") as f:
        f.write("# 求职匹配清单\n\n")
        f.write(f"导出时间：{generated_at}\n\n")
        for section, section_rows in buckets.items():
            f.write(f"## {section}\n\n")
            if not section_rows:
                f.write("暂无岗位。\n\n")
                continue
            for row in section_rows:
                f.write(f"### #{row_value(row, 'id')} {row_value(row, 'company')} - {row_value(row, 'title')}\n\n")
                f.write(f"- 匹配：{row_value(row, 'score')} / {row_value(row, 'fit_label')}\n")
                f.write(f"- 状态：{row_value(row, 'status')}\n")
                f.write(f"- 地点：{row_value(row, 'location') or 'N/A'}\n")
                if row_value(row, "url"):
                    f.write(f"- 链接：{row_value(row, 'url')}\n")
                f.write(f"- 风险点：{risk_summary(row)}\n")
                f.write("\n**投递话术**\n\n")
                f.write(str(row_value(row, "pitch")) + "\n\n")
    return output
