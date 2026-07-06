"""
File:
    agent.py

Purpose:
    Central export module for all AI agents.

Responsibilities:
    - Import each individual agent.
    - Expose a single import location for the orchestrator.

This keeps the orchestration layer clean:

from agents.agent import (
    jd_analyzer,
    resume_analyzer,
    recommendation_agent,
    outreach_writer,
)
"""

# ==========================================================
# Individual Agent Imports
# ==========================================================
from agents.jd_analyzer import jd_analyzer
from agents.resume_analyzer import resume_analyzer
from agents.recommendation import recommendation_agent
from agents.outreach_writer import outreach_writer
from agents.quality_checker import quality_checker

__all__ = [
    "jd_analyzer",
    "resume_analyzer",
    "recommendation_agent",
    "quality_checker",
    "outreach_writer",
]
