from scraper.browser import BrowserSession
from scraper.vanilla.extractors.company_name import extract_company_name
from scraper.vanilla.extractors.emails import extract_emails
from scraper.vanilla.extractors.phone_numbers import extract_phone_numbers
from scraper.vanilla.extractors.social_links import extract_social_links
from utils.dict_tools import deep_update, filter_unknown_fields
from utils.url_tools import normalize_url

class WebsiteScraper:
    def __init__(self, url: str, log_queue=None):
        self.next_links = {normalize_url(url)}
        self.visited_links = set()
        self.results = dict()
        self.log_queue = log_queue

    def scrape(self):
        while self.next_links:
            url = self.next_links.pop()
            if url in self.visited_links:
                continue
            self.url = url
            with BrowserSession() as session:
                session.load(url)
                self.visited_links.add(url)
                self.log_queue.put(f"Scraping {url}")
                self.page = session.page
                self.domain = self._get_domain(url)
                self._extract()
                self.log_queue.put(f"Finished {url}")
                self.next_links.update(self._extract_internal_links())

    def _get_domain(self, url):
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.lower().replace("www.", "")

    def _absolute_url(self, href):
        from urllib.parse import urljoin
        return urljoin(self.url, href)

    def _extract_internal_links(self):
        RELEVANT_KEYWORDS = ["about", "team", "company", "leadership", "contact", "founder", "careers", "story"]
        links = set()

        # normal links
        anchors = self.page.query_selector_all("a")
        base_domain = self._get_domain(self.url)

        for anchor in anchors:
            try:
                href = anchor.get_attribute("href")
                text = anchor.inner_text().strip().lower()

                if not href or href.startswith(("mailto:", "javascript:", "tel:", "#")):
                    continue

                href = href.split("#")[0].strip("/")
                full_url = normalize_url(self._absolute_url(href))
                if self._get_domain(full_url) != base_domain:
                    continue

                # Ensure BOTH link text and href contain relevant keywords
                if any(kw in text for kw in RELEVANT_KEYWORDS) and any(kw in full_url.lower() for kw in RELEVANT_KEYWORDS):
                    links.add(full_url)
            except Exception:
                continue

        # quirky links (clickable elements)
        CLICKABLE_TAGS = {"div", "button", "span", "p"}
        elements = self.page.query_selector_all("*")

        for el in elements:
            try:
                text = el.inner_text().strip().lower()
                if not any(k in text for k in RELEVANT_KEYWORDS):
                    continue

                tag = el.evaluate("el => el.tagName.toLowerCase()")
                href = el.get_attribute("href")
                role = el.get_attribute("role")
                onclick = el.get_attribute("onclick")

                # Handle anchor with relevant text and href
                if tag == "a" and href and not href.startswith("#"):
                    abs_url = normalize_url(self._absolute_url(href))
                    if any(kw in abs_url.lower() for kw in RELEVANT_KEYWORDS):
                        links.add(abs_url)
                    continue

                # Handle clickable elements with relevant text and resulting URL
                if tag in CLICKABLE_TAGS or role == "button" or onclick:
                    with self.page.expect_navigation(wait_until="networkidle", timeout=3000):
                        el.click(force=True)

                    new_url = normalize_url(self.page.url)
                    if any(kw in new_url.lower() for kw in RELEVANT_KEYWORDS):
                        links.add(new_url)

                    self.page.go_back(wait_until="networkidle")

            except Exception:
                continue

        return links

    def _extract(self):
        html = self.page.content()

        deep_update(self.results, {
            "emails": extract_emails(html),
            "phone_numbers": extract_phone_numbers(html),
            "company_name": extract_company_name(self.page, self.domain),
            **extract_social_links(self.page),
        })
        
        self.results = filter_unknown_fields(self.results)