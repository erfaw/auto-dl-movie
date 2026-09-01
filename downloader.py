from pathlib import Path
import requests as rq
from pathlib import Path
from urllib.parse import unquote
from tqdm import tqdm

class Downloader:
    def __init__(self) -> None:
        """
        Make a Downloader object to controll download by stream using `requests`_ package.

        .. _requests:
            https://requests.readthedocs.io/en/latest/#
        """


    def get(self, url: str, path: Path) -> Path | None:
        """
        Starting download a file of any type to given path using `stream=True`_ and `Streaming Requests`_ .

        Using chunk_size = `64*1024` = `65,536` (64 KB).

        With power of `tqdm`_ package shows a nice progress bar in terminal.

        Note:
            returns the Path object even file exists from past and is complete.

        Args:
            url(str):
                full URL string which start download with `GET` request.
            path(Path):
                SAVE_DIR which file will be save at. must be made with `pathlib.Path()`_
        Returns:
            Path | None: Path to the downloaded file if successful; otherwise, None.

        .. _stream=True:
            https://requests.readthedocs.io/en/latest/api/#requests.Response.iter_content
        .. _Streaming Requests:
            https://requests.readthedocs.io/en/latest/user/advanced/#streaming-requests
        .. _pathlib.Path():
            https://docs.python.org/3/library/pathlib.html#pathlib.Path
        .. _tqdm:
            https://tqdm.github.io/docs/tqdm/
        """
        file_name = unquote(url.split('/')[-1])
        path.mkdir(exist_ok=True)
        file_path = path / file_name

        if file_path.is_file() and file_path.exists():
            # TODO (Low): ask user for this situation, rewrite or skip?
            is_complete = False
            content_length = None
            with rq.head(url) as r:
                # if r.status_code == 200: # TODO (HIGH) check status_code before each action, and raise error or pass None for that situation.
                try:
                    content_length = r.headers['Content-Length']
                except KeyError:
                    content_length = -1
                file_size_byte = int(content_length)
                if file_size_byte <= file_path.stat().st_size:
                    is_complete = True
            print(f"\t🎭🌓'{file_path.name}' file already exists in dest_dir!\n\t(download is_complete: {is_complete})")
            if is_complete:
                return file_path
            else:
                return None
        # TODO (Low) : Implement resume feature for downlading. (if there is a file with that name already)
        # TODO (HIGH) : Implement Error handling for ConnectoinError or Abort.

        with rq.get(url, stream=True) as response:
            content_length = None
            try:
                content_length = response.headers['Content-Length']
            except KeyError:
                content_length = -1
            file_size_byte = int(content_length)
            with open(file_path, 'wb') as file:
                with tqdm(
                    total=file_size_byte,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=file_path.name,
                ) as pb:
                    for chunk in response.iter_content(chunk_size=64*1024):
                        if chunk :
                            file.write(chunk)
                            pb.update(len(chunk))
        return file_path

