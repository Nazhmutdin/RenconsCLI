from os import listdir, mkdir, path

from click import Command, Option

from settings import Settings


class SortWelderFilesCommand(Command):

    def __init__(self) -> None:
        name = "sort-welder-files"

        folder_option = Option(["--folder", "-f"], type=str)
        super().__init__(name=name, params=[folder_option], callback=self.execute)


    def execute(self, folder: str) -> None: ...