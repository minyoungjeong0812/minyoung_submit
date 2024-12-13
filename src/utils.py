import requests
from bs4 import BeautifulSoup

def load_report(source: str) -> str:
    # Check if source starts with "http" to determine if it's a URL
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source)
        response.raise_for_status()
        content = response.text
    else:
        # Otherwise treat source as a file path
        with open(source, "r", encoding="utf-8") as f:
            content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    return text.strip()