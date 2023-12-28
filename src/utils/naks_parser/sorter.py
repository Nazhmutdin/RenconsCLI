from src.utils.naks_parser.types import WelderData
from src.shemas import WelderShema, WelderCertificationShema


class Sorter:
    def _sort_welder_data(self, data: list[WelderData]) -> dict[str, list[WelderData]]:
        data_dict: dict[str, list[WelderData]] = {}

        for el in data:
            if el.kleymo not in data_dict:
                data_dict[el.kleymo] = [el]
                continue

            data_dict[el.kleymo].append(el)


        return data_dict
    

    def _select_name(self, data: list[WelderData]) -> str:
        name = data[0].name
        date = data[0].certification_date

        for el in data:
            if el.certification_date > date:
                name = el.name
                date = el.certification_date

        
        return name


    def sort_welder_data(self, data: list[WelderData]) -> list[WelderShema]:
        data_dict: dict[str, list[WelderData]] = self._sort_welder_data(data)
        result = []

        for kleymo, datas in data_dict.items():
            welder = WelderShema(
                name=self._select_name(datas),
                kleymo=kleymo
            )

            welder.certifications = [WelderCertificationShema.model_validate(el, from_attributes=True) for el in datas]

            result.append(welder)

        return result


    def sort_engineer_data(self, data: list) -> list: ...
