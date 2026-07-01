from google.adk.agents import Agent

outreach_writer = Agent(
    name="outreach_writer",
    model="gemini-2.0-flash-exp",
    description="Writes outreach messages and cover letters.",
)
