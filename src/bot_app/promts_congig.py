from pydantic import BaseModel


class PromtsConfig(BaseModel):
    number_of_questions: int = 3
    promt_language: str = "English"
    job_description_promt: str = """Job description of advertised OpenAI Technical Expert / Data Scientist position:
            TASKS:
            Development and implementation of Machine Learning / Artificial Intelligence models for applications, e.g. in the area of Natural Language Processing or Computer Vision, with a focus on OpenAI technologies to improve our services and processes
            Collaborate closely with other Data Scientists, subject matter experts, and external service providers
            Use case-based evaluation and consulting on the use of analytical methods and approaches (especially OpenAI technologies) to improve our processes and services
            Collaborate closely with our business units as an internal development partner, supporting them from the ideation phase to implementation
            QUALIFICATIONS:
            Master in computer science, mathematics, physics or a comparable qualification with a focus on Machine Learning / AI.
            At least three years of experience in implementing Machine Learning / AI models, including the use of OpenAI technologies
            In-depth expertise in the area of current Machine Learning / AI methods, especially Large Language Models
            Comprehensive knowledge of relevant programming languages, including Python
            Experience with cloud computing platforms, preferably Azure
            Knowledge of natural language processing and/or computer vision
            Strong analytical skills and the ability to solve complex problems
            Strong English communication skills are required, and basic knowledge of German is preferred.
            """
    initial_promt: str = f"""Job description: {job_description_promt}.
                        Generate {number_of_questions} unique and relevant interview questions for a candidate applying for this position. 
                        Ensure the questions assess various aspects of the candidate's suitability for the position, such as skills, experience, and fit for the company culture.
                        The questions should be formulated in {promt_language} language."""
    evaluation_promt: str = f"""Job description: {job_description_promt}.
                As an AI interview assistant, your task is to assess a candidate's answers for this position.
                Evaluate the quality and depth of the candidate's answers and make a clear hiring decision based on the candidate's performance.
                Please ensure that your evaluation considers the candidate's expertise, problem-solving skills, technical knowledge, and communication abilities..
                Your decision should be well-supported and consider the candidate's potential contributions to the role.
                """
