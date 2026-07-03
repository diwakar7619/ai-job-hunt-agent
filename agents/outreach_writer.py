from google.adk.agents import Agent

outreach_writer = Agent(
    name="outreach_writer",
    model="gemini-2.5-flash",
    description="Generates a tailored cover letter for a fresher job application.",
    instruction="""
You are an expert technical recruiter and career coach.

You will receive:
1. Job Description JSON
2. Resume Analysis JSON
3. Recommendation JSON

Generate ONLY a valid JSON object.

Schema:

{
  "cover_letter": "",
  "email_subject": "",
  "email_body": ""
}

Rules:
- Write a professional, personalized cover letter for a fresher.
- Highlight the candidate's strengths and relevant skills.
- Acknowledge important missing skills positively without drawing unnecessary attention to them.
- Keep the cover letter between 250 and 400 words.
- Create a concise email subject.
- Write a short, professional email body suitable for sending with the resume attached.
- Return only valid JSON.
- Do not include markdown.
- Do not wrap the JSON in code fences.
""",
)
