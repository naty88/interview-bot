import os
import re

from openai import OpenAI

from bot_app.promts_congig import PromtsConfig

# TODO logging

class JobInterviewBot:

    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.promt = PromtsConfig()
        self.nmb_of_questions = 3
        self.user_answers = []

    def generate_questions_output(self):
        # Generate interview questions based on the job description
        initial_promt = f"Generate {self.nmb_of_questions} interview questions for a candidate applying for {self.promt.job_description_promt}."
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": initial_promt},
                *[{"role": "user", "content": ""} for i in range(self.nmb_of_questions)]
            ]
        )
        return response

    def get_questions(self):  # TODO: check type openai.types.chat.chat_completion.ChatCompletion
        response = self.generate_questions_output()
        content = response.choices[0].message.content
        # print(f"content: {content}")

        questions = re.findall(r"\d\..*", content)
        if len(questions) == self.nmb_of_questions:
            return [(question_id, question) for question_id, question in enumerate(questions)]
        else:
            print("Questions were not parsed correctly.")
            print(f"questions: {questions}")


    # def conduct_interview(self):
    #     # Conduct the interview
    #     questions = self.get_questions()
    #     print("Welcome to the interview!")
    #     print("Please answer the following questions with a maximum of 20 words each:")
    #     for i, question in enumerate(questions, 1):
    #         print(f"Question {i}: {question}")
    #         answer = input("Your answer: ")
    #         self.user_answers.append(answer)
    #
    #     print("\nThank you for your answers. We will now evaluate your suitability for the position.")

    def make_hiring_decision(self):
        # Make the hiring decision
        eval_prompt = self.promt.evaluation_promt
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": eval_prompt},
                {"role": "user", "content": " ".join(self.user_answers)}
            ],
            presence_penalty=0.2,
            temperature=0.1
        )
        return response
