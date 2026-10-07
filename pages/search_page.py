from urllib.parse import quote

from playwright.sync_api import Page


class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_names = page.locator(".products-grid .product .name")

    def search(self, term: str):
        self.page.goto(f"/#/search?q={quote(term)}")
        self.page.wait_for_load_state("networkidle")
        return self
