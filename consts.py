from pathlib import Path

IMDB_WL_URL = r"https://www.imdb.com/user/p.rihuzvwcddwbnucg76npzg62m4/watchlist/"

# BASE_DIR = Path(__name__).as_posix()
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

UL_XPATH = (
    r'//*[@id="__next"]/main/div/section/div/section/div/div[1]/section/div[2]/ul'
)

URLs = {
    "donyaye_serial": {
        "one_page_archive": "https://dls2.aparatchi-dlcenter.top/DonyayeSerial/donyaye_serial_all_archive.html",
        "dynamic_archive": "https://dls6.aparatchi-dlcenter.top/DonyayeSerial/10_thous.html",
    },
}

SEARCH_INPUT_XPATH = r"xpath=/html/body/div/div[2]/input"

SAVE_DIR = Path().home() / "Desktop" / "auto-movie-downloader"
