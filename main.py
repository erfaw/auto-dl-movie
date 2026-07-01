from pathlib import Path
from chrome_controller import ChromeController
from downloader import Downloader
import subprocess as sp

IMDB_WL_URL = r"https://www.imdb.com/user/p.rihuzvwcddwbnucg76npzg62m4/watchlist/"

# BASE_DIR = Path(__name__).as_posix()
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

chrome = ChromeController(CHROME_PATH)
downloader = Downloader()

UL_XPATH = (
    r'//*[@id="__next"]/main/div/section/div/section/div/div[1]/section/div[2]/ul'
)

chrome.main_page.goto(url=IMDB_WL_URL)
movies = chrome.get_movies_list(UL_XPATH)

URLs = {
    "donyaye_serial": {
        "one_page_archive": "https://dls2.aparatchi-dlcenter.top/DonyayeSerial/donyaye_serial_all_archive.html",
        "dynamic_archive": "https://dls6.aparatchi-dlcenter.top/DonyayeSerial/10_thous.html", 
    },
}

SEARCH_INPUT_XPATH = r'xpath=/html/body/div/div[2]/input'

movies_dl_links = chrome.get_dl_link(URLs, SEARCH_INPUT_XPATH, movies)

SAVE_DIR = Path().home() / 'Desktop' / 'auto-movie-downloader'
SAVE_DIR.mkdir(exist_ok=True)

sp.call('clear', shell=True)
for n, l in movies_dl_links.items():
    print(f'\nDonwloading "{n}" ...')
    downloader.get(l[0], SAVE_DIR)
    print(f"{n} downloaded successfully!")

input("Press anything to close.")
