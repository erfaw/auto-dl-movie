from pathlib import Path
from chrome_controller import ChromeController

IMDB_WL_URL = r"https://www.imdb.com/user/p.rihuzvwcddwbnucg76npzg62m4/watchlist/"

# BASE_DIR = Path(__name__).as_posix()
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

chrome = ChromeController(CHROME_PATH)

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


chrome.main_page.goto(
    URLs['donyaye_serial']['dynamic_archive']
)
SEARCH_INPUT_XPATH = r'xpath=/html/body/div/div[2]/input'
search_input_locator = chrome.main_page.locator("xpath=/html/body/div/div[2]/input")
search_input_locator.fill(f"{movies[0]["name"]} {movies[0]["year"]}")
search_input_locator.press("Enter")
input("Press anything to close.")
