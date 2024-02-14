from typing import TypeAlias, Self, Literal
from re import fullmatch
from time import sleep

from requests import Session, Response


"""
=======================================================================================================
Types
=======================================================================================================
"""


MainPage: TypeAlias = str
AdditionalPage: TypeAlias = str


"""
=======================================================================================================
Parser
=======================================================================================================
"""


def get_http_worker(mode: Literal["personal", "acst"]) -> "NaksHTTPWorker":
    return NaksHTTPWorker()._set_worker(mode)


class PersonalNaksHTTPService:
    def __init__(self) -> None:
        self.session = Session()

        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://naks.ru',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
        }

    
    def _detect_search_value_type(self, search_value: str) -> Literal["name", "kleymo", "certification_number"]:
        if fullmatch(r"[A-Z0-9]{4}", search_value): return "kleymo"
        
        elif fullmatch(r"[А-Я]+-[А-Я0-9]+-[IV]+-[0-9]+", search_value): return "certification_number"

        else: return "name" 


    def request_main_page(self, search_value: str) -> Response:
        payload_values: dict[str, str] = {
            "name": "",
            "cert_abbr": "",
            "cert_lvl": "",
            "cert_number": "",
            "kleymo": ""
        }
        
        search_value_type = self._detect_search_value_type(search_value)

        if search_value_type == "certification_number":
            args = search_value_type.split("-")
            payload_values.update(
                {
                    "cert_abbr": f"{args[0]}-{args[1]}",
                    "cert_lvl": f"{args[2]}",
                    "cert_number": f"{args[3]}"
                }
            )

        else: payload_values[search_value_type] = search_value
        
        payload: str = """
        arrFilter_pf%5Bap%5D=&arrFilter_ff%5BNAME%5D={name}&arrFilter_pf%5Bshifr_ac{cert_abbr}%5D=&arrFilter_pf%5Buroven_ac%5D={cert_lvl}&arrFilter_pf%5Bnum_ac%5D={cert_number}&arrFilter_ff%5BCODE%5D={kleymo}&arrFilter_DATE_CREATE_1=&arrFilter_DATE_CREATE_2=&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_DATE_ACTIVE_FROM_1=&arrFilter_DATE_ACTIVE_FROM_2=&g-recaptcha-response=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=
        """.format(**payload_values).strip()

        return self.session.post("https://naks.ru/registry/personal/", data=payload)


    def request_additional_page(self, id: str) -> Response:
        return self.session.get(f"https://naks.ru/registry/personal/detail.php?ID={id}")


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


    def _set_worker(self, mode: Literal["personal", "acst"]) -> Self:
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
