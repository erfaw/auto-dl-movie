from pathlib import Path
from chrome_controller import ChromeController

IMDB_WL_URL = r"https://www.imdb.com/user/p.rihuzvwcddwbnucg76npzg62m4/watchlist/?ref_=ext_shr_lnk"

# BASE_DIR = Path(__name__).as_posix()
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

chrome = ChromeController(CHROME_PATH)
chrome.start()
UL_XPATH = (
    r'//*[@id="__next"]/main/div/section/div/section/div/div[1]/section/div[2]/ul'
)
chrome.main_page.goto(url=IMDB_WL_URL)

input("Press anything to close.")


#     ul_locator = page.locator(UL_XPATH)
#     ul_locator.wait_for()

#     all_movies_list = ul_locator.locator("> li").all()

#     first_5_movies = all_movies_list[:5]

#     print(len(first_5_movies))

