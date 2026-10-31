import requests
from bs4 import BeautifulSoup


def read_website(url):
    headers = {
        "User-Agent": "AURA-AI/1.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary page elements
    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header"
    ]):
        element.decompose()

    # Extract readable text
    text = soup.get_text(separator=" ", strip=True)

    return text


if __name__ == "__main__":
    url = input("Enter a website URL: ").strip()

    try:
        content = read_website(url)

        print("\nWebsite content:\n")
        print(content[:5000])

        print("\nTotal characters:", len(content))

    except requests.RequestException as error:
        print("Website request failed:", error)

    except Exception as error:
        print("Error:", error)