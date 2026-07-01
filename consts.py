from pathlib import Path

# BASE_DIR = Path(__name__).as_posix()
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

XPATH = {
    "imdb_wl": {
        "ul_container": r'//*[@id="__next"]/main/div/section/div/section/div/div[1]/section/div[2]/ul',
    },
    "donyaye_serial": {
        "dynamic_archive": {
            "search_input": r"xpath=/html/body/div/div[2]/input"
        },
    },
}

URLS = {
    "donyaye_serial": {
        "one_page_archive": "https://dls2.aparatchi-dlcenter.top/DonyayeSerial/donyaye_serial_all_archive.html",
        "dynamic_archive": "https://dls6.aparatchi-dlcenter.top/DonyayeSerial/10_thous.html",
    },
    "imdb_wl": r"https://www.imdb.com/user/p.rihuzvwcddwbnucg76npzg62m4/watchlist/",
}
"""dict: and organized dictionary for each site we use till here. 
this organization mostly is for be scalable for future!
"""

SAVE_DIR = Path().home() / "Desktop" / "auto-movie-downloader"
"""Path: default is to your desktop in windows and in other OS idk :) .

>>> Users/<Your User>/Dekstop/auto-movie-downloader

"""
