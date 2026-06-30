from playwright.sync_api import Playwright, sync_playwright, Page, Browser
from pathlib import Path


class ChromeController:
    """
    A controller for Chrome which could do stuff with empowerment of `Playwright`.
    """

    def __init__(self, chrome_path: Path) -> None:
        self.chrome_path = chrome_path

    def start(self):
        self.pw: Playwright = sync_playwright().start()
        self.browser: Browser = self.pw.chromium.launch(
            executable_path=self.chrome_path,
            headless=False,  # TODO : comment it and check when development was done.
        )
        self.main_page: Page = self.browser.new_page()

    def close(self):
        self.pw.stop()

    def make_page(self):
        pass

    def get_movies_list(self):
        pass
