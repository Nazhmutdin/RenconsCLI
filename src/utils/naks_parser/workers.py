from threading import Thread
from queue import Queue

from src.shemas import WelderShema, ACSTShema
from src.utils.naks_parser.http_worker import get_http_worker
from src.utils.naks_parser.extractors import WelderDataExtractor, ACSTDataExtractor, extract_links
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


class ACSTNaksWorker(Thread):
    def __init__(self, queue: Queue, acsts_list: list[ACSTShema]) -> None:
        Thread.__init__(self)

        self.http_worker = get_http_worker(mode="acst")
        self.queue = queue
        self.result = acsts_list
        self.extractor = ACSTDataExtractor()


    def run(self) -> None:
        while not self.queue.empty():
            value = self.queue.get_nowait()
            
            main_page = self.http_worker.get_acst_page(value)

            links = extract_links(main_page)

            self.result.append(self.extractor.extract(main_page))