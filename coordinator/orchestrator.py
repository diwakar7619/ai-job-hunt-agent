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

    # --------------------------------------------------------
    # Pipeline
    # --------------------------------------------------------

    def get_pipeline(self):

        return [
            self.jd_analyzer,
            self.resume_analyzer,
            self.recommendation_agent,
            self.outreach_writer,
        ]

    # --------------------------------------------------------
    # JD Analyzer
    # --------------------------------------------------------

    def get_jd_agent(self):

        return self.jd_analyzer
