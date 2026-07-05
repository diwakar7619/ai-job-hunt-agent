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
# Page Config
# ==========================================================

st.set_page_config(
    page_title="AI Fresher Job Hunt Agent",
    page_icon="🤖",
    layout="wide",
)


# ==========================================================
# Helpers — Label Normalization
# ==========================================================


def _normalize_fit_label(raw: str) -> str:
    if not raw or raw == "N/A":
        return raw
    text = raw.lower()
    if any(w in text for w in ["strong", "excellent", "great", "highly"]):
        return "Strong"
    if any(w in text for w in ["moderate", "partial", "some", "decent"]):
        return "Moderate"
    if any(w in text for w in ["weak", "poor", "low", "limited", "lacks"]):
        return "Weak"
    if len(raw) <= 15:
        return raw.strip().title()
    return "Moderate"


def _normalize_experience_label(raw: str) -> str:
    if not raw or raw == "N/A":
        return raw
    text = raw.lower()
    if any(w in text for w in ["high", "strong", "excellent", "well", "closely"]):
        return "High"
    if any(w in text for w in ["medium", "moderate", "partial", "some"]):
        return "Medium"
    if any(w in text for w in ["low", "weak", "limited", "no ", "none", "lacks"]):
        return "Low"
    if len(raw) <= 10:
        return raw.strip().title()
    return "Medium"


# ==========================================================
# Helpers — UI Components
# ==========================================================


def render_header() -> None:
    st.title("🤖 AI Fresher Job Hunt Agent")
    st.caption("Kaggle 5-Day AI Agents Vibe Coding Capstone")
    st.markdown(
        "**Stack:** `Google ADK` · `Gemini 2.5 Flash` · `Multi-Agent Pipeline` · `Streamlit`"
    )
    st.divider()


def render_dashboard(resume_result: dict) -> None:
    st.subheader("📊 Candidate Match Dashboard")

    fit_label = _normalize_fit_label(resume_result.get("overall_fit", "N/A"))
    exp_label = _normalize_experience_label(
        resume_result.get("experience_match", "N/A")
    )

    matched_skills = resume_result.get("matched_skills", [])
    missing_skills = resume_result.get("missing_skills", [])
    total_skills = len(matched_skills) + len(missing_skills)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Fit", fit_label)
    c2.metric("Experience Match", exp_label)
    c3.metric(
        "✅ Matched Skills",
        len(matched_skills),
        delta=f"of {total_skills} required" if total_skills else None,
        delta_color="off",
    )
    c4.metric(
        "❌ Missing Skills",
        len(missing_skills),
        delta=f"of {total_skills} required" if total_skills else None,
        delta_color="off",
    )
    st.divider()


def render_execution_timeline(stages_done: list[str]) -> None:
    all_stages = [
        ("🔍", "JD Analyzer"),
        ("📄", "Resume Analyzer"),
        ("💡", "Recommendation Agent"),
        ("✉️", "Outreach Writer"),
    ]

    st.subheader("⚡ Agent Execution Timeline")

    for i, (icon, label) in enumerate(all_stages):
        done = label in stages_done
        status = "✅" if done else "⏳"
        state_label = "Complete" if done else "Pending"

        col_icon, col_text = st.columns([0.08, 0.92])
        with col_icon:
            st.write(status)
        with col_text:
            st.write(f"**{icon} {label}** — {state_label}")

        if i < len(all_stages) - 1:
            c1, c2 = st.columns([0.08, 0.92])
            with c1:
                st.write("│")
            with c2:
                st.write("▼")

    st.divider()


