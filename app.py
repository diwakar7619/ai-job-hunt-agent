# ui/app.py
import streamlit as st
from agents.agent import agent

st.set_page_config(page_title="AI Job Hunt Agent", layout="wide")

# 1. Initialize Session Memory
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

st.title("🎯 AI Fresher Job Hunt Agent")
st.markdown(
    "Analyze JDs, match your resume, and generate outreach. History is saved in the sidebar."
)

# 2. Input Section
col1, col2 = st.columns(2)
with col1:
    jd_input = st.text_area("Paste Job Description", height=250)
with col2:
    resume_input = st.text_area("Paste Resume Text", height=250)

# 3. Execution
if st.button("Run Full Analysis"):
    if jd_input and resume_input:
        with st.spinner("Coordinating JD Analysis, Resume Match, and Outreach..."):
            prompt = f"Job Description:\n{jd_input}\n\nResume:\n{resume_input}"

            # Execute sequential coordinator
            result = agent(prompt)

            # Store in memory
            st.session_state.analysis_history.append(
                {"jd_preview": jd_input[:60] + "...", "output": result}
            )

            st.success("Sequence Complete")
            st.write(result)
    else:
        st.warning("Please provide both a JD and a Resume.")

# 4. Session Memory Sidebar
st.sidebar.title("Session Memory")
if st.session_state.analysis_history:
    for idx, record in enumerate(st.session_state.analysis_history):
        with st.sidebar.expander(f"Run {idx + 1}: {record['jd_preview']}"):
            st.write(record["output"])
else:
    st.sidebar.info("No analyses run yet in this session.")
