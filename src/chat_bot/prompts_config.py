from pydantic import BaseModel


class PromptsConfig(BaseModel):
    number_of_questions: int = 3
    prompt_language: str = "English"
    job_description_prompt: str = """The job description for the advertised position as OpenAI Technical Expert / Data Scientist:
                TASKS
                Development and implementation of machine learning / AI models for applications, e.g., in the area of Natural Language Processing (NLP) or Computer Vision, with a focus on OpenAI technologies (LLM).
                Close collaboration with other data scientists and our business units, subject matter experts, internal and external service providers.
                Case-based assessment and consultation on the use of analytical methods and approaches (especially OpenAI technologies) to improve our processes and services.
                Support of business units as an internal development partner, from ideation to implementation.
                QUALIFICATIONS
                Completed master's degree in computer science, mathematics, physics, or a comparable qualification with a focus on machine learning / artificial intelligence.
                Three years of experience in implementing machine learning / AI models, including the use of OpenAI technologies.
                Deep expertise in current methods in the field of ML and AI, especially Large Language Models.
                Experience with cloud computing platforms, specifically Azure. Comprehensive knowledge of relevant programming languages, including Python. Good knowledge in NLP and/or Computer Vision.
                Strong analytical skills and the ability to solve complex problems.
                Excellent written and verbal communication skills in German and English.
                """
    initial_prompt: str = f"""Job description: {job_description_prompt}.
                Generate {number_of_questions} unique and relevant interview questions for a candidate applying for this position. 
                Ensure the questions assess various aspects of the candidate's suitability for the position, such as skills, experience, and fit for the company culture.
                The questions should be formulated in {prompt_language} language and should start with a number like in the example:
                1. <Question> 
                """
    evaluation_prompt: str = f"""Job description: {job_description_prompt}.
                Assess a candidate's answers for this position. Evaluate the quality and depth of the candidate's answers
                and make a clear hiring decision based on the candidate's answers. Please ensure that your evaluation considers the candidate's expertise,
                problem-solving skills, technical knowledge, and communication abilities. Your decision should be well-supported
                and consider the candidate's potential contributions to the role. Provide the evaluation and decision in {prompt_language} language.
                """
