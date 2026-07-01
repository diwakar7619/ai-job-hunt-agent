from google.adk.agents import Agent

jd_analyzer = Agent(
    name="jd_analyzer",
    model="gemini-2.0-flash-exp",
    description="Analyzes a job description and extracts key information.",
    instruction="""
You are a Job Description Analyzer.

When given a job description:

1. Identify the job title.
2. Extract all required technical skills.
3. Extract preferred skills.
4. Summarize the role in 3-4 sentences.
5. Return the response in clean Markdown.
""",
)
