from pathlib import Path
from chrome_controller import ChromeController
from downloader import Downloader
import subprocess as sp
from consts import (
    CHROME_PATH,
    URLS,
    SAVE_DIR,
    XPATH,
    PREFER
)

chrome = ChromeController(CHROME_PATH)
downloader = Downloader()

chrome.main_page.goto(url=URLS["imdb_wl"])
movies = chrome.get_movies_list(XPATH["imdb_wl"]["ul_container"], XPATH["imdb_wl"]["year"])
movies_dl_links = chrome.get_dl_link(
    URLS,
    movies,
    XPATH["donyaye_serial"]["dynamic_archive"]["search_input"],
    XPATH["donyaye_serial"]["dynamic_archive"]["show_links_btn_text"],
    XPATH["donyaye_serial"]["dynamic_archive"]["mkv_links"],
    PREFER["resolution"],
    PREFER["dub/subtitle"],
)
chrome.close()

SAVE_DIR.mkdir(exist_ok=True)

sp.call("clear", shell=True)
for n, l in movies_dl_links.items():
    print(f'\nDonwloading "{n}" ...')
    downloader.get(l[0], SAVE_DIR)
    print(f"{n} downloaded successfully!")

input("Press anything to close.")
