# TODO : With `threading parallelism` make io file copying a thread, io file downloading a thread and these 2 threads must talking to each other through a Queue with main thread.
import shutil
from pathlib import Path
from tqdm import tqdm


class FileHandler:
    def __init__(self, base_dir: Path) -> None:
        """
        Make an object to work with copying/moving/deleteing/making files on system. using `shutil`.

        Args:
            base_dir (Path): Path object for current running directory of program. 
        """
        self.base_dir = base_dir
        self.CHUNK_SIZE = 64 * 1024

    def disk_info(self, path: Path) -> dict[str, float] | None:
        """
        Get information about disk of given Path obj and return.
        Args:
            path (Path): Path object which must be `exists()=True` on this system.
        Returns:
            dict[str, float] | None:
                if exists: used, free and total amount in `GB` (1024**3).
                if not exists: None.
        Example:
            P:/ does not exist:
            >>> disk_info(Path('P:/'))
            None
            
            C:/ exist:
            >>> disk_info(Path('C:/')) # exist
            {'unit': 'GB', 'total': 326.31, 'used': 248.96, 'free': 77.35}
        """

        if not path.exists():
            print(f"This Path({path}) does not exist on this system.")
            return None

        disk = {}
        du = shutil.disk_usage(path=path)
        disk["unit"] = 'GB'
        disk["total"] = float(round(du.total/(1024**3), 2))
        disk["used"] = float(round(du.used/(1024**3), 2))
        disk["free"] = float(round(du.free/(1024**3), 2))
        return disk

    def copy(self, src_fp: Path, dest_dir: Path) -> None:
        """
        It validates `src_fp` and `dest_dir` then calls `_copy_with_progress_bar()`.

        Args:
            src_fp(Path):
                Path object for source file.
            dest_dir(Path):
                Path object for destination directory. (it has to be directory!)

        Returns:
            None
        """
        if not src_fp.exists():
            print(f"This source does not exist. Entered Path: '{src_fp}'")
            return None
        if not src_fp.is_file():
            print(f"Use path to the files please.")
            return None
        
        if dest_dir.is_file():
            print("Entered Path for 'dest_dir' is not a directory. Use path to a directory please.")
            return None
        if not dest_dir.exists(): # TODO : could be refactored to one line and delete if.
            dest_dir.parent.mkdir(parents=True, exist_ok=True)

        dest_fp = dest_dir / src_fp.name

        if dest_fp.is_file() and dest_fp.exists():
            # TODO (low): ask user for this situation, rewrite or skip?
            print(f"🎭🌓'{dest_fp.name}' file already exists in dest_dir!")
            return None

        if dest_fp.name == src_fp.name:
            dest_fp.parent.mkdir(exist_ok=True)

            print(f"---\nstart copying...\n\tsrc: '{src_fp}'\n\tdest_fp: '{dest_dir}'")
            self._copy_with_progress_bar(src_fp, dest_fp, )
            print("✅done")
        else:
            raise RuntimeError

    def _copy_with_progress_bar(self, src_fp: Path, dest_fp: Path) -> None:
        """
        Use `open()` and read/write with chunks to copy a file from src to dest_dir.

        Args:
            src_fp (Path):
                Path object for source file.
            dest_fp(Path):
                Path object for destination directory. (it has to be directory!)
        
        Returns:
            None:
        """
        total_size = src_fp.stat().st_size

        with (
            src_fp.open("rb") as source,
            dest_fp.open("wb") as target,
            tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=src_fp.name,
                colour="green",
            ) as pbar,
        ):
            while chunk := source.read(self.CHUNK_SIZE):
                target.write(chunk)
                pbar.update(len(chunk))

        shutil.copystat(src_fp, dest_fp)

    def move(self):
        pass

    def delete(self):
        pass 

    def rename(self):
        pass

    def copy_dir(self):
        pass

    def remove_dir(self):
        pass 
