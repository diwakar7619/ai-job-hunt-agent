from google.adk.agents import LlmAgent

jd_analyzer_agent = LlmAgent(
    name="jd_analyzer",
    model="gemini-2.0-flash",
    instruction=""" You are an expert technical recruiter.

                    Your job is to analyze a Job Description.

                    Extract:
                    - Job Title
                    - Required Skills
                    - Preferred Skills
                    - Experience Required
                    - Education Required
                    - Job Responsibilities

                    Return the information in a clean, structured format.
                    """,
)
