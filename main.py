from playwright.sync_api import Playwright, sync_playwright
from pathlib import Path

IMDB_WL_URL = r"https://www.imdb.com/user/p.rihuzvwcddwbnucg76npzg62m4/watchlist/?ref_=ext_shr_lnk"

# BASE_DIR = Path(__name__).as_posix()
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


def run(playwright: Playwright):
    chrome = playwright.chromium
    context = chrome.launch(
        executable_path=CHROME_PATH,
        headless=False,
    )

    page = context.new_page()

    page.goto(url=IMDB_WL_URL)

    all_movies_list = page.locator(".ipc-metadata-list-summary-item").all()

    first_5_movies = []

    for m in all_movies_list:
        if len(first_5_movies) < 6:
            first_5_movies.append(m)
        else:
            break

    input()


with sync_playwright() as pw:
    run(pw)
