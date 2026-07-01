from pathlib import Path
import requests as rq
from pathlib import Path
from urllib.parse import unquote
from tqdm import tqdm

class Downloader:
    """
    Make a Downloader object to controll download by stream using `requests`_ package.

    .. _requests:
        https://github.com
    """

    def __init__(self) -> None:
        """
        Downloader using `requests`_

        .. _requests:
            https://github.com
        """


    def get(self, url: str, path: Path) -> None:
        """
        Starting download a file of any type to given path using `stream=True`_ and `Streaming Requests`_ .

        Using chunk_size = `64*1024` = `65,536` (64 KB).

        With power of `tqdm`_ package shows a nice progress bar in terminal.

        Args:
            url(str):
                full URL string which start download with `GET` request.
            path(Path):
                SAVE_DIR which file will be save at. must be made with `pathlib.Path()`_
        Returns:
            None:
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

        with rq.get(url, stream=True) as response:
            with open(file_path, 'wb') as file:
                with tqdm(
                    total=int(response.headers['Content-Length']),
                    unit='B',
                    unit_scale=True,
                ) as pb:
                    for chunk in response.iter_content(chunk_size=64*1024):
                        if chunk :
                            file.write(chunk)
                            pb.update(len(chunk))

