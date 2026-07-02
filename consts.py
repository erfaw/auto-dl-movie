from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CHROME_PATH = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
"""Path: point to `chrome.exe` file on your computer. 

This is for usage without `playwright install` stuff. (because we have geoblocked at the moment!)

If it's okay to run that command, feel free to set this to `None` to use default way.
"""

XPATH = {
    "imdb_wl": {
        "ul_container": r'//*[@id="__next"]/main/div/section/div/section/div/div[1]/section/div[2]/ul',
        "year": "xpath=/div/div/div/div[1]/div[2]/div[2]/ul/li[1]",
    },
    "donyaye_serial": {
        "dynamic_archive": {
            "search_input": r"xpath=/html/body/div/div[2]/input",
            "show_links_btn_text": r"مشاهده لینک ها",
            "mkv_links": "a[href$='.mkv']",
        },
    },
}
"""dict[dict[xpath]]: an organized dictionary for each site we use till here. 
this organization mostly is for be scalable for future!
"""

URLS = {
    "donyaye_serial": {
        "one_page_archive": "https://dls2.aparatchi-dlcenter.top/DonyayeSerial/donyaye_serial_all_archive.html",
        "dynamic_archive": "https://dls6.aparatchi-dlcenter.top/DonyayeSerial/10_thous.html",
    },
    "imdb_wl": r"https://www.imdb.com/user/p.rihuzvwcddwbnucg76npzg62m4/watchlist/",
}
"""dict[url]: an organized dictionary for each site we use till here. 
this organization mostly is for be scalable for future!
"""

SAVE_DIR = Path().home() / "Desktop" / "auto-movie-downloader"
"""Path: default is to your desktop in windows and in other OS idk :) .

>>> Users/<Your User>/Dekstop/auto-movie-downloader

"""

PREFER = {
    "resolution": "720p",
    "dub/subtitle": "SoftSub",
}
"""dict: some preferation details. so be able to change it from here. 
"""