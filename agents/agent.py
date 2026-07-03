from .jd_analyzer import jd_analyzer
from .resume_analyzer import resume_analyzer
from .recommendation import recommendation_agent
from .outreach_writer import outreach_writer

AVAILABLE_AGENTS = {
    "jd_analyzer": jd_analyzer,
    "resume_analyzer": resume_analyzer,
    "recommendation_agent": recommendation_agent,
    "outreach_writer": outreach_writer,
}

# Temporary root agent for testing.
# The coordinator will orchestrate all agents later.
root_agent = jd_analyzer
