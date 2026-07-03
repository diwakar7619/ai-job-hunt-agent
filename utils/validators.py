"""
File:
    validators.py

Purpose:
    Validation utilities.

Responsibilities:
    - Validate user inputs
    - Validate parsed JSON
"""


def validate_jd(job_description: str):

    return bool(job_description.strip())


def validate_resume(resume_text: str):

    return bool(resume_text.strip())


def validate_json(data):

    return isinstance(data, dict)


def validate_pdf(text: str):

    return len(text.strip()) > 50
