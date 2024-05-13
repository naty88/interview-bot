import os
import re
from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletion

from chat_bot.promts_congig import PromtsConfig
from utils import remove_number


class JobInterviewBot:

    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.promt = PromtsConfig()

    def generate_questions_output(self) -> ChatCompletion:
        # Generate interview questions based on the job description
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.promt.initial_promt},
                *[{"role": "user", "content": ""} for i in range(self.promt.number_of_questions)]
            ],
        )
        return response

    def generate_questions(self) -> List[tuple]:
        response = self.generate_questions_output()
        content = response.choices[0].message.content

        questions = re.findall(r"\d\..*", content)
        questions = [remove_number(question) for question in questions]
        return [(question_id, question) for question_id, question in enumerate(questions)]

    def make_hiring_decision(self, users_answer: List[tuple]) -> str:
        eval_prompt = self.promt.evaluation_promt
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": eval_prompt},
                {"role": "user", "content": " ".join([elem[1] for elem in users_answer])}
            ],
            presence_penalty=0.2,
            temperature=0.1
        )
        return response.choices[0].message.content
