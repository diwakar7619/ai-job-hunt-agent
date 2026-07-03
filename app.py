import os
from dotenv import load_dotenv

load_dotenv()

import asyncio
import json
import streamlit as st
import pdfplumber
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents.agent import root_agent

APP_NAME = "ai_fresher_job_hunt"
USER_ID = "user_1"

st.set_page_config(page_title="AI Job Hunt Agent", layout="wide")


async def init_session():
    sessions = InMemorySessionService()
    session = await sessions.create_session(app_name=APP_NAME, user_id=USER_ID)
    runner = Runner(agent=root_agent, session_service=sessions, app_name=APP_NAME)
    return sessions, session, runner


async def run_agent(runner, session_id, prompt):
    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    result_text = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=session_id, new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    result_text = part.text
    return result_text


def parse_json_block(text, key):
    """Extract first JSON object from agent output that contains `key`."""
    try:
        # Strip markdown fences if any
        clean = (
            text.strip()
            .removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )
        data = json.loads(clean)
        if key in data:
            return data
    except Exception:
        pass
    # Fallback: scan for JSON objects
    for chunk in text.split("\n\n"):
        try:
            data = json.loads(chunk.strip())
            if key in data:
                return data
        except Exception:
            continue
    return None


def render_match_result(rec):
    """Render rich UI from MATCH_JSON."""
    pct = rec.get("match_percentage", 0)
    color = "#00d26a" if pct >= 60 else "#ffa500" if pct >= 40 else "#ff4b4b"

    col_score, col_verdict = st.columns([1, 3])
    with col_score:
        st.markdown(
            f"<div style='text-align:center; padding:16px; background:#1e2130; border-radius:8px;'>"
            f"<div style='color:#888; font-size:11px; letter-spacing:1px;'>MATCH SCORE</div>"
            f"<div style='color:{color}; font-size:48px; font-weight:bold;'>{pct}%</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_verdict:
        summary = rec.get("recommendation_summary", "—")
        st.markdown(
            f"<div style='padding:16px; background:#1e2130; border-radius:8px; height:100%;'>"
            f"<div style='color:#888; font-size:11px; letter-spacing:1px; margin-bottom:8px;'>VERDICT</div>"
            f"<div style='color:#e2e8f0; font-size:14px; line-height:1.6;'>{summary}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    col_match, col_miss = st.columns(2)
    with col_match:
        st.markdown("**✅ Matching Skills**")
        tags = " ".join(
            f"<span style='background:#0d3d2a; color:#00d26a; padding:3px 10px; border-radius:12px; margin:3px; display:inline-block; font-size:12px;'>{s}</span>"
            for s in rec.get("matching_skills", [])
        )
        st.markdown(tags or "—", unsafe_allow_html=True)

    with col_miss:
        st.markdown("**❌ Missing Skills**")
        tags = " ".join(
            f"<span style='background:#3d1515; color:#ff4b4b; padding:3px 10px; border-radius:12px; margin:3px; display:inline-block; font-size:12px;'>{s}</span>"
            for s in rec.get("missing_skills", [])
        )
        st.markdown(tags or "—", unsafe_allow_html=True)


def render_sidebar_record(record, idx):
    rec = record.get("match_json")
    pct = rec.get("match_percentage", "?") if rec else "?"
    color = (
        "#00d26a"
        if isinstance(pct, int) and pct >= 60
        else "#ffa500"
        if isinstance(pct, int) and pct >= 40
        else "#ff4b4b"
    )
    label = f"Run {idx + 1}: {record['jd_preview']}"
    with st.sidebar.expander(label):
        if rec:
            st.markdown(
                f"<span style='background:{color}22; color:{color}; padding:2px 10px; border-radius:10px; font-size:12px;'>{pct}% match</span>",
                unsafe_allow_html=True,
            )
            summary = rec.get("recommendation_summary", "")
            if summary:
                st.caption(summary[:120] + ("..." if len(summary) > 120 else ""))
        else:
            st.write(record["output"])


# ── Init ──────────────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    sessions, session, runner = asyncio.run(init_session())
    st.session_state.session_id = session.id
    st.session_state.runner = runner
    st.session_state.analysis_history = []

# ── Main UI ───────────────────────────────────────────────────────────────────
st.title("🎯 AI Fresher Job Hunt Agent")
st.markdown("Analyze JDs, match your resume, and generate outreach.")

col1, col2 = st.columns(2)
with col1:
    jd_input = st.text_area("Paste Job Description", height=250)
with col2:
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    resume_input = ""
    if resume_file:
        with pdfplumber.open(resume_file) as pdf:
            resume_input = "\n".join(
                page.extract_text() for page in pdf.pages if page.extract_text()
            )
        st.success("Resume parsed!")

if st.button("Run Full Analysis"):
    if jd_input and resume_input:
        with st.spinner("Running agents..."):
            prompt = f"Job Description:\n{jd_input}\n\nResume:\n{resume_input}"
            result = asyncio.run(
                run_agent(st.session_state.runner, st.session_state.session_id, prompt)
            )

        # Parse MATCH_JSON from result
        match_json = parse_json_block(result, "match_percentage")

        record = {
            "jd_preview": jd_input[:60] + "...",
            "output": result,
            "match_json": match_json,
        }
        st.session_state.analysis_history.append(record)

        if match_json:
            render_match_result(match_json)
        else:
            st.warning("Could not parse structured result. Raw output:")
            st.write(result)

        # Email section — look for email JSON in same result blob
        email_json = parse_json_block(result, "subject")
        if email_json:
            with st.expander("📧 Outreach Email"):
                st.markdown(f"**Subject:** {email_json.get('subject', '')}")
                st.markdown(email_json.get("body", ""))
    else:
        st.warning("Provide a JD and upload a PDF resume.")

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("Session Memory")
if st.session_state.analysis_history:
    for idx, record in enumerate(st.session_state.analysis_history):
        render_sidebar_record(record, idx)
else:
    st.sidebar.info("No analyses yet.")
