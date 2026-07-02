from google.adk.agents import Agent

jd_analyzer = Agent(
    name="jd_analyzer",
    model="gemini-2.5-flash",
    description="Analyzes job descriptions for fresher applications.",
    instruction="""
You are an expert Job Description Analyzer.

When given a job description, return a structured analysis.

Extract:

- Job Title
- Required Technical Skills
- Preferred Skills
- Experience Required
- Responsibilities
- Short Summary

Be accurate and concise.
""",
)
