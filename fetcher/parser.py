from __future__ import annotations

import json
from typing import Any


def separate_tasks_assignments(text: str) -> dict[str, Any]:
    """Split raw assignment text into a small structured payload.

    This keeps the project importable even before a full Gemini parser is wired up.
    """
    cleaned = text.strip()
    if not cleaned:
        return {"tasks": [], "instructions": [], "raw_text": ""}

    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    tasks = [line for line in lines if line.lower().startswith(("task", "question", "problem", "exercise"))]
    instructions = [line for line in lines if line not in tasks]

    result = {
        "tasks": tasks,
        "instructions": instructions,
        "raw_text": cleaned,
    }
    return result


if __name__ == "__main__":
    print(json.dumps(separate_tasks_assignments("Task 1: solve this problem\nRead the instructions carefully."), indent=2))
