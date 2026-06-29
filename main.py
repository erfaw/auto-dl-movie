from playwright.sync_api import Playwright, sync_playwright
from pathlib import Path

IMDB_WL_URL = r"https://www.imdb.com/user/p.rihuzvwcddwbnucg76npzg62m4/watchlist/?ref_=ext_shr_lnk"

# BASE_DIR = Path(__name__).as_posix()
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


def run(playwright: Playwright): # TODO : make a BrowserController class for playwright stuff.
    chrome = playwright.chromium
    context = chrome.launch(
        executable_path=CHROME_PATH,
        headless=False, # TODO : comment it and check when development was done.
    )

    page = context.new_page()

    page.goto(url=IMDB_WL_URL)

    UL_XPATH = (
        r'//*[@id="__next"]/main/div/section/div/section/div/div[1]/section/div[2]/ul'
    )
    ul_locator = page.locator(UL_XPATH)
    ul_locator.wait_for()

    all_movies_list = ul_locator.locator("> li").all()

    first_5_movies = []
    for m in all_movies_list: # TODO : refactor this with list comprehension or list slicing.
        if len(first_5_movies) < 5:
            first_5_movies.append(m)
        else:
            break

    print(
        len(first_5_movies)
    )

with sync_playwright() as pw:
    run(pw)
    input("press any key to close")
