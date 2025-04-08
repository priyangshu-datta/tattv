from playwright.sync_api import sync_playwright

class BrowserSession:
    def __init__(self):
        self.page = None
        self.browser = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        self.playwright.stop()

    def load(self, url: str):
        self.page.goto(url, wait_until='networkidle')