def render_download_center(results: dict) -> None:
    st.subheader("⬇️ Download Center")

    outreach_result = results.get(OUTREACH_KEY, {})
    cover_letter = outreach_result.get("cover_letter", "")
    email_body = outreach_result.get("email_body", "")
    email_subject = outreach_result.get("email_subject", "")

    full_json = json.dumps(results, indent=2, ensure_ascii=False)
    cover_letter_txt = f"COVER LETTER\n{'=' * 40}\n\n{cover_letter}"
    email_txt = f"EMAIL SUBJECT: {email_subject}\n{'=' * 40}\n\n{email_body}"

    d1, d2, d3 = st.columns(3)
    with d1:
        st.download_button(
            label="📦 Full Analysis (JSON)",
            data=full_json,
            file_name="job_hunt_analysis.json",
            mime="application/json",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            label="📝 Cover Letter (TXT)",
            data=cover_letter_txt,
            file_name="cover_letter.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with d3:
        st.download_button(
            label="📧 Outreach Email (TXT)",
            data=email_txt,
            file_name="outreach_email.txt",
            mime="text/plain",
            use_container_width=True,
        )
    st.divider()


# ==========================================================
# STATE 1 — Input Page
# ==========================================================


def show_input_page() -> None:
    render_header()

    with st.expander("⚙️ Pipeline Architecture", expanded=False):
        st.markdown(
            """
**Sequential Multi-Agent Workflow**

```
JD Analyzer
     │
     ▼
Resume Analyzer
     │
     ▼
Recommendation Agent
     │
     ▼
Outreach Writer
```

Each agent receives structured output from the previous stage.
Powered by **Google ADK SequentialAgent** with **Gemini 2.5 Flash**.
            """
        )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Job Description")
        job_description = st.text_area(
            label="Paste the Job Description",
            height=350,
            placeholder="Paste the complete Job Description here...",
            key="jd_input",
        )

    with right:
        st.subheader("Resume")
        resume = st.file_uploader(
            label="Upload Resume (PDF)",
            type=["pdf"],
            key="resume_input",
        )

    analyze = st.button(
        label="🚀 Analyze Application",
        type="primary",
        use_container_width=True,
    )

    if analyze:
        if not job_description.strip():
            st.warning("Please paste a Job Description.")
        elif resume is None:
            st.warning("Please upload a Resume PDF.")
        else:
            try:
                resume_text = extract_text(resume)
                if not resume_text.strip():
                    st.error(
                        "Could not extract text from the PDF. Try a different file."
                    )
                    st.stop()

                # Store resume text for optional debug view later
                st.session_state["resume_text_debug"] = resume_text

                with st.spinner(
                    "Running Google ADK Pipeline...\n"
                    "  ✓ JD Analysis\n"
                    "  ✓ Resume Analysis\n"
                    "  ✓ Recommendations\n"
                    "  ✓ Outreach"
                ):
                    orchestrator = JobHuntOrchestrator()
                    results = orchestrator.run(job_description, resume_text)
                    st.session_state["results"] = results

                st.rerun()

            except Exception as error:
                st.error(f"Pipeline failed: {error}")
                st.exception(error)


# ==========================================================
# STATE 2 — Results Page
# ==========================================================


def show_results_page(results: dict[str, Any]) -> None:
    render_header()

    jd_result = results.get(JD_ANALYSIS_KEY, {})
    resume_result = results.get(RESUME_ANALYSIS_KEY, {})
    recommendation_result = results.get(RECOMMENDATION_KEY, {})
    outreach_result = results.get(OUTREACH_KEY, {})

    # ── Dashboard ─────────────────────────────────────────
    render_dashboard(resume_result)

    # ── Execution Timeline ────────────────────────────────
    completed_stages = []
    if jd_result:
        completed_stages.append("JD Analyzer")
    if resume_result:
        completed_stages.append("Resume Analyzer")
    if recommendation_result:
        completed_stages.append("Recommendation Agent")
    if outreach_result:
        completed_stages.append("Outreach Writer")

    render_execution_timeline(completed_stages)

    # ── Tabs ──────────────────────────────────────────────
    jd_tab, resume_tab, rec_tab, outreach_tab = st.tabs(
        [
            "🏢 Job Analysis",
            "👤 Resume Match",
            "🎯 Recommendations",
            "✉️ Outreach",
        ]
    )

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
                st.write("**🔧 Required Skills:**")
                for s in jd_result["required_skills"]:
                    st.write(f"  - {s}")

            if jd_result.get("preferred_skills"):
                st.write("**⭐ Preferred Skills:**")
                for s in jd_result["preferred_skills"]:
                    st.write(f"  - {s}")

            if jd_result.get("responsibilities"):
                st.write("**📋 Responsibilities:**")
                for r in jd_result["responsibilities"]:
                    st.write(f"  - {r}")

    with resume_tab:
        if "raw" in resume_result:
            st.text(resume_result["raw"])
        else:
            st.write(f"**Overall Fit:** {resume_result.get('overall_fit', 'N/A')}")
            st.write(
                f"**Experience Match:** {resume_result.get('experience_match', 'N/A')}"
            )
            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.write("**✅ Matched Skills**")
                for s in resume_result.get("matched_skills", []):
                    st.write(f"  - {s}")
                st.write("**💪 Strengths**")
                for s in resume_result.get("strengths", []):
                    st.write(f"  - {s}")
            with col2:
                st.write("**❌ Missing Skills**")
                for s in resume_result.get("missing_skills", []):
                    st.write(f"  - {s}")
                st.write("**⚠️ Weaknesses**")
                for s in resume_result.get("weaknesses", []):
                    st.write(f"  - {s}")

    with rec_tab:
        if "raw" in recommendation_result:
            st.text(recommendation_result["raw"])
        else:
            if recommendation_result.get("priority_skills"):
                st.write("**🎯 Priority Skills to Learn:**")
                for s in recommendation_result["priority_skills"]:
                    st.write(f"  - {s}")

            if recommendation_result.get("learning_plan"):
                st.write("**📚 Learning Plan:**")
                for item in recommendation_result["learning_plan"]:
                    st.write(f"  - {item}")

            if recommendation_result.get("resume_improvements"):
                st.write("**📝 Resume Improvements:**")
                for item in recommendation_result["resume_improvements"]:
                    st.write(f"  - {item}")

            if recommendation_result.get("project_recommendations"):
                st.write("**🚀 Project Recommendations:**")
                for item in recommendation_result["project_recommendations"]:
                    st.write(f"  - {item}")

            if recommendation_result.get("interview_focus"):
                st.write("**💬 Interview Focus Areas:**")
                for item in recommendation_result["interview_focus"]:
                    st.write(f"  - {item}")

    with outreach_tab:
        if "raw" in outreach_result:
            st.text(outreach_result["raw"])
        else:
            st.write(
                f"**📌 Email Subject:** {outreach_result.get('email_subject', '')}"
            )
            st.divider()

            cover_letter_val = outreach_result.get("cover_letter", "")
            edited_cl = st.text_area(
                label="Cover Letter (editable)",
                value=cover_letter_val,
                height=300,
                key="edited_cover_letter",
            )

            st.divider()
            st.write("**📧 Email Body:**")
            st.text(outreach_result.get("email_body", ""))

            # ── Human-in-the-loop ────────────────────────────
            if st.button("🔄 Regenerate Cover Letter with My Edits"):
                with st.spinner("Regenerating cover letter..."):
                    try:
                        jd_context = json.dumps(jd_result, indent=2, ensure_ascii=False)
                        resume_context = json.dumps(
                            resume_result, indent=2, ensure_ascii=False
                        )
                        recommendation_context = json.dumps(
                            recommendation_result, indent=2, ensure_ascii=False
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

                        st.session_state["results"][OUTREACH_KEY] = new_outreach
                        st.success("Cover letter regenerated!")
                        st.rerun()

                    except Exception as error:
                        st.error(f"Regeneration failed: {error}")

    st.divider()

    # ── Download Center ───────────────────────────────────
    render_download_center(results)

    # ── Debug — hidden by default ─────────────────────────
    if st.session_state.get("resume_text_debug"):
        with st.expander("🔍 Debug — Extracted Resume Text", expanded=False):
            text = st.session_state["resume_text_debug"]
            st.text(text[:2000] + ("..." if len(text) > 2000 else ""))

    st.divider()

    # ── New Analysis ──────────────────────────────────────
    if st.button("🔄 Analyze Another Job", use_container_width=True):
        for key in ["results", "resume_text_debug"]:
            st.session_state.pop(key, None)
        st.rerun()


# ==========================================================
# Router — Two-State UI
# ==========================================================

if "results" not in st.session_state:
    show_input_page()
else:
    show_results_page(st.session_state["results"])
