# agents/recommendation.py
from google.adk.agents import Agent

recommendation_agent = Agent(
    name="recommendation_agent",
    model="gemini-2.5-flash",
    description="Compares JD and Resume to evaluate fit.",
    instruction="""
You are an expert ATS Recommendation Agent.

Given a Job Description JSON and Resume JSON, return ONLY this JSON:

{
  "match_percentage": 0,
  "matching_skills": [],
  "missing_skills": [],
  "recommendation_summary": "2-3 sentences: is candidate suitable, what to upskill, apply or not"
}

recommendation_summary must include:
- Suitability verdict (strong/partial/weak fit)
- Top 2 skills to upskill immediately
- Whether to apply now or after upskilling

No extra text. No markdown. Only JSON.
""",
)
