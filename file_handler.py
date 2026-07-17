# TODO (High) : With `threading parallelism` make io file copying a thread, io file downloading a thread and these 2 threads must talking to each other through a Queue with main thread.
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
        self.downloaded_movies_fp: list = []
        
    def disk_info(self, path: Path) -> dict[str, float] | None:
        """
        Get information about disk of given Path obj and return.
        Args:
            path (Path): Path object which must be `exists()=True` on this system.
        Returns:
            dict[str, float] | None:
                if exists: used, free and total amount in `MB` (1024**2).
                if not exists: None.
        Example:
            P:/ does not exist:
            >>> disk_info(Path('P:/'))
            None
            
            C:/ exist:
            >>> disk_info(Path('C:/')) # exist
            {'unit': 'MB', 'total': 334141.44, 'used': 254935.04, 'free': 79206.40}
        """

        if not path.exists():
            print(f"This Path({path}) does not exist on this system.")
            return None

        disk = {}
        du = shutil.disk_usage(path=path)
        disk["unit"] = 'MB'
        disk["total"] = float(round(du.total/(1024**2), 2))
        disk["used"] = float(round(du.used/(1024**2), 2))
        disk["free"] = float(round(du.free/(1024**2), 2))
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
        # TODO : Remove print statements and let just preffix of tqdm talks to user.
        if not src_fp.exists():
            print(f"This source does not exist. Entered Path: '{src_fp}'")
            return None
        if not src_fp.is_file():
            print(f"Use path to the files please.")
            return None
        
        if dest_dir.is_file():
            print("Entered Path for 'dest_dir' is not a directory. Use path to a directory please.")
            return None
        if not dest_dir.exists(): # TODO (Low) : could be refactored to one line and delete if.
            dest_dir.parent.mkdir(parents=True, exist_ok=True)

        dest_fp = dest_dir / src_fp.name

        if dest_fp.is_file() and dest_fp.exists():
            # TODO (Low) : ask user for this situation, rewrite or skip?
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

    def copy_dir(self, src_dir: Path, dest_dir: Path) -> Path:
        """
        Copy a directory with all files in it (without any ignore patterns for now) into a destination path. using `shutil.copytree()`_.

        Args:
            src_dir (Path): Path object which must be a directory to perform copytree().
            dest_dir (Path): Path object which must be a directory to copy into it.

        Returns:
            Path: if performance was successful return directory path object of copied directory.

        .. _shutil.copytree():
            https://docs.python.org/3/library/shutil.html#shutil.copytree
        """
        dest_dir = dest_dir / src_dir.name
        dest_dir.mkdir(exist_ok=True)
        if not src_dir.exists() or not src_dir.is_dir():
            raise AttributeError(f"{src_dir} does not exist or not a directory.\nError message")
        else:
            shutil.copytree(
                src=src_dir,
                dst=dest_dir,
                ignore=None,
                dirs_exist_ok=True,
            )
            return Path(dest_dir)

    def remove_dir(self):
        pass 

    def get_dir_size(self, target_dir: Path) -> dict[str, float | dict[str, float]]:
        """
        Calcluate each file size and a overall size of a directory. using `Path().stats().st_size`_

        Args:
            target_dir (Path): Path object to where we want size details.

        Returns:
            dict[str, float | dict[str, float]]: include each file size and overall size of directory. unit is KB.

        Examples:
        >>> get_dir_size(BASE_DIR)
        {
            'overall_KB': 35.62,
            'files_KB': {
                'python_master_challenges(76_to_).ipynb': 25.06,
                'README.md': 3.0,
                'test_file_exercise_81.txt': 7.12,
                'test_file_exercise_83.txt': 0.3,
                'test_file_exercise_84_1.txt': 0.07,
                'test_file_exercise_84_2.txt': 0.07
            }
        }

        .. _Path().stats().st_size:
            https://docs.python.org/3/library/pathlib.html#pathlib.Path.stat
        """

        r_dict = {}
        r_dict['overall_KB'] = 0 
        r_dict['files_KB'] = {}
        for f in target_dir.rglob('*'):
            r_dict['files_KB'][f.name] = round(f.stat().st_size / 1024, 2)
            r_dict['overall_KB'] += r_dict['files_KB'][f.name]
        return r_dict
