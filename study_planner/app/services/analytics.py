from collections import defaultdict
from datetime import date, timedelta

from app.services.sessions import get_sessions_for_user


def _week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def compute_analytics(user_id: int) -> dict:
    sessions = get_sessions_for_user(user_id)

    total_minutes = 0
    hours_per_subject: dict[str, float] = defaultdict(float)
    weekly_totals: dict[date, float] = defaultdict(float)

    for session in sessions:
        session_date = date.fromisoformat(session["session_date"])
        minutes = int(session["duration"])
        total_minutes += minutes

        hours = minutes / 60.0
        hours_per_subject[session["subject"]] += hours
        weekly_totals[_week_start(session_date)] += hours

    weekly_list = [
        {"week_start": week, "hours": round(hours, 2)}
        for week, hours in sorted(weekly_totals.items())
    ]

    total_hours = round(total_minutes / 60.0, 2)

    trend = "flat"
    if weekly_list:
        last_week = weekly_list[-1]["hours"]
        prev_week = weekly_list[-2]["hours"] if len(weekly_list) > 1 else 0
        if last_week > prev_week * 1.1:
            trend = "up"
        elif last_week < prev_week * 0.9:
            trend = "down"

    return {
        "total_hours": total_hours,
        "hours_per_subject": {k: round(v, 2) for k, v in hours_per_subject.items()},
        "weekly_totals": weekly_list,
        "trend": trend,
    }
