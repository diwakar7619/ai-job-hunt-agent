from agents.agent import (
    jd_analyzer,
    resume_analyzer,
    recommendation_agent,
    outreach_writer,
)


class JobHuntOrchestrator:
    """
    Temporary orchestrator.

    The execution logic will be connected to ADK Runner
    after all components are in place.
    """

    def __init__(self):
        self.jd_analyzer = jd_analyzer
        self.resume_analyzer = resume_analyzer
        self.recommendation_agent = recommendation_agent
        self.outreach_writer = outreach_writer

    def get_pipeline(self):
        return [
            self.jd_analyzer,
            self.resume_analyzer,
            self.recommendation_agent,
            self.outreach_writer,
        ]
