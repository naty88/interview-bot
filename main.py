import streamlit as st
from PIL import Image
from streamlit_chat import message

from bot_app.job_interview_bot import JobInterviewBot
from utils import generate_uuid

with Image.open("ChatGPT-Logo.png") as img:  # TODO rename
    st.set_page_config(
        page_title="Job Interview Bot",
        page_icon=img,
        layout="centered"
    )

st.title("Job Interview Bot")
st.divider()

greeting_msg = """Hello! I"m your interviewer bot powered by OpenAI.
                \nI will ask you a few questions, and your responses will be evaluated. Let"s get started."""

job_interview_bot = JobInterviewBot()
bot_questions = job_interview_bot.get_questions()

if not st.session_state:
    st.session_state["messages"] = [{"role": "ai", "content": greeting_msg}]
    message(st.session_state["messages"][0].get("content"), avatar_style="lorelei")

    # save generated questions
    st.session_state["questions"] = bot_questions

    # prepare answer list
    st.session_state["answers"] = []

    # set interview step to 0
    st.session_state["interview_step"] = 0


def ask_question() -> None:
    """
    Display the current question.
    """
    question_id, question = st.session_state["questions"][st.session_state["interview_step"]]
    message(question, key=question_id, avatar_style="lorelei")


def get_answer():
    # answer = st.text_input("Your answer:  ", key=f"user_input_{st.session_state['interview_step']}",
    #                        label_visibility="visible", placeholder="Type your answer")

    if answer := st.chat_input(placeholder="Your answer:  ", key=f"user_input_{st.session_state['interview_step']}"):
        st.session_state["answers"].append((answer, generate_uuid()))
        st.session_state['interview_step'] += 1
        st.rerun()
        #
        # # Display user message in chat message container
        # with st.chat_message("user"):
        #     st.markdown(answer)


        print(f"st.session_state AFTER get_answer: {st.session_state}")


def display_past_questions_and_answers() -> None:
    """
    Display all past questions and their corresponding answers.
    """
    for i in range(st.session_state['interview_step']):
        question_id, question = st.session_state['questions'][i]
        message(question, key=question_id, avatar_style="lorelei")

        if i < len(st.session_state['answers']):
            answer_text, answer_key = st.session_state['answers'][i]
            message(answer_text, is_user=True, key=answer_key)

display_past_questions_and_answers()

if st.session_state["interview_step"] < len(st.session_state["questions"]):
    ask_question()
    get_answer()

elif st.session_state['interview_step'] == len(st.session_state['questions']):
    evaluation = job_interview_bot.make_hiring_decision()
    st.write(f"OpenAI GPT-3.5's evaluation: {evaluation}")
    st.session_state['interview_step'] += 1


print(f"ANSWERS: {st.session_state['answers']}")
