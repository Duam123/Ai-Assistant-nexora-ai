import requests
from bs4 import BeautifulSoup


def read_website(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup([
        "script", "style", "nav",
        "footer", "header", "noscript"
    ]):
        element.decompose()

    title = soup.title.get_text(strip=True) if soup.title else url
    content = soup.get_text(separator=" ", strip=True)

    content = " ".join(content.split())
    content = content[:6000]

    if not content:
        raise ValueError("No readable content found on this webpage.")

    return {
        "url": url,
        "title": title,
        "content": content
    }