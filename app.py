# ============================================================
# Imports
# ============================================================

import streamlit as st

from tools.pdf_reader import extract_text


# ============================================================
# Streamlit Configuration
# ============================================================

st.set_page_config(
    page_title="AI Fresher Job Hunt Agent",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# Page Header
# ============================================================

st.title("🤖 AI Fresher Job Hunt Agent")
st.caption("Kaggle 5-Day AI Agents Vibe Coding Capstone")

st.divider()


# ============================================================
# Input Section
# ============================================================

left, right = st.columns(2)


# ------------------------------------------------------------
# Job Description Input
# ------------------------------------------------------------

with left:
    st.subheader("Job Description")

    job_description = st.text_area(
        label="Paste the Job Description",
        height=350,
        placeholder="Paste the complete Job Description here...",
    )


# ------------------------------------------------------------
# Resume Upload
# ------------------------------------------------------------

with right:
    st.subheader("Resume")

    resume = st.file_uploader(
        label="Upload Resume (PDF)",
        type=["pdf"],
    )


# ============================================================
# Analyze Button
# ============================================================

analyze = st.button(
    "Analyze Application",
    type="primary",
    use_container_width=True,
)


# ============================================================
# Results Section
# ============================================================

st.divider()

st.subheader("Results")

jd_tab, resume_tab, recommendation_tab, outreach_tab = st.tabs(
    [
        "JD Analysis",
        "Resume Analysis",
        "Recommendations",
        "Outreach",
    ]
)


# ------------------------------------------------------------
# JD Analysis Tab
# ------------------------------------------------------------

with jd_tab:
    st.info("JD Analyzer output will appear here.")


# ------------------------------------------------------------
# Resume Analysis Tab
# ------------------------------------------------------------

with resume_tab:
    st.info("Resume Analyzer output will appear here.")


# ------------------------------------------------------------
# Recommendation Tab
# ------------------------------------------------------------

with recommendation_tab:
    st.info("Recommendations will appear here.")


# ------------------------------------------------------------
# Outreach Tab
# ------------------------------------------------------------

with outreach_tab:
    st.info("Cover Letter and Email will appear here.")


# ============================================================
# Analyze Workflow
# ============================================================

if analyze:
    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if not job_description.strip():
        st.warning("Please paste a Job Description.")

    elif resume is None:
        st.warning("Please upload a Resume PDF.")

    else:
        # ----------------------------------------------------
        # Step 1 : Extract Resume Text
        # ----------------------------------------------------

        resume_text = extract_text(resume)

        st.success("Resume processed successfully!")

        # ----------------------------------------------------
        # Step 2 : Preview Extracted Resume
        # ----------------------------------------------------

        with st.expander("Extracted Resume Text"):
            st.text(resume_text)

        # ----------------------------------------------------
        # Step 3 : Upcoming Pipeline
        # ----------------------------------------------------
        #
        # JD Analyzer
        #        ↓
        # Resume Analyzer
        #        ↓
        # Recommendation Agent
        #        ↓
        # Outreach Writer
        #
        # (To be connected next)
        # ----------------------------------------------------
