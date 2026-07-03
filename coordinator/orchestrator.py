"""
File: orchestrator.py

Purpose: Coordinates the execution of a multi-stage AI job hunting pipeline.

Responsibilities:
- Manage asynchronous execution of sequential LlmAgents.
- Ensure isolated ADK sessions to prevent state leakage between stages.
- Safely bridge synchronous UI (Streamlit) execution contexts with async ADK calls.

Dependencies: google.adk, google.genai, dotenv, internal agents and utilities.
"""

# ==========================================================
# Environment
# ==========================================================

from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# Standard Library Imports
# ==========================================================

import asyncio
import json
import uuid
from typing import Any

# ==========================================================
# Google ADK Imports
# ==========================================================

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

# ==========================================================
# Project Imports
# ==========================================================

from agents.agent import (
    jd_analyzer,
    outreach_writer,
    recommendation_agent,
    resume_analyzer,
)
from utils.constants import (
    APP_NAME,
    JD_ANALYSIS_KEY,
    OUTREACH_KEY,
    RECOMMENDATION_KEY,
    RESUME_ANALYSIS_KEY,
)
from utils.helper import clean_text, truncate_resume
from utils.logger import (
    log_agent_start,
    log_error,
    log_parsed_output,
    log_raw_output,
)
from utils.parser import parse_json_safe

# ==========================================================
# Module Constants
# ==========================================================

PipelineResult = dict[str, Any]

USER_ID = "job_hunt_user"


# ==========================================================
# Internal Helpers
# ==========================================================


async def _run_agent(
    agent: LlmAgent, prompt: str, app_name: str, output_key: str
) -> PipelineResult:
    """Run a single LlmAgent via InMemoryRunner and return its parsed output.

    Each agent gets its own isolated InMemoryRunner and session so there is
    no cross-contamination of session state between pipeline stages. The
    agent writes its structured JSON output to ``session.state[output_key]``
    after the run completes; this helper reads that value back and parses it.

    Args:
        agent: An instantiated ``LlmAgent`` with a matching ``output_key``.
        prompt: The full user-facing prompt string for this stage, including
            any context injected from prior stages.
        app_name: The ADK application name used when creating the runner and
            session. Must be consistent within a single pipeline execution.
        output_key: The session-state key the agent writes its output to.

    Returns:
        A dictionary containing the parsed JSON output from the agent.
        Falls back to ``{"raw": <text>}`` if JSON parsing fails.

    Raises:
        RuntimeError: If the ADK runner raises an exception during execution,
            wrapping the original error to preserve the traceback.
    """
    log_agent_start(agent.name)

    # ----------------------------------------------------------
    # Create runner
    # ----------------------------------------------------------
    # Isolate execution environment per agent to guarantee zero state leakage.
    runner = InMemoryRunner(
        agent=agent,
        app_name=app_name,
    )

    # ----------------------------------------------------------
    # Create isolated session
    # ----------------------------------------------------------
    # Unique sessions ensure concurrent orchestrator runs do not collide.
    session_id = str(uuid.uuid4())

    session = await runner.session_service.create_session(
        app_name=app_name,
        user_id=USER_ID,
        session_id=session_id,
    )

    # ----------------------------------------------------------
    # Build ADK Content
    # ----------------------------------------------------------
    # Package the prompt strictly according to GenAI format requirements.
    message = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    # ----------------------------------------------------------
    # Execute Agent
    # ----------------------------------------------------------
    # Stream the async generator to completion to ensure full state writes.
    try:
        async for _event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=message,
        ):
            pass

    except Exception as error:
        log_error(agent.name, error)
        raise RuntimeError(f"{agent.name} failed during execution.") from error

    # ----------------------------------------------------------
    # Retrieve Session State
    # ----------------------------------------------------------
    # Fetch the final session state where the agent deposited its output payload.
    final_session = await runner.session_service.get_session(
        app_name=app_name,
        user_id=USER_ID,
        session_id=session.id,
    )

    raw_output = final_session.state.get(output_key, "")
    log_raw_output(agent.name, raw_output)

    # ----------------------------------------------------------
    # Parse Output
    # ----------------------------------------------------------
    # Ensure downstream tasks receive clean dictionaries rather than raw strings.
    parsed = parse_json_safe(raw_output)
    log_parsed_output(agent.name, parsed)

    # ----------------------------------------------------------
    # Return Result
    # ----------------------------------------------------------
    return parsed


# ==========================================================
# Async Utilities
# ==========================================================


def _run_async_safe(coro: Any) -> Any:
    """Run an async coroutine safely from a synchronous Streamlit context.

    Streamlit may already own a running event loop. This helper detects
    that case and applies ``nest_asyncio`` so the coroutine can be run
    on the existing loop via ``loop.run_until_complete()``. When no loop
    is running, ``asyncio.run()`` is used directly.

    Args:
        coro: Any awaitable coroutine object.

    Returns:
        The return value of the coroutine.
    """
    try:
        # ----------------------------------------------------------
        # Running-loop case
        # ----------------------------------------------------------
        # Streamlit often spins up its own event loop; nest_asyncio prevents
        # "loop already running" runtime errors when we invoke async code.
        loop = asyncio.get_running_loop()
        import nest_asyncio

        nest_asyncio.apply()
        return loop.run_until_complete(coro)
    except RuntimeError:
        # ----------------------------------------------------------
        # asyncio.run case
        # ----------------------------------------------------------
        # Fallback for standard synchronous execution environments (e.g., tests).
        return asyncio.run(coro)


