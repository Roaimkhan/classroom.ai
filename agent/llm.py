from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

try:
    from google import genai
except ModuleNotFoundError:  # pragma: no cover - handled at runtime
    genai = None


BASE_DIR = Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH = BASE_DIR / "system_prompt.txt"


def _load_system_prompt() -> str:
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    return "You are a helpful assignment assistant. Return JSON with a concise answer."


def run_llm(payload: Any) -> dict[str, Any]:
    """Run the Gemini model if configured; otherwise return a stub payload."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or genai is None:
        text = payload if isinstance(payload, str) else json.dumps(payload, indent=2, ensure_ascii=False)
        return {
            "status": "stub",
            "note": "GEMINI_API_KEY is not configured or the google-genai package is unavailable.",
            "answer": text[:2000],
        }

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {"text": _load_system_prompt()},
            {"text": json.dumps(payload, ensure_ascii=False, indent=2)},
        ],
    )

    text = getattr(response, "text", None)
    if text is None:
        raw = str(response)
        return {"status": "ok", "answer": raw}

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = {"raw_response": text}
    return {"status": "ok", "answer": parsed}


if __name__ == "__main__":
    print(run_llm({"tasks": ["Task 1"], "instructions": ["Do the work"]}))
