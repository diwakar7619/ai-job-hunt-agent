"""
File:
    helper.py

Purpose:
    Common reusable helper functions.

Responsibilities:
    - Resume preprocessing
    - Company extraction
    - Candidate extraction
    - Text cleanup
"""

import re


MAX_RESUME_LENGTH = 35000


def clean_text(text: str) -> str:
    """Normalize whitespace."""

    if not text:
        return ""

    return re.sub(r"\s+", " ", text).strip()


def truncate_resume(text: str) -> str:
    """Prevent extremely long prompts."""

    return clean_text(text)[:MAX_RESUME_LENGTH]


def extract_name(resume_text: str) -> str:
    """
    Assumes candidate name is near top of resume.
    """

    if not resume_text:
        return ""

    for line in resume_text.splitlines():
        line = line.strip()

        if len(line) > 3 and len(line) < 60 and any(c.isalpha() for c in line):
            return line.title()

    return ""


def extract_company(job_description: str) -> str:
    """
    Very lightweight extraction.

    Future improvement:
        Use LLM if needed.
    """

    patterns = [
        r"Company\s*:\s*(.+)",
        r"About\s+(.+)",
        r"Join\s+(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, job_description, flags=re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return ""
