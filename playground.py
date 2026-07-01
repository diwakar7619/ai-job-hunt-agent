import asyncio
import os

from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from agents.jd_analyzer import jd_analyzer

load_dotenv()

APP_NAME = "job_hunt_agent"
USER_ID = "pratham"
SESSION_ID = "session_001"

session_service = InMemorySessionService()
