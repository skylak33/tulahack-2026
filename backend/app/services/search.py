import json
from datetime import datetime
from uuid import UUID

from google import genai
from google.genai import types
from pydantic import BaseModel

from app.config import GEMINI_API_KEY


# ── Gemini response schema ────────────────────────────────────────────────────


class _CandidateAnalysis(BaseModel):
    user_id: str
    compatibility_score: float
    compatibility_summary: str
    strengths: list[str]
    risks: list[str]


class _GeminiVerdict(BaseModel):
    candidates: list[_CandidateAnalysis]
    summary: str


# ── Scoring ───────────────────────────────────────────────────────────────────


def _disc_compatibility(team_members: list[dict], candidate: dict) -> float:
    """Score how well a candidate's DISC complements the team."""
    candidate_disc = candidate.get("disc_profile")
    if not candidate_disc:
        return 0.5

    profiles = [m["disc_profile"] for m in team_members if m.get("disc_profile")]
    if not profiles:
        return 0.5

    avg = {
        k: sum(p.get(k, 0) for p in profiles) / len(profiles)
        for k in ("D", "I", "S", "C")
    }
    gaps = {k: max(0.0, 50 - avg[k]) for k in avg}
    total_gap = sum(gaps.values())
    if total_gap == 0:
        return 0.5

    fill = sum(min(candidate_disc.get(k, 0), gaps[k]) for k in gaps)
    return min(fill / total_gap, 1.0)


# ── Serialization ─────────────────────────────────────────────────────────────


def _serialize(obj) -> dict:
    result = {}
    for k, v in obj.items() if isinstance(obj, dict) else dict(obj).items():
        if isinstance(v, UUID):
            result[k] = str(v)
        elif isinstance(v, datetime):
            result[k] = v.isoformat()
        else:
            result[k] = v
    return result


# ── Main service ──────────────────────────────────────────────────────────────


async def analyze_candidates(
    query_text: str,
    team_members: list[dict],
    candidates: list[dict],
    top_n: int = 10,
) -> dict:
    scored = sorted(
        candidates,
        key=lambda c: _disc_compatibility(team_members, c),
        reverse=True,
    )[:top_n]

    team_info = [
        {
            "full_name": m.get("full_name"),
            "team_role": m.get("team_role"),
            "disc_profile": m.get("disc_profile"),
            "motivation_profile": m.get("motivation_profile"),
        }
        for m in team_members
    ]

    candidates_info = [
        {
            "id": str(c["id"]),
            "full_name": c.get("full_name"),
            "age": c.get("age"),
            "team_role": c.get("team_role"),
            "disc_profile": c.get("disc_profile"),
            "motivation_profile": c.get("motivation_profile"),
        }
        for c in scored
    ]

    prompt = (
        "Ты эксперт по подбору команд. Менеджер ищет нового сотрудника.\n\n"
        f"Запрос менеджера: {query_text}\n\n"
        f"Текущая команда:\n{json.dumps(team_info, ensure_ascii=False, indent=2)}\n\n"
        f"Кандидаты для оценки:\n{json.dumps(candidates_info, ensure_ascii=False, indent=2)}\n\n"
        "Для каждого кандидата оцени совместимость с командой и запросом менеджера. Выведи кандидатов в порядке убывания по оценке совместимости"
        "Учитывай DISC-профили, роли, мотивацию и пожелания менеджера. "
        "Верни JSON строго по схеме."
    )

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=_GeminiVerdict,
        ),
    )

    gemini_data = json.loads(response.text)
    candidate_by_id = {str(c["id"]): c for c in scored}

    result_candidates = []
    for item in gemini_data["candidates"]:
        user_data = candidate_by_id.get(item["user_id"])
        if user_data is None:
            continue
        result_candidates.append(
            {
                "user": _serialize(user_data),
                "compatibility_score": item["compatibility_score"],
                "compatibility_summary": item["compatibility_summary"],
                "strengths": item["strengths"],
                "risks": item["risks"],
            }
        )

    return {
        "candidates": result_candidates,
        "summary": gemini_data["summary"],
    }
