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

    def get_dl_link(self, urls: dict, search_xpath: str, movies: list[dict]) -> dict:
        """
        Get all download links from particular page in `Donyaye Serial` website archive.

        Args:
            urls (dict[dict]): a dict contain link of website archive. where to check. for now it is shit and static!
            search_xpath (str): raw string to locating search input with `XPATH`.
            movies (list[dict]): list of dict which must contains `name`, `year`, `directors` of movie.
            None:

        Examples:
            urls :
            >>> URLs = {
                    "donyaye_serial": {
                        "one_page_archive": "https://dls2.aparatchi-dlcenter.top/DonyayeSerial/donyaye_serial_all_archive.html",
                        "dynamic_archive": "https://dls6.aparatchi-dlcenter.top/DonyayeSerial/10_thous.html",
                    },
                }
            search_xpath :
            >>> r'xpath=/html/body/div/div[2]/input'
            movies :
            >>> m = [
                    {"name": "se7en", "year": "1995", "directors": ['David Fincher']}
                ]

        Returns:
            dict: strings of downlaod links of each film.
        """
        self.main_page.goto(urls["donyaye_serial"]["dynamic_archive"])

        search_input_locator = self.main_page.locator(search_xpath)
        show_links_btn_locator = self.main_page.get_by_text("مشاهده لینک ها")

        links = {}
        for m in movies:
            search_input_locator.fill(f"{m["name"]} {m["year"]}")
            search_input_locator.press("Enter")
            
            if show_links_btn_locator.count() == 0 :
                # TODO : make procedure to remove this films from Watchlist and added them to another playlist called 'Not_found' or 'Irani'
                links[m['name']] = 'not_found'
            else:
                show_links_btn_locator.first.click()

                all_links_locator = self.main_page.locator("a[href$='.mkv']").all()
                all_links = [link.get_attribute('href') for link in all_links_locator]

                filtered_links = [ l for l in all_links if "720p" in l and "SoftSub" in l ] # type: ignore
                if not filtered_links : 
                    filtered_links = [ l for l in all_links if "720p" in l ] # type: ignore
                if not filtered_links : 
                    filtered_links = [all_links[0]]

                links[f"{m['name']} {m['year']}"] = filtered_links

        return links

    def dl_movie(self, url: str, save_path: Path):
        """
        Download a file with given url and file path to save.

        Args:
            url (str):string url use for download.
            save_path (Path):a Path obj for saving file.
        """
        pass
        # with self.main_page.expect_download() as download_info:
        #     self.main_page.goto(url)

        # download = download_info.value

        # download.save_as(save_path / download.suggested_filename)
