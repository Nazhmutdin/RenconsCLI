import typing
from re import compile

from pydantic import BaseModel



class WelderFolder(BaseModel):
    original_name: str
    lower_name: str
    kleymo: str | None


class WelderFileSortContex(BaseModel):

    def __init__(self, folders: list[str]) -> None:
        welder_name = compile(r"[А-Я][а-я ]+|[A-Z][a-z ]+")
        welder_kleymo = compile(r"[A-Z0-9]{4}")
        self.folders: list[WelderFolder] = []

        for folder in folders:
            name = welder_name.search(folder)[0]
            kleymo = welder_kleymo.search(folder)[0]

            if name == None:
                raise ValueError("Invalid folder name!")

            self.folders.append(
                WelderFolder(
                    original_name=name,
                    lower_name=name.lower(),
                    kleymo=kleymo
                )
            )
        

    def get_welder_folder(self, welder_name: str) -> WelderFolder:
        for folder in self.folders:
            if folder.lower_name == welder_name.lower():
                return folder
            