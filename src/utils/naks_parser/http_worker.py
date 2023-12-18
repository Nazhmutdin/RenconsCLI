from time import sleep
import typing

from re import fullmatch
from requests import Session


"""
=======================================================================================================
Types
=======================================================================================================
"""


MainPage: typing.TypeAlias = str
AdditionalPage: typing.TypeAlias = str


"""
=======================================================================================================
Parser
=======================================================================================================
"""


def get_http_worker(mode: typing.Literal["personal", "acst"]) -> "NaksHTTPWorker":
    return NaksHTTPWorker()._set_worker(mode)



class NaksHTTPWorker:

    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://naks.ru',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }

        self.url: str = NotImplementedError

        self.payload: str = NotImplementedError


    def _set_worker(self, mode: typing.Literal["personal", "acst"]) -> typing.Self:
        match mode:
            case "personal":
                self.url = 'https://naks.ru/registry/personal/'
                self.payload = 'arrFilter_pf%5Bap%5D=&arrFilter_ff%5BNAME%5D={name}&arrFilter_pf%5Bshifr_ac%5D=&arrFilter_pf%5Buroven_ac%5D=&arrFilter_pf%5Bnum_ac%5D=&arrFilter_ff%5BCODE%5D={kleymo}&arrFilter_DATE_CREATE_1=&arrFilter_DATE_CREATE_2=&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_DATE_ACTIVE_FROM_1=&arrFilter_DATE_ACTIVE_FROM_2=&g-recaptcha-response=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y'
                return self
            
            case "acst":
                self.url = 'https://naks.ru/registry/reg/st/?arrFilter_pf%5Bnum_sv%5D={acst}&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_ff%5BNAME%5D=&arrFilter_ff%5BPREVIEW_TEXT%5D=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y'
                return self
            case _:
                raise ValueError("Invalid http worker mode!")


    def _set_welder_request_data(self, search_value: str) -> str:
        data = self.payload

        if fullmatch(r"[A-Z0-9]{4}", search_value.strip()):
            data = data.format(kleymo=search_value.strip(), name="")
            return data
        
        name = repr(search_value.encode("windows-1251"))[2:-1].replace("\\x", "%").upper().replace(" ", "+")
        data = data.format(name=name, kleymo="")
        return data
    

    def _set_acst_request_url(self, search_value: str) -> str:
        url = self.url

        acst = repr(search_value.encode("windows-1251"))[2:-1].replace("\\x", "%").upper().replace(" ", "+")

        return url.format(acst=acst)
        

    def get_welder_page(self, value: str) -> MainPage:

        data = self._set_welder_request_data(value)
        res = self.session.post(self.url, data)
        sleep(1)

        return res.text
    

    def get_welder_certification_pages(self, links: list[str]) -> list[AdditionalPage]:
        additional_pages = []

        for link in links:
            additional_pages.append(self.session.get(link).text)
            sleep(.5)
        
        return additional_pages
    

    def get_acst_page(self, acst: str) -> MainPage:
        url = self._set_acst_request_url(acst)
        res = self.session.get(url)
        sleep(1)

        return res.text