# ==========================================================
# Pipeline
# ==========================================================


async def _pipeline(job_description: str, resume_text: str) -> PipelineResult:
    """Execute the full four-stage agent pipeline asynchronously.

    Normalizes inputs, then runs each agent in sequence, injecting prior
    outputs into each subsequent agent's prompt as structured JSON context.

    Args:
        job_description: Raw job description text pasted by the user.
        resume_text: Raw resume text extracted from the uploaded PDF.

    Returns:
        A ``PipelineResult`` dict with keys:
        ``jd_analysis``, ``resume_analysis``,
        ``recommendation_analysis``, ``outreach_output``.
    """
    job_description = clean_text(job_description)
    resume_text = truncate_resume(clean_text(resume_text))

    # ==========================================================
    # Stage 1 — Job Description Analysis
    # ==========================================================
    # Extract core requirements and company context to ground downstream agents.
    jd_prompt = f"Analyze this Job Description:\n\n{job_description}"

    jd_result = await _run_agent(
        agent=jd_analyzer,
        prompt=jd_prompt,
        app_name=APP_NAME,
        output_key=JD_ANALYSIS_KEY,
    )

    # ==========================================================
    # Stage 2 — Resume Analysis
    # ==========================================================
    # Compare the uploaded resume against the structured JD analysis.
    resume_prompt = (
        f"JD Analysis:\n"
        f"{json.dumps(jd_result, indent=2, ensure_ascii=False)}\n\n"
        f"Resume Text:\n{resume_text}\n\n"
        f"Analyze the resume against the JD analysis above."
    )

    resume_result = await _run_agent(
        agent=resume_analyzer,
        prompt=resume_prompt,
        app_name=APP_NAME,
        output_key=RESUME_ANALYSIS_KEY,
    )

    # ==========================================================
    # Stage 3 — Career Recommendations
    # ==========================================================
    # Synthesize gaps identified in Stage 2 into actionable advice.
    rec_prompt = (
        f"JD Analysis:\n"
        f"{json.dumps(jd_result, indent=2, ensure_ascii=False)}\n\n"
        f"Resume Analysis:\n"
        f"{json.dumps(resume_result, indent=2, ensure_ascii=False)}\n\n"
        f"Provide career recommendations based on the above."
    )

    rec_result = await _run_agent(
        agent=recommendation_agent,
        prompt=rec_prompt,
        app_name=APP_NAME,
        output_key=RECOMMENDATION_KEY,
    )

    # ==========================================================
    # Stage 4 — Outreach Writing
    # ==========================================================
    # Draft tailored communications leveraging all prior contextual analysis.
    outreach_prompt = (
        f"JD Analysis:\n"
        f"{json.dumps(jd_result, indent=2, ensure_ascii=False)}\n\n"
        f"Resume Analysis:\n"
        f"{json.dumps(resume_result, indent=2, ensure_ascii=False)}\n\n"
        f"Recommendations:\n"
        f"{json.dumps(rec_result, indent=2, ensure_ascii=False)}\n\n"
        f"Write a personalized cover letter and application email."
    )

    outreach_result = await _run_agent(
        agent=outreach_writer,
        prompt=outreach_prompt,
        app_name=APP_NAME,
        output_key=OUTREACH_KEY,
    )

    return {
        JD_ANALYSIS_KEY: jd_result,
        RESUME_ANALYSIS_KEY: resume_result,
        RECOMMENDATION_KEY: rec_result,
        OUTREACH_KEY: outreach_result,
    }


# ==========================================================
# Public API
# ==========================================================


class JobHuntOrchestrator:
    """Coordinates the four-stage AI job hunt pipeline.

    Provides a synchronous ``run()`` entry point safe for use from
    Streamlit, and a ``get_pipeline()`` helper for introspection and
    testing (used by ``main.py``).
    """

    def get_pipeline(self) -> list[LlmAgent]:
        """Return the ordered list of agents that make up the pipeline.

        Used by ``main.py`` for startup introspection and by tests to
        verify the pipeline composition without executing it.

        Returns:
            A list of ``LlmAgent`` instances in execution order.
        """
        return [
            jd_analyzer,
            resume_analyzer,
            recommendation_agent,
            outreach_writer,
        ]

    def run(self, job_description: str, resume_text: str) -> PipelineResult:
        """Execute the full pipeline synchronously and return all results.

        Wraps the async ``_pipeline()`` coroutine so Streamlit can call
        this method directly without managing an event loop. Handles
        both the case where Streamlit owns a running loop (via
        ``nest_asyncio``) and the case where no loop exists.

        Args:
            job_description: Raw job description text from the UI text area.
            resume_text: Plain text extracted from the uploaded resume PDF.

        Returns:
            A ``PipelineResult`` dict with keys:
            ``jd_analysis``, ``resume_analysis``,
            ``recommendation_analysis``, ``outreach_output``.

        Raises:
            RuntimeError: Propagated from any agent stage that fails,
                with the original exception attached as ``__cause__``.
        """
        return _run_async_safe(
            _pipeline(
                job_description=job_description,
                resume_text=resume_text,
            )
        )
