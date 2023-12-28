from abc import ABC, abstractmethod
import re
from datetime import date

from lxml import html
from dateutil.relativedelta import relativedelta

from src.utils.funcs import str_to_date
from src.shemas import WelderCertificationShema, ACSTShema
from src.utils.naks_parser.types import WelderData


"""
=======================================================================================================
Extractors
=======================================================================================================
"""



def extract_links(welder_page: str) -> list[str]:
    tree: html.HtmlElement = html.fromstring(welder_page)
    links = tree.xpath("//tr[@bgcolor]/td[13]/a/@onclick")
    links = [re.search(r"/[\w]+/[\w]+/detail.php\?ID=[\w\W]+", link)[0].replace('"', '').split(",")[0] for link in links]

    links = [f"https://naks.ru{link}" for link in links]

    return links


class WelderDataExtractor:
    def __init__(self) -> None:
        self.methods = {
            "Толщина деталей, мм": self.__extract_details_thikness,
            "Наружный диаметр, мм": self.__extract_outer_diameter,
            "Диаметр стержня, мм": self.__extract_rod_diameter,
            "Диаметр деталей, мм": self.__extract_details_diameter,
            "Группы технических устройств опасных производственных объектов:": self.__extract_gtd,
            "Вид деталей": self.__extract_details_type,
            "Типы швов": self.__extract_joint_type,
            "Группа свариваемого материала": self.__extract_groups_materials_for_welding
        }

    
    def extract(self, main_page: str, additional_pages: list[str]) -> list[WelderData]:
        result = []

        main_page_data = self._extract_data_from_welder_page(main_page)

        for page_index in range(len(additional_pages)):
            additional_page_data = self._extract_data_from_welder_certification_page(
                additional_pages[page_index]
            )
            # if not main_page_data[page_index].get("additional_page_data")

            data = main_page_data[page_index] | additional_page_data

            if data["kleymo"] != None:
                result.append(
                    WelderData.model_validate(data)
                )

        return result


    def _extract_data_from_welder_page(self, welder_page: str) -> list[dict[str, str | date | None]]:
        result = []
        tree: html.HtmlElement = html.fromstring(welder_page)

        trs = tree.xpath("//tr[@bgcolor]")

        for tr in trs:
            row_tree: html.HtmlElement = html.fromstring(html.tostring(tr))
            name = row_tree.xpath("//tr[@bgcolor]/td[1]/text()")[0].strip()
            try:
                kleymo = row_tree.xpath("//tr[@bgcolor]/td[2]/span/text()")[0].strip()
            except:
                kleymo = None
            company = row_tree.xpath("//tr[@bgcolor]/td[3]/text()")[0].strip()
            job_title = row_tree.xpath("//tr[@bgcolor]/td[4]/text()")[0].strip()
            certification_number = row_tree.xpath("//tr[@bgcolor]/td[5]/text()")[0].strip()
            insert = row_tree.xpath("//tr[@bgcolor]/td[6]/text()")[0].strip()
            certification_date = str_to_date(row_tree.xpath("//tr[@bgcolor]/td[9]/text()")[0].strip())
            expiration_date = str_to_date(row_tree.xpath("//tr[@bgcolor]/td[10]/text()")[0].strip())
            expiration_date_fact = str_to_date(row_tree.xpath("//tr[@bgcolor]/td[11]/text()")[0].strip())
            
            if expiration_date == None:
                expiration_date = certification_date + relativedelta(years=2)

            if expiration_date_fact == None:
                expiration_date_fact = expiration_date


            result.append({
                "name": name,
                "kleymo": kleymo,
                "company": company,
                "job_title": job_title,
                "certification_number": certification_number,
                "insert": insert,
                "certification_date": certification_date,
                "expiration_date": expiration_date,
                "expiration_date_fact": expiration_date_fact,
                "certification_id": WelderCertificationShema.compute_certification_id(kleymo, certification_number, certification_date, insert)
                }
            )

        return result


    def _extract_data_from_welder_certification_page(self, welder_certification_page: str) -> dict[str, str]:
        result = {}
        tree: html.HtmlElement = html.fromstring(welder_certification_page)

        trs: list[html.HtmlElement] = tree.xpath("//tr")

        for tr in trs:
            tds: list[html.HtmlElement] = tr.getchildren()

            if len(tds) < 2:
                continue

            key = tds[0].text

            value = ", ".join([td.text_content() for td in tds[1:]])

            method = self.methods.get(key)

            if method == None:
                result[key] = value
                continue

            method(value, result)

        return result
    

    def __extract_details_thikness(self, value: str, result: dict[str, str]) -> None:
        key = "details_thikness"

        self.__extract_from_before_values(value, result, key)
    

    def __extract_outer_diameter(self, value: str, result: dict[str, str]) -> None:
        key = "outer_diameter"

        self.__extract_from_before_values(value, result, key)


    def __extract_rod_diameter(self, value: str, result: dict[str, str]) -> None:
        key = "rod_diameter"

        self.__extract_from_before_values(value, result, key)


    def __extract_details_diameter(self, value: str, result: dict[str, str]) -> None:
        key = "details_diameter"

        self.__extract_from_before_values(value, result, key)


    def __extract_from_before_values(self, value: str, result: dict[str, str], key: str) -> None:

        if not value:
            self.__change_dict(result, key)
            return None
        
        value = value.replace("свыше", "от").replace("Свыше", "от")
        value = re.sub(r"[ ]+", " ", value)
        from_value, before_value = self.__get_from_before_values(value)

        self.__change_dict(result, key, from_value, before_value)


    def __extract_gtd(self, value: str, result: dict[str, str]) -> None:
        output: list[str] = []

        if not value:
            result["gtd"] = []
            return None
        
        number_pattern = re.compile(r"[0-9]+[.,][0-9]+|[0-9]+")

        for gtd in value.split("),"):
            values = gtd.split("(")
            try:
                gtd_type = self.__get_gtd_abbr(values[0].strip().lower())

                for number in number_pattern.findall(values[1]):
                    value = f"{gtd_type}({number})"
                    if value not in output:
                        output.append(value)
            except:
                pass

        result["gtd"] = output
    

    def __extract_details_type(self, value: str, result: dict[str, str]) -> None:

        if not value:
            result["details_type"] = None
            return None

        value = re.sub(r"[\[\(][\w\W]+[\]\)]", " ", value)
        result["details_type"] = list(set(re.findall(r"[А-Я+]+", value)))


    def __extract_joint_type(self, value: str, result: dict[str, str]) -> None:

        if not value:
            result["joint_type"] = None
            return None

        value = re.sub(r"[\[\(][\w\W]+[\]\)]", " ", value)
        result["joint_type"] = list(set(re.findall(r"[А-Я+]+", value)))
        

    def __extract_groups_materials_for_welding(self, value: str, result: dict[str, str]) -> None:

        if not value:
            result["groups_materials_for_welding"] = None
        
        value = value.replace("М", "M")

        value = re.sub(r"[\[\(][\w\W]+[\]\)]", " ", value)

        value = list(set(re.findall(r"[M0-9+]+", value)))
        result["groups_materials_for_welding"] = value


    def __get_gtd_abbr(self, gtd_name: str) -> str:
        if "нефтеперераб" in gtd_name and "взрывопожа" in gtd_name:
            return "ОХНВП"
        if "котел" in gtd_name and "оборуд" in gtd_name: 
            return "КО"
        if "нефтегазо" in gtd_name and "оборуд" in gtd_name:
            return "НГДО"
        if "газ" in gtd_name and "оборуд" in gtd_name:
            return "ГО"
        if "строит" in gtd_name and "констру" in gtd_name:
            return "СК"
        if "горнодоб" in gtd_name and "оборуд" in gtd_name:
            return "ГДО"
        if "металлур" in gtd_name and "оборуд" in gtd_name:
            return "МО"
        if "подъемно-транспортное" in gtd_name and "оборуд" in gtd_name:
            return "ПТО"
        if "сталь" in gtd_name and "мост" in gtd_name:
            return "КСМ"
        if "трансп" in gtd_name and "груз" in gtd_name:
            return "ОТОГ"
        
    
    def __get_from_before_values(self, string: str) -> tuple[float, float]:
        value_from = re.compile(r"от [0-9]+[.,][0-9]+|от [0-9]+")
        value_before= re.compile(r"до [0-9]+[.,][0-9]+|до [0-9]+")

        from_strings: list[str] = value_from.findall(string)
        before_strings: list[str] = value_before.findall(string)

        from_value = min([float(value.strip().replace("от ", "").replace(",", ".").strip()) for value in from_strings]) if from_strings != [] else None
        before_value = max([float(value.strip().replace("до ", "").replace(",", ".").strip()) for value in before_strings]) if before_strings != [] else None

        return (from_value, before_value)
    

    def __change_dict(self, data_dict: dict[str, str], key: str, from_value: float | None = None, before_value: float | None = None) -> None:
        data_dict[f"{key}_from"] = from_value
        data_dict[f"{key}_before"] = before_value
        


class EngineerDataExtractor: ...


class ACSTDataExtractor: 
    def extract(self, main_page: str) -> ACSTShema:
        tree: html.HtmlElement = html.fromstring(main_page)

        acst = tree.xpath("//tr[@bgcolor]/td[6]/text()")[0].strip()
        company = tree.xpath("//tr[@bgcolor]/td[1]/text()")[0].strip()

        return ACSTShema(
            acst=acst,
            company=company
        )
