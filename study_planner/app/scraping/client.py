from urllib import request


def fetch_html(url: str, timeout: int = 10) -> str:
    req = request.Request(
        url,
        headers={
            "User-Agent": "StudyPlannerBot/1.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""
