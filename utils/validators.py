"""
File:
    parser.py

Purpose:
    Safely parse LLM responses into Python dictionaries.

Responsibilities:
    - Remove markdown fences
    - Extract JSON from noisy responses
    - Handle malformed outputs gracefully
    - Never crash the application

Dependencies:
    json
    re
"""

import json
import re


def parse_json_safe(raw):
    """
    Safely parse an LLM response.

    Args:
        raw: Raw response returned by the LLM.

    Returns:
        dict: Parsed JSON if successful, otherwise {"raw": original_response}.
    """

    if raw is None:
        return {"raw": ""}

    if isinstance(raw, dict):
        return raw

    if isinstance(raw, list):
        return {"data": raw}

    raw = str(raw).strip()

    # ---------------------------------------------------------
    # Remove Markdown code fences (```json ... ```)
    # ---------------------------------------------------------
    raw = re.sub(r"^```(?:json)?", "", raw, flags=re.IGNORECASE).strip()
    raw = re.sub(r"```$", "", raw).strip()

    # ---------------------------------------------------------
    # First attempt: parse the entire response as JSON
    # ---------------------------------------------------------
    try:
        return json.loads(raw)
    except Exception:
        pass

    # ---------------------------------------------------------
    # Second attempt: extract the JSON object from surrounding text
    # ---------------------------------------------------------
    start = raw.find("{")
    end = raw.rfind("}")

    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(raw[start : end + 1])
        except Exception:
            pass

    # ---------------------------------------------------------
    # Final fallback
    # ---------------------------------------------------------
    return {"raw": raw}
