from pathlib import Path

# BASE_DIR = Path(__name__).as_posix()
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

XPATH = {
    "imdb_wl": {
        "ul_container": r'//*[@id="__next"]/main/div/section/div/section/div/div[1]/section/div[2]/ul',
    }
}

URLS = {
    "donyaye_serial": {
        "one_page_archive": "https://dls2.aparatchi-dlcenter.top/DonyayeSerial/donyaye_serial_all_archive.html",
        "dynamic_archive": "https://dls6.aparatchi-dlcenter.top/DonyayeSerial/10_thous.html",
    },
    "imdb_wl": r"https://www.imdb.com/user/p.rihuzvwcddwbnucg76npzg62m4/watchlist/",
}

SEARCH_INPUT_XPATH = r"xpath=/html/body/div/div[2]/input"

SAVE_DIR = Path().home() / "Desktop" / "auto-movie-downloader"
