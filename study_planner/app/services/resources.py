from app.scraping.client import fetch_html
from app.scraping.providers import PROVIDERS, parse_links
from app.utils.errors import ValidationError


def search_resources(topic: str, limit: int = 12) -> list[dict]:
    if not topic or not topic.strip():
        raise ValidationError("Topic is required for resource search.")

    query = topic.strip()
    results: list[dict] = []

    for provider in PROVIDERS:
        url = provider["build_search_url"](query)
        html = fetch_html(url)
        if not html:
            continue

        links = parse_links(html, provider)
        for link in links:
            results.append(link)
            if len(results) >= limit:
                return results

    return results
