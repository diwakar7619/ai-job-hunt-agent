# ============================================================
# Imports
# ============================================================

from google.adk.agents import LlmAgent

from utils.constants import (
    MODEL_NAME,
    OUTREACH_KEY,
)


# ============================================================
# Outreach Writer Agent
# ============================================================

outreach_writer = LlmAgent(
    name="outreach_writer",
    model=MODEL_NAME,
    description="Generates a personalized cover letter and application email.",
    output_key=OUTREACH_KEY,
    instruction="""
You are an expert technical recruiter.

INPUT

You will receive:

1. Job Description Analysis
2. Resume Analysis
3. Recommendation Analysis

TASK

Generate ONLY valid JSON.

{
    "cover_letter": "",
    "email_subject": "",
    "email_body": ""
}

Rules

- Return JSON only.
- Do not use markdown.
- Do not use code fences.
- Cover letter should be around 250 words.
- Email should be concise and professional.
- Tailor everything to the job description and candidate profile.
""",
)
