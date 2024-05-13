import time
from typing import List

import streamlit as st
from streamlit_chat import message

from bot_app.job_interview_bot import JobInterviewBot
from utils import generate_uuid

st.set_page_config(
    page_title="Job Interview Bot",
    layout="centered"
)

st.title("Job Interview Bot")
st.divider()


def initialize_session(greeting_msg: str, bot_questions: List[str]):
    if not st.session_state:
        st.session_state["messages"] = [{"role": "ai", "content": greeting_msg}]
        message(st.session_state["messages"][0].get("content"), avatar_style="lorelei-neutral")

        # save generated questions
        st.session_state["questions"] = bot_questions

        # prepare answer list
        st.session_state["answers"] = []

        # set interview step to 0
        st.session_state["interview_step"] = 0

    time.sleep(2)


def ask_question() -> None:
    """
    Display the current question.
    """
    question_id, question = st.session_state["questions"][st.session_state["interview_step"]]
    message(question, key=question_id, avatar_style="lorelei-neutral")


def get_answer() -> None:
    if answer := st.chat_input(placeholder="Your answer:  ", key=f"user_input_{st.session_state['interview_step']}"):
        st.session_state["answers"].append((generate_uuid(), answer))
        st.session_state['interview_step'] += 1
        st.rerun()


def display_past_questions_and_answers() -> None:
    """
    Display all past questions and their corresponding answers.
    """
    for i in range(st.session_state['interview_step']):
        question_id, question = st.session_state['questions'][i]
        message(question, key=question_id, avatar_style="lorelei-neutral")

        if i < len(st.session_state.answers):
            answer_key, answer_text = st.session_state['answers'][i]
            message(answer_text, is_user=True, key=answer_key, avatar_style="miniavs")  # miniavs


def start_interview_process(job_interview_bot: JobInterviewBot) -> None:
    greeting_msg = f"""Hello! I"m your interviewer bot powered by OpenAI.
                    \nI will ask you a few questions, and your responses will be evaluated. Let"s get started.
                     The questions for the interview will be in the {job_interview_bot.promt.promt_language} language."""

    bot_questions = job_interview_bot.generate_questions()

    initialize_session(greeting_msg, bot_questions)

    display_past_questions_and_answers()

    if st.session_state["interview_step"] < len(st.session_state["questions"]):
        ask_question()
        get_answer()

    elif st.session_state.interview_step == len(st.session_state.questions):
        message("Thank you for your answers. We will now evaluate your suitability for the position...",
                avatar_style="lorelei-neutral")
        decision = job_interview_bot.make_hiring_decision(st.session_state.answers)
        message(decision, avatar_style="lorelei-neutral")
        st.session_state.interview_step += 1


def execute_chat_bot() -> None:
    job_interview_bot = JobInterviewBot()
    start_interview_process(job_interview_bot)


if __name__ == "__main__":
    execute_chat_bot()
