from dotenv import load_dotenv

load_dotenv()

from agents.jd_analyzer import jd_analyzer
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

APP_NAME = "job_hunt_agent"
USER_ID = "pratham"
SESSION_ID = "session_001"

session_service = InMemorySessionService()

session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
)

runner = Runner(
    agent=jd_analyzer,
    app_name=APP_NAME,
    session_service=session_service,
)
