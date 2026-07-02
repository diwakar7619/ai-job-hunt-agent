# agents/recommendation.py
from google.adk.agents import Agent

recommendation_agent = Agent(
    name="recommendation_agent",
    model="gemini-2.5-flash",
    description="Compares parsed Job Description and Resume JSONs to evaluate candidate fit.",
    instruction="""
You are an expert ATS (Applicant Tracking System) Recommendation Agent.

When given a Job Description JSON and a Resume JSON, evaluate the match and return ONLY a JSON object in this exact format:

{
  "match_percentage": 0,
  "matching_skills": [],
  "missing_skills": [],
  "recommendation_summary": ""
}

No extra text. No markdown. No explanation. Only the JSON object.
""",
)
