# agents/agent.py
from google.adk.agents import Agent
from agents.jd_analyzer import jd_analyzer
from agents.resume_analyzer import resume_analyzer
from agents.recommendation import recommendation_agent
from agents.outreach_writer import outreach_writer

root_agent = Agent(
    name="job_hunt_coordinator",
    model="gemini-2.5-flash",
    description="Orchestrates full job hunt pipeline.",
    instruction="""
You are a job hunt pipeline coordinator. You MUST call all 4 sub-agents in order. Do not stop early.

STEP 1: Call jd_analyzer with the raw Job Description text. Store result as JD_JSON.
STEP 2: Call resume_analyzer with the raw Resume text. Store result as RESUME_JSON.
STEP 3: Call recommendation_agent with the JD_JSON and RESUME_JSON from previous steps.
STEP 4: Call outreach_writer with the JD_JSON, RESUME_JSON, and MATCH_JSON from previous steps.

After ALL 4 steps complete, output EXACTLY this format:

## Analysis Results

Match Score: [match_percentage]%
Matching Skills: [matching_skills as comma list]
Missing Skills: [missing_skills as comma list]

Recommendation:
[recommendation_summary]

Outreach Email:
Subject: [subject_line]

[email_body]

YOU MUST NOT STOP after step 1. All 4 sub-agents are mandatory.
""",
    sub_agents=[jd_analyzer, resume_analyzer, recommendation_agent, outreach_writer],
)
