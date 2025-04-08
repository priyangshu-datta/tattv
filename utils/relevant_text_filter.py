from bs4 import BeautifulSoup

KEYWORDS = [
    "industry", "headquarter", "employees", "founded", "about",
    "mission", "services", "what we do", "who we are", "size",
    "team", "location", "overview", "specialties", "type", "website"
]

def extract_relevant_sections(html: str, max_pairs: int = 10) -> str:
    soup = BeautifulSoup(html, "html.parser")
    chunks = []

    divs = soup.find_all("div")
    i = 0
    while i < len(divs) - 1 and len(chunks) < max_pairs:
        label = divs[i].get_text(strip=True)
        value = divs[i + 1].get_text(strip=True)

        # Heuristic: short label, not too long, keyword must be in label
        if (
            label.lower() in KEYWORDS or
            any(k in label.lower() for k in KEYWORDS)
        ):
            if value:
                chunks.append(f"{label}: {value}")
                i += 2
                continue
        i += 1

    return "\n".join(chunks)
