import os
from dotenv import load_dotenv

load_dotenv()

print("API Key found:", bool(os.getenv("GOOGLE_API_KEY")))

from agents.jd_analyzer import jd_analyzer_agent

print("Agent name:", jd_analyzer_agent.name)
print("Agent model:", jd_analyzer_agent.model)
