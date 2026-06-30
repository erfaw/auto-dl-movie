from playwright.sync_api import Playwright, sync_playwright, Page, Browser
from pathlib import Path


class ChromeController:
    """
    A controller for Chrome which could do stuff with empowerment of `Playwright`.
    """

    def __init__(self, chrome_path: Path) -> None:
        """
        A Chrome based controller powered by `Playwright` based on a main page to explore and automize some basic works.

        It automaticly `start()`.

        Args:
            chrome_path (:obj:`Path`): Path to `chrome.exe` file on system .

        Returns:
            None
        """
        self.chrome_path = chrome_path
        self.start()

    def start(self):
        """
        set `pw`, run `start()` and make a `self.main_page` to work on it.

        actually starts a playwright loop to be able make browser.
        """
        self.pw: Playwright = sync_playwright().start()
        self.browser: Browser = self.pw.chromium.launch(
            executable_path=self.chrome_path,
            headless=False,  # TODO : comment it and check when development was done.
        )
        self.main_page: Page = self.browser.new_page()

    def close(self):
        """
        run `stop()` on `self.pw`.
        """
        self.pw.stop()

    def get_movies_list(self, ul_selector):
        """
        Scrape all movies and slice 5 first then return.

        Args:
            ul_selector: XPath or css selector of some element in DOM.

        Returns:
            list[dict]: return a list of dicts contain movies detail.
        """
        ul_continer = self.main_page.locator(ul_selector)
        ul_continer.wait_for()
        li_first_child_selector = "> li"
        movies = ul_continer.locator(li_first_child_selector).all()[:5]

        r_movie = []
        for m in movies:
            d = {}
            name = m.locator("h4").inner_text()
            d["name"] = name[3:]

            year = m.locator(
                "xpath=/div/div/div/div[1]/div[2]/div[2]/ul/li[1]"
            ).inner_text()
            d["year"] = year

            directors = (
                m.get_by_text("Director")
                .locator("xpath=../span[position() > 1]")
                .all_inner_texts()
            )
            d["directors"] = directors

            r_movie.append(d)

        return r_movie
