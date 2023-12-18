from src.utils.naks_parser.types import WelderData
from src.shemas import WelderShema, WelderCertificationShema


class Sorter:

    def sort_welder_data(self, data: list[WelderData]) -> list[WelderShema]:
        data_dict: dict[str, WelderShema] = {}

        for el in data:
            if el.kleymo not in data_dict:
                
                if el.kleymo == None:
                    continue

                welder = WelderShema.model_validate(el, from_attributes=True)
                welder.certifications = [WelderCertificationShema.model_validate(el, from_attributes=True)]
                data_dict[el.kleymo] = welder
                continue

            data_dict[el.kleymo].certifications.append(WelderCertificationShema.model_validate(el, from_attributes=True))

        return list(data_dict.values())


    def sort_engineer_data(self, data: list) -> list: ...
