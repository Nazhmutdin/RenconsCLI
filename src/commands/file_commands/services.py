from pathlib import Path
from re import compile
from os import listdir, mkdir, path
from shutil import copy

from settings import Settings




class SortWelderFilesService:
    
    def sort_files(self, folder: str) -> None:
        group_folder_path = self._create_group_folder(folder)

        processed_files = listdir(Settings.PROCESSED_DIR())

        self.ctx
    

    def _copy_welder_file(self, file: str) -> None: ...


    def _create_welder_fodler(welder_name: str) -> None: ...


    def _create_group_folder(self, group_folder: str) -> Path:
        
        group_folder_path = f"{Settings.GROUPS_DIR()}/{group_folder}"
        
        if not path.exists(group_folder_path):
            mkdir(group_folder_path)

        return group_folder_path