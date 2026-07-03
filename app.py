import streamlit as st

st.set_page_config(
    page_title="AI Fresher Job Hunt Agent",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Fresher Job Hunt Agent")
st.caption("Kaggle 5-Day AI Agents Vibe Coding Capstone")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Job Description")

    job_description = st.text_area(
        "Paste the Job Description",
        height=350,
        placeholder="Paste the complete job description here...",
    )

with right:
    st.subheader("Resume")

    resume = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"],
    )

analyze = st.button(
    "Analyze Application",
    type="primary",
    use_container_width=True,
)

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

with jd_tab:
    st.info("JD Analyzer output will appear here.")

with resume_tab:
    st.info("Resume Analyzer output will appear here.")

with recommendation_tab:
    st.info("Recommendations will appear here.")

with outreach_tab:
    st.info("Cover letter and email will appear here.")

if analyze:
    if not job_description.strip():
        st.warning("Please paste a Job Description.")
    elif resume is None:
        st.warning("Please upload a resume PDF.")
    else:
        st.success("Inputs received. ADK pipeline will be connected next.")
