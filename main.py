import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import re

st.set_page_config(page_title="Workout Planner")
st.title("Workout Planner")

openai_api_key = st.sidebar.text_input("OpenAI API Key:", type="password")


def escape_str(text):
    return re.sub(r":([a-zA-Z])", r"\:\1", text).replace("$", "dollars")


def generate_workout_plan(
    age,
    weight,
    height,
    body_type,
    workout_goals,
    days_per_week,
    workout_schedule,
    body_goal,
):
    llm = OpenAI(openai_api_key=openai_api_key)

    template = PromptTemplate(
        input_variables=[
            "age",
            "weight",
            "height",
            "body_type",
            "workout_goals",
            "days_per_week",
            "workout_schedule",
            "body_goal",
        ],
        template="Generate a workout plan and diet recommendations for a {body_type} {body_goal} individual with age {age}, weight {weight} kg, height {height} cm, workout goals {workout_goals}, workout schedule {workout_schedule}, and {days_per_week} days per week. Use the markdown formatting to make the output more readable. Add google search url as a markdown link for each exercises so the user can learn how to do the exercise.",
    )
    prompt = template.format(
        age=age,
        weight=weight,
        height=height,
        body_type=body_type,
        workout_goals=workout_goals,
        days_per_week=days_per_week,
        workout_schedule=workout_schedule,
        body_goal=body_goal,
    )

    response = llm(prompt, max_tokens=3700, temperature=0.7)

    return response


with st.form("myform"):
    st.header("Personal Information")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    weight = st.number_input("Weight (kg)", min_value=0.0, max_value=200.0, step=0.1)
    height = st.number_input("Height (cm)", min_value=0.0, max_value=230.0, step=0.1)
    body_type = st.selectbox("Body Type", ["Endomorph", "Mesomorph", "Ectomorph"])

    st.header("Workout Goals")
    workout_goals = st.multiselect(
        "Select Workout Goals", ["Weight Loss", "Muscle Gain", "Strength", "Endurance"]
    )

    st.header("Schedule")
    days_per_week = st.number_input("Days per Week", min_value=1, max_value=7, step=1)
    workout_schedule = st.multiselect(
        "Preferred Workout Days",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    )

    st.header("Body Goals")
    body_goal = st.radio("Body Goal", ["Lose Fat", "Maintain Weight", "Build Muscle"])

    submitted = st.form_submit_button("Generate Plan")

    if submitted and openai_api_key:
        response = generate_workout_plan(
            age,
            weight,
            height,
            body_type,
            workout_goals,
            days_per_week,
            workout_schedule,
            body_goal,
        )

        st.markdown(escape_str(response))

    elif not openai_api_key:
        st.warning("No OpenAI API Key detected!", icon="⚠")
