import os
import re
from typing import List

from chat_bot.prompts_config import PromptsConfig
from openai import OpenAI
from openai.types.chat import ChatCompletion
from utils import remove_number


class JobInterviewBot:
    """
    Class representing a job interview bot.

    Attributes:
        openai_client (OpenAI): An instance of the OpenAI client.
        prompt (PromptsConfig): An instance of the PromptsConfig class.

    Methods:
        __init__(): Initialize the JobInterviewBot instance.
        generate_questions_output() -> ChatCompletion:
            Generate interview questions based on the job description.
        generate_questions() -> List[tuple]:
            Generate and format interview questions.
        make_hiring_decision(users_answer: List[tuple]) -> str:
            Make a hiring decision based on the user's answers.
    """

    def __init__(self):
        """
        Initialize the JobInterviewBot instance.
        """
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.prompt = PromptsConfig()

    def generate_questions_output(self) -> ChatCompletion:
        """
        Generate interview questions based on the job description.
        Returns:
            ChatCompletion: The completion response containing generated questions.
        """
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": self.prompt.initial_prompt},
                      *[{"role": "user", "content": ""} for i in range(self.prompt.number_of_questions)]],
        )

        return response

    def generate_questions(self) -> List[tuple]:
        """
        Generate and format interview questions.
        Returns:
            List[tuple]: A list of tuples containing question IDs and questions.
        """
        response = self.generate_questions_output()
        content = response.choices[0].message.content

        questions = re.findall(r"\d\..*", content)
        questions = [remove_number(question) for question in questions]
        return [(question_id, question) for question_id, question in enumerate(questions)]

    def make_hiring_decision(self, users_answer: List[tuple]) -> str:
        """
        Make a hiring decision based on the user's answers.
        Args:
            users_answer (List[tuple]): A list of tuples containing question IDs and user answers.
        Returns:
            str: The hiring decision.
        """
        eval_prompt = self.prompt.evaluation_prompt
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": eval_prompt},
                      {"role": "user", "content": " ".join([elem[1] for elem in users_answer])}],
            presence_penalty=0.2,
            temperature=0.1,
        )
        return response.choices[0].message.content
