# TODO : make a FileHandler class to work with files. it must be able to use `shutil` to copy files from a `src` to a `dest` with progressbar using `tqdm`. which for now be called after download procedure. 
# TODO : after implementing above todo, with `threading parallelism` make io file copying a thread, io file downloading a thread and these 2 threads must talking to each other through a Queue with main thread. 
import shutil


class FileHandler:
    def __init__(self) -> None:
        """
        Make an object to work with copying/moving/deleteing/making files on system. using `shutil`.
        """
        pass

    def disk_info(self):
        pass 
    
    def copy(self):
        pass

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
    