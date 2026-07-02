# agents/resume_analyzer.py
from google.adk.agents import Agent

resume_analyzer = Agent(
    name="resume_analyzer",
    model="gemini-2.5-flash",
    description="Analyzes applicant resumes for fresher applications.",
    instruction="""
You are an expert Resume Analyzer.

When given a resume text, extract and return ONLY a JSON object in this exact format:

{
  "name": "",
  "education": [],
  "skills": [],
  "projects": [],
  "experience": []
}

No extra text. No markdown. No explanation. Only the JSON object.
""",
)
