from pathlib import Path
from chrome_controller import ChromeController
from downloader import Downloader
from file_handler import FileHandler
import subprocess as sp
from consts import (
    CHROME_PATH,
    URLS,
    SAVE_DIR,
    XPATH,
    PREFER,
    BASE_DIR,
    EXTERNAL_STORAGE,
)

chrome = ChromeController(CHROME_PATH)
downloader = Downloader()
file_handler = FileHandler(
    base_dir=BASE_DIR, 
)

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
for n, l in movies_dl_links.items(): # TODO : Make a method for downloading all links in Downloader.
    if l is None:
        print(f'\n❌ Not found any link for "{n}"')
    else:
        print(f'\nDonwloading "{n}" ...')
        fp = downloader.get(l[0], SAVE_DIR)
        if fp:
            file_handler.downloaded_movies_fp.append(fp)
        # TODO : Open a Thread for copying the file to `dest`.
        print(f"✅ {n} downloaded successfully!")

# TODO : Start procedure of file copying.
# free_space = file_handler.disk_info(EXTERNAL_STORAGE)['free'] * 1024 # type:ignore

# dl_dir_whole_space = SAVE_DIR.stat().st_size

# if free_space > dl_dir_whole_space:
#     print('we can do it on a row')

input("Press anything to close.")
