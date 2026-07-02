# TODO : make a FileHandler class to work with files. it must be able to use `shutil` to copy files from a `src` to a `dest` with progressbar using `tqdm`. which for now be called after download procedure.
# TODO : after implementing above todo, with `threading parallelism` make io file copying a thread, io file downloading a thread and these 2 threads must talking to each other through a Queue with main thread.
import shutil
from pathlib import Path


class FileHandler:
    def __init__(self, base_dir: Path) -> None:
        """
        Make an object to work with copying/moving/deleteing/making files on system. using `shutil`.

        Args:
            base_dir (Path): Path object for current running directory of program. 
        """
        self.base_dir = base_dir

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

    def copy(self, src: Path, dest_dir: Path) -> None:
        """
        Use `shutil.copy2()`_ to copy a file from src to dest_dir.

        Args:
            src(Path):
                Path object for source file.
            dest_dir(Path):
                Path object for destination directory. (it has to be directory!)

        Returns:
            None

        .. _shutil.copy2():
            https://docs.python.org/3/library/shutil.html#shutil.copy2
        """
        if not src.exists():
            print(f"This source does not exist. Entered Path: '{src}'")
            return None
        if not src.is_file():
            print(f"Use path to the files please.")
            return None
        if not dest_dir.exists():
            dest_dir.parent.mkdir(parents=True)
        # TODO : make 'dest' to be a directory in logic. then prepare dest_name which is a Path obj. then tend to copy.
        # TODO : check for filenames be exual (if not, file be corrupted for good. )
        # TODO : start copy processing.
        print(shutil.copy2(
            src=src,
            dst=dest_dir,
        ))
        print("✅done")

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
