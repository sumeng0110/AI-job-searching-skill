"""Keyword-based job matching and outreach generation."""

from __future__ import annotations

import re
import textwrap
from typing import Any


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def count_terms(text: str, terms: list[str]) -> tuple[int, list[str]]:
    lowered = text.lower()
    hits: list[str] = []
    total = 0
    for term in terms:
        if term.lower() in lowered:
            hits.append(term)
            total += 1
    return total, hits


def score_job(title: str, jd: str, config: dict[str, Any]) -> dict[str, Any]:
    text = f"{title}\n{jd}"
    total = 0
    detail: dict[str, Any] = {"tracks": {}, "risks": {}, "bonuses": []}

    for track_name, track in config["tracks"].items():
        score = 0
        hits_by_group: dict[str, list[str]] = {}
        for group_name, group in track["groups"].items():
            hit_count, hits = count_terms(text, group["terms"])
            if hits:
                group_score = min(group["max"], hit_count * group["weight"])
                score += group_score
                hits_by_group[group_name] = hits
        score = min(track["max_score"], score)
        detail["tracks"][track_name] = {
            "score": score,
            "hits": hits_by_group,
            "label": track["label"],
        }
        total += score

    for bonus in config.get("bonuses", []):
        hit_count, hits = count_terms(text, bonus["terms"])
        if hits:
            points = min(bonus["max"], hit_count * bonus["weight"])
            total += points
            detail["bonuses"].append({"name": bonus["name"], "points": points, "hits": hits})

    for risk in config.get("risks", []):
        hit_count, hits = count_terms(text, risk["terms"])
        if hits:
            penalty = min(risk["max_penalty"], hit_count * risk["penalty"])
            total -= penalty
            detail["risks"][risk["name"]] = {"penalty": penalty, "hits": hits}

    total = max(0, min(100, total))
    if total >= 55:
        fit_label = "强匹配"
    elif total >= 42:
        fit_label = "可投"
    elif total >= 30:
        fit_label = "备选"
    else:
        fit_label = "低优先级"

    return {"score": total, "fit_label": fit_label, "detail": detail}


def best_tracks(detail: dict[str, Any]) -> list[tuple[str, int, str]]:
    rows = []
    for name, item in detail.get("tracks", {}).items():
        rows.append((name, int(item["score"]), item["label"]))
    return sorted(rows, key=lambda x: x[1], reverse=True)


def generate_pitch(title: str, company: str, jd: str, score_result: dict[str, Any], config: dict[str, Any]) -> str:
    del company, jd
    detail = score_result["detail"]
    tracks = best_tracks(detail)
    top_track = tracks[0] if tracks else ("finance_ai_fde", 0, "财务 AI / FDE")
    top_track_key = top_track[0]
    resume_focus = config["resume_focus"].get(top_track_key, config["resume_focus"]["finance_ai_fde"])

    risk_note = ""
    if detail.get("risks"):
        risk_names = "、".join(detail["risks"].keys())
        risk_note = f"\n注意：该岗位存在 {risk_names} 相关要求，投递前需要确认是否为硬门槛。"

    pitch = f"""您好，我关注到贵司「{title}」岗位，和我的经历比较匹配。

我有 4 年外企财务与经营分析背景，覆盖 FP&A、预算、对账、财务系统迁移和数据分析；同时独立做过财务 Agent 工作流、Power BI / Cursor 报表工作流和多模型 AI 应用。

针对这个岗位，我最相关的经验是：{resume_focus}

我比较擅长把业务流程拆成可落地的 AI / 数据方案：先识别高频、规则明确、可校验的流程，再设计输入契约、工具调用、质量门禁和人工复核节点，确保结果可用、可信、可审计。

如果方便的话，希望能进一步沟通这个岗位的具体场景和团队需求。{risk_note}
"""
    return textwrap.dedent(pitch).strip()
