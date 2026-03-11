from collections import defaultdict
from datetime import date

from app.services.plans import get_plans_for_user
from app.services.sessions import get_sessions_for_user


def get_recommendations(user_id: int) -> list[dict]:
    plans = get_plans_for_user(user_id)
    sessions = get_sessions_for_user(user_id)
    today = date.today()

    recommendations: list[dict] = []
    studied_subjects = {session["subject"] for session in sessions}

    open_plans = [plan for plan in plans if plan["status"] != "completed"]
    if open_plans:
        nearest = min(open_plans, key=lambda p: p["deadline"])
        days_left = (date.fromisoformat(nearest["deadline"]) - today).days
        if days_left <= 7:
            recommendations.append(
                {
                    "title": "Deadline approaching",
                    "message": f"{nearest['subject']} is due in {max(days_left, 0)} days. Consider focusing on it.",
                }
            )

    studied_hours = defaultdict(float)
    for session in sessions:
        studied_hours[session["subject"]] += int(session["duration"]) / 60.0

    if open_plans:
        remaining_by_subject = {}
        for plan in open_plans:
            subject = plan["subject"]
            remaining = float(plan["estimated_hours"]) - studied_hours.get(subject, 0.0)
            remaining_by_subject[subject] = remaining

        if remaining_by_subject:
            target_subject = max(remaining_by_subject, key=remaining_by_subject.get)
            recommendations.append(
                {
                    "title": "Focus suggestion",
                    "message": f"Allocate time to {target_subject} to close remaining study hours.",
                }
            )

        unstarted = [plan["subject"] for plan in open_plans if plan["subject"] not in studied_subjects]
        if unstarted:
            recommendations.append(
                {
                    "title": "Start new subject",
                    "message": f"Consider starting: {', '.join(unstarted[:3])}.",
                }
            )

    if sessions:
        last_session_date = max(date.fromisoformat(s["session_date"]) for s in sessions)
        days_since = (today - last_session_date).days
        if days_since >= 7:
            recommendations.append(
                {
                    "title": "Consistency reminder",
                    "message": f"It has been {days_since} days since your last study session. Plan a short session today.",
                }
            )
    else:
        recommendations.append(
            {
                "title": "Get started",
                "message": "Log your first study session to unlock analytics and suggestions.",
            }
        )

    if not recommendations:
        recommendations.append(
            {
                "title": "On track",
                "message": "Your study plan looks balanced. Keep up the steady progress.",
            }
        )

    return recommendations
