from bs4 import BeautifulSoup
import requests


# Standard headers to fetch a website
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}


def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10  # ⬅️ CRITICAL FIX
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")

        title = soup.title.string.strip() if soup.title else "No title found"

        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input", "nav", "footer", "header"]):
                irrelevant.decompose()

            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""

        return (title + "\n\n" + text)[:2_000]

    except requests.exceptions.Timeout:
        return "ERROR: Website took too long to respond."

    except requests.exceptions.RequestException as e:
        return f"ERROR: Could not fetch website ({e})"


def fetch_website_links(url):
    """
    Return the links on the website at the given url
    """
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")
        links = [link.get("href") for link in soup.find_all("a")]
        return [link for link in links if link]

    except requests.exceptions.RequestException:
        return []
