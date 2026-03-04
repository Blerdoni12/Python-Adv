import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

st.title("📚 Study Planner System")

api_key_input = st.text_input("Enter API Key", type="password")



def validate_api_key(api_key):
    headers = {"api-key": api_key}
    response = requests.get(f"{BASE_URL}/api/validate_key/", headers=headers)
    return response.status_code == 200



def get_users():
    response = requests.get(f"{BASE_URL}/api/users/")
    if response.status_code == 200:
        return response.json()
    return []


def add_user(api_key, name, email):
    headers = {"api-key": api_key}
    response = requests.post(
        f"{BASE_URL}/api/users/",
        params={"name": name, "email": email},
        headers=headers
    )
    return response



def get_plans():
    response = requests.get(f"{BASE_URL}/api/plans/")
    if response.status_code == 200:
        return response.json()
    return []


def add_plan(api_key, subject, study_date, user_id):
    headers = {"api-key": api_key}
    response = requests.post(
        f"{BASE_URL}/api/plans/",
        params={
            "subject": subject,
            "study_date": study_date,
            "user_id": user_id
        },
        headers=headers
    )
    return response



def users_dashboard(api_key):
    st.header("👤 Users Management")

    users = get_users()
    df = pd.DataFrame(users)
    st.dataframe(df, use_container_width=True)

    st.subheader("Add User")
    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Add User"):
        if name.strip() and email.strip():
            response = add_user(api_key, name, email)
            if response.status_code == 200:
                st.success("User added successfully")
                st.rerun()
            else:
                st.error(response.json())
        else:
            st.error("All fields required")



def plans_dashboard(api_key):
    st.header("📖 Study Plans")

    users = get_users()
    plans = get_plans()

    if not users:
        st.warning("Create a user first.")
        return

    user_map = {u["id"]: u["name"] for u in users}

    for plan in plans:
        plan["user"] = user_map.get(plan["user_id"], "Unknown")

    df = pd.DataFrame(plans)
    st.dataframe(df, use_container_width=True)

    st.subheader("Add Study Plan")

    subject = st.text_input("Subject")
    study_date = st.date_input("Study Date")
    selected_user = st.selectbox(
        "User",
        users,
        format_func=lambda x: x["name"]
    )

    if st.button("Add Plan"):
        if subject.strip():
            response = add_plan(
                api_key,
                subject,
                study_date,
                selected_user["id"]
            )
            if response.status_code == 200:
                st.success("Study plan added")
                st.rerun()
            else:
                st.error(response.json())
        else:
            st.error("Subject required")



def visualization_dashboard():
    st.header("📊 Study Analytics")

    plans = get_plans()

    if not plans:
        st.warning("No plans available")
        return

    df = pd.DataFrame(plans)

    plans_by_date = df.groupby("study_date").size().reset_index(name="Count")

    fig = px.bar(
        plans_by_date,
        x="study_date",
        y="Count",
        title="Plans by Study Date"
    )

    st.plotly_chart(fig, use_container_width=True)



st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Choose a dashboard",
    ["Users", "Study Plans", "Analytics"]
)

if api_key_input and validate_api_key(api_key_input):
    if option == "Users":
        users_dashboard(api_key_input)
    elif option == "Study Plans":
        plans_dashboard(api_key_input)
    elif option == "Analytics":
        visualization_dashboard()
else:
    st.warning("Enter valid API key to continue.")