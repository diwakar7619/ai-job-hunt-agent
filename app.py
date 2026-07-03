"""
File: app.py

Purpose: Provides the main Streamlit user interface for the AI Fresher Job Hunt Agent.

Responsibilities:
- Handle user inputs for job descriptions and resumes.
- Coordinate the execution of the JobHuntOrchestrator pipeline.
- Render pipeline results across categorized tabs.
- Support human-in-the-loop workflow for outreach regeneration.

Dependencies: streamlit, json, tools.pdf_reader, coordinator.orchestrator, agents.outreach_writer, utils.constants
"""

# ==========================================================
# Imports
# ==========================================================

import json
from typing import Any

import streamlit as st

from agents.outreach_writer import outreach_writer
from coordinator.orchestrator import JobHuntOrchestrator, _run_agent, _run_async_safe
from tools.pdf_reader import extract_text
from utils.constants import (
    APP_NAME,
    JD_ANALYSIS_KEY,
    OUTREACH_KEY,
    RECOMMENDATION_KEY,
    RESUME_ANALYSIS_KEY,
)


# ==========================================================
# Configuration
# ==========================================================

# Configure the main Streamlit page settings
st.set_page_config(
    page_title="AI Fresher Job Hunt Agent",
    page_icon="🤖",
    layout="wide",
)

# Display the application title
st.title("🤖 AI Fresher Job Hunt Agent")

# Display the sub-heading/caption for context
st.caption("Kaggle 5-Day AI Agents Vibe Coding Capstone")

# Visual separator for the header
st.divider()


# ==========================================================
# UI Layout
# ==========================================================

left, right = st.columns(2)

with left:
    st.subheader("Job Description")
    job_description = st.text_area(
        label="Paste the Job Description",
        height=350,
        placeholder="Paste the complete Job Description here...",
    )

with right:
    st.subheader("Resume")
    resume = st.file_uploader(
        label="Upload Resume (PDF)",
        type=["pdf"],
    )

analyze = st.button(
    label="Analyze Application",
    type="primary",
    use_container_width=True,
)

st.divider()
st.subheader("Results")

jd_tab, resume_tab, rec_tab, outreach_tab = st.tabs(
    [
        "JD Analysis",
        "Resume Analysis",
        "Recommendations",
        "Outreach",
    ]
)


# ==========================================================
# Rendering Helpers
# ==========================================================


