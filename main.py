from pathlib import Path
from threading import Thread
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


# TODO (Mid) : Design and implement Database with sqlite and SQLAlchemy to somehow program remebers what it did before and make it possible to implement some more specific features on it.
# TODO (Mid) : With using db; add downloaded movies to another playlist named 'on_hold'.
# TODO (Mid) : With using db; moving we watched and it's already in EXTERNAL_STORAGE to a directory in system and remove it from EXTERNAL_STORAGE, at the same time change details in db about it to prevent from downloading again and copying again. (monolithic procedure).

chrome = ChromeController(CHROME_PATH)
downloader = Downloader()
file_handler = FileHandler(
    base_dir=BASE_DIR, 
)
# TODO (Low) : It can be a full procedure just for one single movie.
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
external_storage_dir = EXTERNAL_STORAGE / "auto-dl-movie"
external_storage_dir.mkdir(exist_ok=True)

def thread_copy(movie_fp):
    dest_fp = external_storage_dir / movie_fp.name
    if (
        dest_fp.is_file()
        and dest_fp.exists()
        and dest_fp.stat().st_size == movie_fp.stat().st_size
    ):
        print(
            f"---\n🎭🌓'{dest_fp.name}' file already exists in '{external_storage_dir}' !"
        )
    else:
        movie_size_MB = round(movie_fp.stat().st_size / 1024**2, 2)
        free_size_external_storage = file_handler.disk_info(EXTERNAL_STORAGE)['free'] # type: ignore
        if free_size_external_storage > movie_size_MB: 
            file_handler.copy(
                src_fp=movie_fp,
                dest_dir=external_storage_dir,
            )
        else:
            print(f"---\nThere is not enough space for '{movie_fp.name}' in {EXTERNAL_STORAGE}\n  file size    :   {movie_size_MB} MB\n  current free :   {free_size_external_storage} MB")


# TODO (High) : Print a heading for downloading. 

sp.call("clear", shell=True)

threads = []
for n, l in movies_dl_links.items(): # TODO (Low) : Make a method for downloading all links in Downloader.
    if l is None:
        print(f'\n❌ Not found any link for "{n}"')
    else:
        # TODO (Mid) : Move print stuff to downloader.get() method (before and after actual procedure)
        # TODO (Mid) : Insert a '---\n' begin of printing. 
        print(f'\nDonwloading "{n}" ...')
        fp = downloader.get(l[0], SAVE_DIR)
        if fp:
            file_handler.downloaded_movies_fp.append(fp)
            background_copy_thread = Thread(target=thread_copy, args=(fp,))
            # TODO: Check the reason of delay of done tick of copy.
            threads.append(background_copy_thread)
            background_copy_thread.start()
        # TODO (High) : Open a Thread for copying the file to `dest`.
        # print(f"✅ {n} downloaded successfully!")
        print(f"✅ {n} downloaded successfully!")

for t in threads:
    t.join()

input("Press anything to close.")
