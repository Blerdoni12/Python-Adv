from html.parser import HTMLParser
from urllib.parse import quote_plus, urljoin, urlparse


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._current_href: str | None = None
        self._current_text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = None
        for key, value in attrs:
            if key == "href":
                href = value
                break
        if href:
            self._current_href = href
            self._current_text_parts = []

    def handle_data(self, data: str) -> None:
        if self._current_href is not None:
            self._current_text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._current_href:
            text = " ".join(part.strip() for part in self._current_text_parts).strip()
            self.links.append((self._current_href, text))
            self._current_href = None
            self._current_text_parts = []


def _gfg_search(query: str) -> str:
    return f"https://www.geeksforgeeks.org/?s={quote_plus(query)}"


def _tpoint_search(query: str) -> str:
    return f"https://www.tutorialspoint.com/search?search={quote_plus(query)}"


PROVIDERS = [
    {
        "name": "GeeksforGeeks",
        "base_url": "https://www.geeksforgeeks.org",
        "allowed_domains": ["geeksforgeeks.org"],
        "build_search_url": _gfg_search,
        "max_results": 6,
    },
    {
        "name": "TutorialsPoint",
        "base_url": "https://www.tutorialspoint.com",
        "allowed_domains": ["tutorialspoint.com"],
        "build_search_url": _tpoint_search,
        "max_results": 6,
    },
]


def _is_allowed(url: str, allowed_domains: list[str]) -> bool:
    if not allowed_domains:
        return True
    netloc = urlparse(url).netloc.lower()
    return any(netloc.endswith(domain) for domain in allowed_domains)


def parse_links(html: str, provider: dict) -> list[dict]:
    parser = LinkParser()
    parser.feed(html)

    results: list[dict] = []
    base_url = provider.get("base_url", "")
    allowed_domains = provider.get("allowed_domains", [])
    max_results = int(provider.get("max_results", 6))

    for href, text in parser.links:
        if not href or href.startswith("#") or href.startswith("javascript"):
            continue

        full_url = urljoin(base_url, href)
        if not _is_allowed(full_url, allowed_domains):
            continue

        title = text if text else full_url
        results.append(
            {
                "title": title[:120],
                "url": full_url,
                "source": provider.get("name", "Unknown"),
            }
        )

        if len(results) >= max_results:
            break

    return results
