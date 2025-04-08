# This uses LLM, but also tries vanilla approach

from bs4 import BeautifulSoup
from scraper.browser import BrowserSession
from utils.dict_tools import filter_unknown_fields
from utils.relevant_text_filter import extract_relevant_sections

class LinkedInScraper:
    def __init__(self, url: str, llm_client=None, log_queue=None):
        self.url = url
        self.llm_client = llm_client
        self.log_queue = log_queue

    def scrape(self) -> dict:
        with BrowserSession() as session:
            try:
                session.load(self.url)
                self.log_queue.put(f"Scraping {self.url}")
                session.page.goto(self.url, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                self.log_queue.put(f"[WARN] Error while loading {self.url}: {e}. Proceeding with partial data.")

            html = session.page.content()

        soup = BeautifulSoup(html, "html.parser")

        result = {
            "company_name": self._get_title(soup),
            "tagline": self._get_tagline(soup),
            "location": self._get_location(soup),
            "industry": self._get_industry(soup),
        }

        if self._needs_llm(result) and self.llm_client:
            filtered_text = extract_relevant_sections(html)
            llm_data = self.llm_client.extract_fields(filtered_text)
            result.update({k: v for k, v in llm_data.items() if v})

        return filter_unknown_fields(result)
        
    def _get_title(self, soup):
        tag = soup.find("title")
        return tag.text.strip() if tag else None

    def _get_tagline(self, soup):
        tag = soup.find("p", class_="break-words white-space-pre-wrap")
        return tag.text.strip() if tag else None

    def _get_location(self, soup):
        tag = soup.find("dt", string="Headquarters")
        return tag.find_next_sibling("dd").text.strip() if tag else None

    def _get_industry(self, soup):
        tag = soup.find("dt", string="Industry")
        return tag.find_next_sibling("dd").text.strip() if tag else None

    def _needs_llm(self, data: dict) -> bool:
        return sum(bool(v) for v in data.values()) < 2
