import json
import os
from datetime import date
from urllib import error, parse, request

import streamlit as st


def load_env(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError:
        return


load_env()
API_BASE_URL = os.getenv("API_BASE_URL", os.getenv("BASE_URL", "http://127.0.0.1:8000"))

import matplotlib.pyplot as plt


def api_request(method: str, path: str, data: dict | None = None, token: str | None = None, params: dict | None = None):
    url = API_BASE_URL.rstrip("/") + path
    if params:
        url = f"{url}?{parse.urlencode(params)}"

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = json.dumps(data).encode("utf-8") if data else None
    req = request.Request(url, data=payload, headers=headers, method=method)

    try:
        with request.urlopen(req, timeout=10) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else None
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            return exc.code, json.loads(body)
        except json.JSONDecodeError:
            return exc.code, {"detail": body}
    except error.URLError as exc:
        return 0, {"detail": str(exc)}


def error_detail(data: object, fallback: str) -> str:
    if isinstance(data, dict):
        return data.get("detail", fallback)
    return fallback


st.set_page_config(page_title="Study Planner", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None

st.title("Study Planner System")


def render_auth():
    st.subheader("Login")
    login_user = st.text_input("Username or Email", key="login_user")
    login_pass = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        status, data = api_request(
            "POST",
            "/login",
            data={"username_or_email": login_user, "password": login_pass},
        )
        if status == 200:
            st.session_state.token = data["access_token"]
            st.success("Logged in successfully.")
            st.rerun()
        else:
            st.error(error_detail(data, "Login failed."))

    st.divider()
    st.subheader("Register")
    reg_user = st.text_input("Username", key="reg_user")
    reg_email = st.text_input("Email", key="reg_email")
    reg_pass = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Create Account"):
        status, data = api_request(
            "POST",
            "/register",
            data={"username": reg_user, "email": reg_email, "password": reg_pass},
        )
        if status == 200:
            st.success("Account created. Please log in.")
        else:
            st.error(error_detail(data, "Registration failed."))


def render_dashboard():
    st.subheader("Overview")
    status, data = api_request("GET", "/analytics", token=st.session_state.token)
    if status != 200:
        st.error(error_detail(data, "Unable to load analytics."))
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Hours", data.get("total_hours", 0))
    col2.metric("Subjects", len(data.get("hours_per_subject", {})))
    col3.metric("Trend", data.get("trend", "flat"))

    rec_status, rec_data = api_request("GET", "/recommendations", token=st.session_state.token)
    if rec_status == 200:
        st.subheader("Recommendations")
        for rec in rec_data.get("recommendations", []):
            st.write(f"{rec['title']}: {rec['message']}")


def render_plans():
    st.subheader("Study Plans")
    status, plans = api_request("GET", "/plans", token=st.session_state.token)
    plans_list = plans if status == 200 and isinstance(plans, list) else []
    if status == 200:
        st.dataframe(plans_list, use_container_width=True)
    else:
        st.error(error_detail(plans, "Unable to load plans."))

    st.divider()
    st.subheader("Add Plan")
    subject = st.text_input("Subject")
    deadline = st.date_input("Deadline", value=date.today())
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
    estimated_hours = st.number_input("Estimated Hours", min_value=1.0, step=0.5)
    status_value = st.selectbox("Status", ["pending", "in_progress", "completed"], index=0)

    if st.button("Create Plan"):
        status, data = api_request(
            "POST",
            "/plans",
            token=st.session_state.token,
            data={
                "subject": subject,
                "deadline": deadline.isoformat(),
                "priority": priority,
                "estimated_hours": float(estimated_hours),
                "status": status_value,
            },
        )
        if status == 200:
            st.success("Plan created.")
            st.rerun()
        else:
            st.error(error_detail(data, "Failed to create plan."))

    if plans_list:
        st.divider()
        st.subheader("Update or Delete Plan")
        plan_ids = [plan["id"] for plan in plans_list]
        selected_id = st.selectbox("Plan ID", plan_ids)
        selected_plan = next((plan for plan in plans_list if plan["id"] == selected_id), None)
        if selected_plan:
            edit_subject = st.text_input("Edit Subject", value=selected_plan["subject"], key="edit_subject")
            edit_deadline = st.date_input("Edit Deadline", value=date.fromisoformat(selected_plan["deadline"]), key="edit_deadline")
            edit_priority = st.selectbox("Edit Priority", ["low", "medium", "high"], index=["low", "medium", "high"].index(selected_plan["priority"]), key="edit_priority")
            edit_hours = st.number_input("Edit Estimated Hours", min_value=1.0, step=0.5, value=float(selected_plan["estimated_hours"]), key="edit_hours")
            edit_status = st.selectbox("Edit Status", ["pending", "in_progress", "completed"], index=["pending", "in_progress", "completed"].index(selected_plan["status"]), key="edit_status")

            col_a, col_b = st.columns(2)
            if col_a.button("Update Plan"):
                status, data = api_request(
                    "PUT",
                    f"/plans/{selected_id}",
                    token=st.session_state.token,
                    data={
                        "subject": edit_subject,
                        "deadline": edit_deadline.isoformat(),
                        "priority": edit_priority,
                        "estimated_hours": float(edit_hours),
                        "status": edit_status,
                    },
                )
                if status == 200:
                    st.success("Plan updated.")
                    st.rerun()
                else:
                    st.error(error_detail(data, "Failed to update plan."))

            if col_b.button("Delete Plan"):
                status, data = api_request(
                    "DELETE",
                    f"/plans/{selected_id}",
                    token=st.session_state.token,
                )
                if status == 200:
                    st.success("Plan deleted.")
                    st.rerun()
                else:
                    st.error(error_detail(data, "Failed to delete plan."))


def render_sessions():
    st.subheader("Study Sessions")
    status, sessions = api_request("GET", "/sessions", token=st.session_state.token)
    sessions_list = sessions if status == 200 and isinstance(sessions, list) else []
    if status == 200:
        st.dataframe(sessions_list, use_container_width=True)
    else:
        st.error(error_detail(sessions, "Unable to load sessions."))

    st.divider()
    st.subheader("Log Session")
    subject = st.text_input("Session Subject")
    duration = st.number_input("Duration (minutes)", min_value=5, step=5)
    notes = st.text_area("Notes", max_chars=500)
    session_date = st.date_input("Session Date", value=date.today(), key="session_date")

    if st.button("Add Session"):
        status, data = api_request(
            "POST",
            "/sessions",
            token=st.session_state.token,
            data={
                "subject": subject,
                "duration": int(duration),
                "notes": notes or None,
                "session_date": session_date.isoformat(),
            },
        )
        if status == 200:
            st.success("Session logged.")
            st.rerun()
        else:
            st.error(error_detail(data, "Failed to log session."))


def render_analytics():
    st.subheader("Analytics")
    status, data = api_request("GET", "/analytics", token=st.session_state.token)
    if status != 200:
        st.error(error_detail(data, "Unable to load analytics."))
        return

    hours_by_subject = data.get("hours_per_subject", {})
    if hours_by_subject:
        fig, ax = plt.subplots()
        ax.bar(hours_by_subject.keys(), hours_by_subject.values(), color="#4C78A8")
        ax.set_title("Study Hours per Subject")
        ax.set_ylabel("Hours")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)

    weekly = data.get("weekly_totals", [])
    if weekly:
        weeks = [item["week_start"] for item in weekly]
        hours = [item["hours"] for item in weekly]
        fig2, ax2 = plt.subplots()
        ax2.plot(weeks, hours, marker="o", color="#F58518")
        ax2.set_title("Weekly Study Time")
        ax2.set_ylabel("Hours")
        ax2.tick_params(axis="x", rotation=45)
        st.pyplot(fig2)


def render_resources():
    st.subheader("Resource Finder")
    topic = st.text_input("Topic")
    if st.button("Search Resources"):
        status, data = api_request(
            "GET",
            "/resources",
            token=st.session_state.token,
            params={"topic": topic},
        )
        if status == 200:
            results = data.get("results", [])
            if results:
                for item in results:
                    st.write(f"{item['title']} ({item['source']})")
                    st.write(item["url"])
            else:
                st.info("No resources found.")
        else:
            st.error(error_detail(data, "Search failed."))


if st.session_state.token:
    st.sidebar.success("Authenticated")
    page = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "Study Plans", "Study Sessions", "Analytics", "Resource Finder"],
    )
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.rerun()

    if page == "Dashboard":
        render_dashboard()
    elif page == "Study Plans":
        render_plans()
    elif page == "Study Sessions":
        render_sessions()
    elif page == "Analytics":
        render_analytics()
    elif page == "Resource Finder":
        render_resources()
else:
    render_auth()
