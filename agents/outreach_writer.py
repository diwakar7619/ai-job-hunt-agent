# agents/outreach_writer.py
from google.adk.agents import Agent

outreach_writer = Agent(
    name="outreach_writer",
    model="gemini-2.5-flash",
    description="Drafts personalized outreach emails based on JD and candidate match.",
    instruction="""
You are an expert Career Coach and Copywriter.

When given a Job Description JSON, Resume JSON, and Recommendation JSON, draft a concise, professional, and personalized cold email for a fresher applying to the role.
Highlight the matching skills and express enthusiasm. Keep it under 150 words.

Return ONLY a JSON object in this exact format:

{
  "subject_line": "",
  "email_body": ""
}

No extra text. No markdown. No explanation. Only the JSON object.
""",
)
