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

external_storage_dir = EXTERNAL_STORAGE / "auto-dl-movie"
external_storage_dir.mkdir(exist_ok=True)

for movie_fp in file_handler.downloaded_movies_fp:

    dest_fp = external_storage_dir / movie_fp.name
    if (
        dest_fp.is_file()
        and dest_fp.exists()
        and dest_fp.stat().st_size == movie_fp.stat().st_size
    ):
        print(
            f"---\n🎭🌓'{dest_fp.name}' file already exists in '{external_storage_dir}' !"
        )
        continue

    movie_size_MB = round(movie_fp.stat().st_size / 1024**2, 2)
    free_size_external_storage = file_handler.disk_info(EXTERNAL_STORAGE)['free'] # type: ignore
    if free_size_external_storage > movie_size_MB: 
        file_handler.copy(
            src_fp=movie_fp,
            dest_dir=external_storage_dir,
        )
    else:
        print(f"---\nThere is not enough space for '{movie_fp.name}' in {EXTERNAL_STORAGE}\n  file size    :   {movie_size_MB} MB\n  current free :   {free_size_external_storage} MB")

input("Press anything to close.")
