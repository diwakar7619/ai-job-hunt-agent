"""
Centralized Prompt Package

All system prompts are exposed through helper functions.

This keeps prompt engineering separate from business logic
and allows future prompt versioning or A/B testing.
"""

from .jd_prompt import get_jd_prompt
from .resume_prompt import get_resume_prompt
from .recommendation_prompt import get_recommendation_prompt
from .outreach_prompt import get_outreach_prompt
from .quality_prompt import get_quality_prompt

__all__ = [
    "get_jd_prompt",
    "get_resume_prompt",
    "get_recommendation_prompt",
    "get_outreach_prompt",
]


__all__ = [..., "get_quality_prompt"]
