import os
import arxiv
import requests
import uuid
from bs4 import BeautifulSoup

ASSET_DIR = "assets"
os.makedirs(ASSET_DIR, exist_ok=True)

def ingest_arxiv_paper(query):
    search = arxiv.Search(query=query, max_results=1)
    result = next(search.results(), None)
    if result:
        pdf_url = result.pdf_url
        pdf_path = os.path.join(ASSET_DIR, f"{result.title[:50]}.pdf")
        res = requests.get(pdf_url)
        if res.status_code == 200:
            with open(pdf_path, "wb") as f: f.write(res.content)
            return pdf_path
    return None

def ingest_ieee_paper(query: str) -> str:
    api_key = os.getenv("IEEE_API_KEY")
    if not api_key:
        print("⚠️ IEEE API key not found in .env")
        return None

    url = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
    params = {
        "apikey": api_key,
        "format": "json",
        "max_records": 1,
        "start_record": 1,
        "sort_order": "asc",
        "sort_field": "article_number",
        "querytext": query,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("⚠️ Failed to fetch IEEE paper:", response.status_code)
        return None

    data = response.json()
    articles = data.get("articles", [])
    if not articles:
        print("⚠️ No articles found for:", query)
        return None

    article = articles[0]
    title = article.get("title", "No Title")
    abstract = article.get("abstract", "No abstract available.")
    authors = ", ".join([auth['full_name'] for auth in article.get("authors", [])]) if article.get("authors") else "Unknown authors"

    # Create a temporary text file pretending to be a "PDF" (so summary system still works)
    fake_paper = f"Title: {title}\nAuthors: {authors}\n\nAbstract:\n{abstract}"
    filename = f"ieee_{uuid.uuid4().hex[:8]}.txt"
    path = os.path.join("assets", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(fake_paper)

    return path