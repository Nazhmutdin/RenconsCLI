from threading import Thread
from queue import Queue
from typing import Literal
from re import fullmatch

from src.shemas import WelderShema, ACSTShema
from src.utils.naks_parser.http_worker import get_http_worker, PersonalNaksHTTPService
from src.utils.naks_parser.extractors import WelderDataExtractor, ACSTDataExtractor, extract_links, WelderDataExtractionService
from src.utils.naks_parser.sorter import Sorter


class PersonalNaksWorker(Thread):
    def __init__(self, queue: Queue, welder_list: list[WelderShema]) -> None:
        Thread.__init__(self)

        self.http_worker = get_http_worker(mode="personal")
        self.queue = queue
        self.welder_list = welder_list
        self.extractor = WelderDataExtractor()


    def run(self) -> None:
        while not self.queue.empty():
            value = self.queue.get_nowait()
            
            main_page = self.http_worker.get_welder_page(value)

            links = extract_links(main_page)

            additional_pages = self.http_worker.get_welder_certification_pages(links)

            self.welder_list += Sorter().sort_welder_data(self.extractor.extract(main_page, additional_pages))

    
    def _detect_search_value_type(self, search_value: str) -> Literal["name", "kleymo", "certification_number"]:
        if fullmatch(r"[A-Z0-9]{4}", search_value): return "kleymo"
        
        elif fullmatch(r"[А-Я]+-[А-Я0-9]+-[IV]+-[0-9]+", search_value): return "certification_number"

        else: return "name" 