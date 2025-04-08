import re
from bs4 import BeautifulSoup

def extract_phone_numbers(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    text_content = soup.get_text()
    tel_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('tel:')]

    combined_text = text_content + "\n" + "\n".join(tel_links)

    phone_pattern = re.compile(
        r"""
        (?:(?:\+|00)\d{1,3}[\s\-\.]?)?
        (?:\(?\d{2,4}\)?[\s\-\.]?)?
        \d{3,4}[\s\-\.]?\d{3,4}
        """,
        re.VERBOSE
    )

    # Extract matches and clean them
    raw_matches = re.findall(phone_pattern, combined_text)
    cleaned = [re.sub(r"[^\d+]", "", num) for num in raw_matches if len(re.sub(r"[^\d]", "", num)) >= 7]

    return list(set(cleaned))
