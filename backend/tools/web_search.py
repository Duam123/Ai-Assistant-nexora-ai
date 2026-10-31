
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse, parse_qs, unquote

from backend.tools.web_reader import read_website


def search_web(query, max_results=5):
    if not query.strip():
        raise ValueError("Please enter a search query.")

    search_url = (
        "https://html.duckduckgo.com/html/?q="
        + quote_plus(query)
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
        )
    }

    response = requests.get(
        search_url,
        headers=headers,
        timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    result_links = soup.select("a.result__a")

    if not result_links:
        raise ValueError(
            "No search results found. The search engine may be "
            "temporarily blocking requests."
        )

    pages = []
    visited_urls = set()

    for link in result_links:
        if len(pages) >= max_results:
            break

        href = link.get("href", "").strip()
        if not href:
            continue

        # DuckDuckGo may wrap the actual URL in a redirect link.
        parsed = urlparse(href)
        redirect_url = parse_qs(parsed.query).get("uddg")

        if redirect_url:
            actual_url = unquote(redirect_url[0])
        else:
            actual_url = href

        if not actual_url.startswith(("http://", "https://")):
            continue

        if actual_url in visited_urls:
            continue

        visited_urls.add(actual_url)

        try:
            page = read_website(actual_url)
            pages.append({
                "title": page["title"],
                "url": page["url"],
                "content": page["content"][:3000]
            })
            print("Read:", page["title"])

        except Exception as error:
            print("Skipped a page:", error)

    if not pages:
        raise ValueError(
            "Search results were found, but none of their pages "
            "could be read."
        )

    return {
        "query": query,
        "pages": pages
    }
