from pathlib import Path
from chrome_controller import ChromeController

IMDB_WL_URL = r"https://www.imdb.com/user/p.rihuzvwcddwbnucg76npzg62m4/watchlist/"

# BASE_DIR = Path(__name__).as_posix()
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

chrome = ChromeController(CHROME_PATH)
chrome.start()
UL_XPATH = (
    r'//*[@id="__next"]/main/div/section/div/section/div/div[1]/section/div[2]/ul'
)
chrome.main_page.goto(url=IMDB_WL_URL)
movies = chrome.get_movies_list(UL_XPATH)
print(movies)
input("Press anything to close.")
