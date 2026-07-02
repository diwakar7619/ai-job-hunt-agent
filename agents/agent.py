# agents/agent.py
from google.adk.agents import Agent
from .jd_analyzer import jd_analyzer
from .resume_analyzer import resume_analyzer
from .recommendation import recommendation_agent
from .outreach_writer import outreach_writer

agent = Agent(
    name="job_hunt_coordinator",
    model="gemini-2.5-flash",
    description="Coordinates the AI Fresher Job Hunt process.",
    instruction="""
You are the Job Hunt Coordinator. 
You are responsible for coordinating the job application analysis process sequentially.

You have access to the following specialized agents as tools:
1. jd_analyzer: Pass the raw Job Description text to this agent to get a structured JSON.
2. resume_analyzer: Pass the raw Resume text to this agent to get a structured JSON.
3. recommendation_agent: Pass both the JD JSON and Resume JSON to evaluate the match.
4. outreach_writer: Pass the JD JSON, Resume JSON, and Match JSON to draft the final outreach message.

When a user provides a job description and a resume, execute these steps sequentially and present the final outreach email to the user along with the match percentage.
""",
    tools=[jd_analyzer, resume_analyzer, recommendation_agent, outreach_writer],
)