def render_results(results: dict[str, Any]) -> None:
    jd_result = results.get(JD_ANALYSIS_KEY, {})
    resume_result = results.get(RESUME_ANALYSIS_KEY, {})
    recommendation_result = results.get(RECOMMENDATION_KEY, {})
    outreach_result = results.get(OUTREACH_KEY, {})

    # ── JD Analysis ─────────────────────────────────────────
    with jd_tab:
        if "raw" in jd_result:
            st.text(jd_result["raw"])
        else:
            st.write(f"**Job Title:** {jd_result.get('job_title', 'N/A')}")
            st.write(f"**Summary:** {jd_result.get('summary', 'N/A')}")
            st.write(
                f"**Experience Required:** {jd_result.get('experience_required', 'N/A')}"
            )

            if jd_result.get("required_skills"):
                st.write("**Required Skills:**")
                for s in jd_result["required_skills"]:
                    st.write(f"  - {s}")

            if jd_result.get("preferred_skills"):
                st.write("**Preferred Skills:**")
                for s in jd_result["preferred_skills"]:
                    st.write(f"  - {s}")

            if jd_result.get("responsibilities"):
                st.write("**Responsibilities:**")
                for r in jd_result["responsibilities"]:
                    st.write(f"  - {r}")

    # ── Resume Analysis ─────────────────────────────────────
    with resume_tab:
        if "raw" in resume_result:
            st.text(resume_result["raw"])
        else:
            st.write(f"**Overall Fit:** {resume_result.get('overall_fit', 'N/A')}")
            st.write(
                f"**Experience Match:** {resume_result.get('experience_match', 'N/A')}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Matched Skills ✅**")
                for s in resume_result.get("matched_skills", []):
                    st.write(f"  - {s}")

                st.write("**Strengths 💪**")
                for s in resume_result.get("strengths", []):
                    st.write(f"  - {s}")

            with col2:
                st.write("**Missing Skills ❌**")
                for s in resume_result.get("missing_skills", []):
                    st.write(f"  - {s}")

                st.write("**Weaknesses ⚠️**")
                for s in resume_result.get("weaknesses", []):
                    st.write(f"  - {s}")

    # ── Recommendations ─────────────────────────────────────
    with rec_tab:
        if "raw" in recommendation_result:
            st.text(recommendation_result["raw"])
        else:
            if recommendation_result.get("priority_skills"):
                st.write("**Priority Skills to Learn:**")
                for s in recommendation_result["priority_skills"]:
                    st.write(f"  - {s}")

            if recommendation_result.get("learning_plan"):
                st.write("**Learning Plan:**")
                for item in recommendation_result["learning_plan"]:
                    st.write(f"  - {item}")

            if recommendation_result.get("resume_improvements"):
                st.write("**Resume Improvements:**")
                for item in recommendation_result["resume_improvements"]:
                    st.write(f"  - {item}")

            if recommendation_result.get("project_recommendations"):
                st.write("**Project Recommendations:**")
                for item in recommendation_result["project_recommendations"]:
                    st.write(f"  - {item}")

            if recommendation_result.get("interview_focus"):
                st.write("**Interview Focus Areas:**")
                for item in recommendation_result["interview_focus"]:
                    st.write(f"  - {item}")

    # ── Outreach ────────────────────────────────────────────
    with outreach_tab:
        if "raw" in outreach_result:
            st.text(outreach_result["raw"])
        else:
            st.write(f"**Email Subject:** {outreach_result.get('email_subject', '')}")
            st.divider()

            cover_letter_val = outreach_result.get("cover_letter", "")
            edited_cl = st.text_area(
                label="Cover Letter (editable)",
                value=cover_letter_val,
                height=300,
                key="edited_cover_letter",
            )

            st.divider()
            st.write("**Email Body:**")
            st.text(outreach_result.get("email_body", ""))

            # ==========================================================
            # Human-in-the-loop
            # ==========================================================

            # Allow the user to regenerate the cover letter using their direct edits as feedback
            if st.button("🔄 Regenerate Cover Letter with My Edits"):
                with st.spinner("Regenerating..."):
                    try:
                        # Safely extract all required contexts as formatted JSON strings preserving unicode
                        jd_context = json.dumps(
                            jd_result,
                            indent=2,
                            ensure_ascii=False,
                        )
                        resume_context = json.dumps(
                            resume_result,
                            indent=2,
                            ensure_ascii=False,
                        )
                        recommendation_context = json.dumps(
                            recommendation_result,
                            indent=2,
                            ensure_ascii=False,
                        )

                        regen_prompt = (
                            f"JD Analysis:\n{jd_context}\n\n"
                            f"Resume Analysis:\n{resume_context}\n\n"
                            f"Recommendations:\n{recommendation_context}\n\n"
                            f"User edited cover letter feedback:\n{edited_cl}\n\n"
                            "Rewrite the cover letter incorporating the user's edits."
                        )

                        new_outreach = _run_async_safe(
                            _run_agent(
                                outreach_writer,
                                regen_prompt,
                                APP_NAME,
                                OUTREACH_KEY,
                            )
                        )

                        # Store results in session state so Streamlit reruns preserve outputs.
                        st.session_state["results"][OUTREACH_KEY] = new_outreach
                        st.success("Regenerated!")
                        st.rerun()

                    except Exception as error:
                        st.error(f"Regeneration failed: {error}")


# ==========================================================
# Application State
# ==========================================================

# Store results in session state so Streamlit reruns preserve outputs.
if "results" in st.session_state:
    render_results(st.session_state["results"])


# ==========================================================
# Main Entry
# ==========================================================

if analyze:
    # ── Validate JD ─────────────────────────────────────────
    if not job_description.strip():
        st.warning("Please paste a Job Description.")

    # ── Validate Resume ─────────────────────────────────────
    elif resume is None:
        st.warning("Please upload a Resume PDF.")

    else:
        try:
            # ── Extract Resume ──────────────────────────────────────
            resume_text = extract_text(resume)
            if not resume_text.strip():
                st.error("Could not extract text from the PDF. Try a different file.")
                st.stop()

            with st.expander("Extracted Resume Text"):
                st.text(resume_text[:2000] + ("..." if len(resume_text) > 2000 else ""))

            # ==========================================================
            # Analysis Pipeline
            # ==========================================================

            with st.spinner("Running 4 AI agents... this takes ~30s ⏳"):
                orchestrator = JobHuntOrchestrator()
                results = orchestrator.run(
                    job_description,
                    resume_text,
                )

                # Store results in session state so Streamlit reruns preserve outputs.
                st.session_state["results"] = results

            st.success("Analysis complete!")

            # ── Display Results ─────────────────────────────────────
            render_results(results)

        except Exception as error:
            st.error(f"Pipeline failed: {error}")
            st.exception(error)
