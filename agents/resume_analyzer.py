from google.adk.agents import Agent

resume_analyzer = Agent(
    name="resume_analyzer",
    model="gemini-2.0-flash-exp",
    description="Compares resume with JD.",
)
