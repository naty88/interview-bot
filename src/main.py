from typing import List

import streamlit as st
from streamlit_chat import message

from chat_bot.job_interview_bot import JobInterviewBot
from utils import generate_uuid

st.set_page_config(page_title="Job Interview Bot", layout="centered")

st.title("Job Interview Bot")
st.divider()


def initialize_session(greeting_msg: str, bot_questions: List[str]):
    """
    Initialize the session state with a greeting message and a list of bot questions.
    Args:
        greeting_msg (str): The greeting message displayed to the user at the start of the interview.
        bot_questions (List[str]): List of questions to be asked during the interview.
    """
    if not st.session_state:
        return st.session_state.update({"messages": [{"role": "ai", "greeting": greeting_msg}], "questions": bot_questions, "answers": [], "interview_step": 0})


def ask_question() -> None:
    """
    Display the current question to the user.
    """
    question_id, question = st.session_state["questions"][st.session_state["interview_step"]]
    message(question, key=question_id, avatar_style="lorelei-neutral")


def get_answer() -> None:
    """
    Get the user's answer to the current question and store it in the session state.
    """
    if answer := st.chat_input(placeholder="Your answer: "):
        st.session_state["answers"].append((generate_uuid(), answer))
        st.session_state["interview_step"] += 1
        st.rerun()


def display_past_questions_and_answers() -> None:
    """
    Display all past questions and their corresponding answers.
    This function iterates through the past questions and their answers stored in the session state,
    displaying them in the chat interface.
    """
    message(st.session_state.messages[0]["greeting"], avatar_style="lorelei-neutral")

    for i in range(st.session_state["interview_step"]):
        question_id, question = st.session_state["questions"][i]
        message(question, key=question_id, avatar_style="lorelei-neutral")

        if i < len(st.session_state.answers):
            answer_key, answer_text = st.session_state["answers"][i]
            message(answer_text, is_user=True, key=answer_key, avatar_style="miniavs")


def start_interview_process(job_interview_bot: JobInterviewBot) -> None:
    """
    Start the interview process by initializing the session, displaying past questions and answers,
    asking questions, getting answers, and evaluating the candidate.
    Args:
        job_interview_bot (JobInterviewBot): An instance of the JobInterviewBot class.
    """
    greeting_msg = f"""Hello! I'm your interviewer bot powered by OpenAI.
                I will ask you a few questions, and your responses will be evaluated.
                The interview questions will be formulated in {job_interview_bot.prompt.prompt_language} language.
                Let's get started. Good luck!
                """
    if "questions" not in st.session_state:
        bot_questions = job_interview_bot.generate_questions()
    else:
        bot_questions = st.session_state.questions

    initialize_session(greeting_msg, bot_questions)

    display_past_questions_and_answers()

    if st.session_state["interview_step"] < len(st.session_state["questions"]):
        ask_question()
        get_answer()

    elif st.session_state.interview_step == len(st.session_state.questions):
        evaluate_candidate(job_interview_bot)


def evaluate_candidate(job_interview_bot: JobInterviewBot) -> None:
    """
    Evaluate the candidate's answers and make a hiring decision based on the job interview bot's criteria.
    Args:
        job_interview_bot (JobInterviewBot): An instance of the JobInterviewBot class.
    """
    message("Thank you for your answers. We will now evaluate your suitability for the position...", avatar_style="lorelei-neutral")
    decision = job_interview_bot.make_hiring_decision(st.session_state["answers"])
    message(decision, avatar_style="lorelei-neutral")
    st.session_state["interview_step"] += 1


def execute_chat_bot() -> None:
    """
    Execute the job interview bot.
    """
    job_interview_bot = JobInterviewBot()
    start_interview_process(job_interview_bot)


if __name__ == "__main__":
    execute_chat_bot()
