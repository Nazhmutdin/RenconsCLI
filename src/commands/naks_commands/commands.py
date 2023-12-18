from os import listdir
from time import sleep
import json

from click import Command, Option

from settings import Settings
from src.utils.threading_progress_bar_queue import ThreadProgressBarQueue
from src.utils.naks_parser.workers import PersonalNaksWorker, ACSTNaksWorker
from src.shemas import WelderShema, ACSTShema
from src.utils.funcs import load_json


class ParseNaksWeldersCommand(Command):
    def __init__(self) -> None:
        name = "parse-naks-welders"

        file_option = Option(["--file"], type=bool, help="get search values from search_settings.json file")
        folder_option = Option(["--folder"], type=str, help="get folder's names in folder as search_values")
        threads_option = Option(["--threads", "-th"], type=int, default=1, help="amount threads")

        super().__init__(name=name, params=[file_option, folder_option, threads_option], callback=self.execute)
            

    def _fill_queue(self, queue: ThreadProgressBarQueue, file: str | None, folder: str | None) -> None:

        if file:
            settings = load_json(Settings.SEARCH_VALUES_FILE())["personal_naks_parsing"]["search_values"]

            for value in settings:
                queue.put(value)

        if folder:
            for value in [value for value in listdir(f"{Settings.GROUPS_DIR()}/{folder}")]:
                queue.put(value)


    def execute(self, threads: int, file: str | None = None, folder: str | None = None) -> None:
        queue = ThreadProgressBarQueue()
        self._fill_queue(queue, file, folder)
        queue.init_progress_bar()

        welder_list: list[WelderShema] = []

        ths: list[PersonalNaksWorker] = []

        for _ in range(threads):
            thread = PersonalNaksWorker(queue, welder_list)

            thread.start()
            ths.append(thread)

        for th in ths:
            th.join()
        sleep(.1)

        welder_list = [welder.model_dump(mode="json") for welder in welder_list]

        with open(Settings.WELDERS_DATA_JSON(), "w", encoding="utf-8") as json_file:
            json.dump(welder_list, json_file, indent=4, ensure_ascii=False)
            json_file.close()


class ParseNaksACSTCommand(Command):
    def __init__(self) -> None:

        name = "parse-naks-acsts"
        threads_option = Option(["--threads", "-th"], type=int, default=1, help="amount threads")

        super().__init__(name=name, params=[threads_option], callback=self.execute)

    
    def _fill_queue(self) -> None:

        settings = load_json(Settings.SEARCH_VALUES_FILE())["acst_naks_parsing"]["search_values"]

        for value in settings:
            self.queue.put(value)

    
    def execute(self, threads: int) -> None:
        self.queue = ThreadProgressBarQueue()
        self._fill_queue()
        self.queue.init_progress_bar()

        acsts: list[ACSTShema] = []

        ths: list[ACSTNaksWorker] = []

        for _ in range(threads):
            thread = ACSTNaksWorker(self.queue, acsts)

            thread.start()
            ths.append(thread)

        for th in ths:
            th.join()
        sleep(.1)


        acsts = [acst.model_dump(mode="json") for acst in acsts]

        with open(Settings.ACSTS_DATA_JSON(), "w", encoding="utf-8") as json_file:
            json.dump(acsts, json_file, indent=4, ensure_ascii=False)
            json_file.close()
