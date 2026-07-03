# ============================================================
# Imports
# ============================================================

from agents.agent import (
    jd_analyzer,
    resume_analyzer,
    recommendation_agent,
    outreach_writer,
)

# ============================================================
# Job Hunt Orchestrator
# ============================================================


class JobHuntOrchestrator:
    def __init__(self):

        self.jd_analyzer = jd_analyzer
        self.resume_analyzer = resume_analyzer
        self.recommendation_agent = recommendation_agent
        self.outreach_writer = outreach_writer

    # ========================================================
    # Pipeline
    # ========================================================

    def get_pipeline(self):

        return [
            self.jd_analyzer,
            self.resume_analyzer,
            self.recommendation_agent,
            self.outreach_writer,
        ]

    # ========================================================
    # Execute Pipeline (Temporary)
    # ========================================================

    def run(self, job_description: str, resume_text: str):
        """
        Temporary pipeline.

        Right now this prepares the shared payload.

        Next milestone:
        Each ADK agent will enrich this dictionary.
        """

        results = {
            "jd_analysis": {"job_description": job_description},
            "resume_analysis": {"resume_text": resume_text},
            "recommendation": {},
            "outreach": {},
        }

        return results
