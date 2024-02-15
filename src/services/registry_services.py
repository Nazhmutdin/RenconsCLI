import typing as t

from openpyxl.worksheet.worksheet import Worksheet

from src.utils.excel_service import ExcelService
from src.services._types import WelderNDTRegistryRow, WelderMethodsData
from src.repositories import WelderNDTRepository, WelderRepository, WelderCertificationRepository
from src.shemas import WelderNDTShema, WelderShema, WelderCertificationShema
from settings import Settings


__all__ = [
    "WelderNDTRegistryService"
]


class WelderNDTRegistryService:

    def update_registry(self) -> None:
        ndts = self._collect_ndts()
        welders = self._collect_welders(ndts.keys())
        certifications = self._collect_welder_certifications(ndts.keys())
        wb = ExcelService.load_file(Settings.NDT_REGISTRY_PATH())
        ws: Worksheet = wb.active
        
        ws.delete_rows(idx=3, amount=ws.max_row)

        rows = []

        for welder in welders:
            data = self._welder_to_rows(welder, ndts[welder.kleymo], certifications[welder.kleymo])
            rows += [ExcelService.data_to_cells([None] + row.as_list(), ws) for row in data]

        ExcelService.style_like_body_rows(rows)

        for e, row in enumerate(rows, start=1):
            row[0].value = e
            ws.append(row)
            
        wb.save(Settings.NDT_REGISTRY_PATH())


    def _collect_welders(self, kleymos: t.Iterable[str | int]) -> list[WelderShema]:
        repo = WelderRepository()

        return [welder for welder in repo.get_many() if welder.kleymo in kleymos]
    

    def _collect_welder_certifications(self, kleymos: t.Iterable[str | int]) -> dict[str, list[WelderCertificationShema]]:
        repo =  WelderCertificationRepository()

        certs = [cert for cert in repo.get_many() if cert.kleymo in kleymos]

        data: dict[str, dict[str, WelderCertificationShema]] = {}
        for cert in certs:

            if cert.kleymo not in data:
                data[cert.kleymo] = {
                    cert.method: cert
                }

            else:
                if cert.method not in data[cert.kleymo]:
                    data[cert.kleymo] = data[cert.kleymo] | {cert.method: cert}
                else:
                    if cert.expiration_date_fact > data[cert.kleymo][cert.method].expiration_date_fact:
                        data[cert.kleymo][cert.method] = cert

        return data

    
    def _collect_ndts(self) -> dict[str, list[WelderNDTShema]]:
        repo = WelderNDTRepository()

        ndts = repo.get_many()
        data: dict[str, WelderNDTShema] = {}

        for ndt in ndts:
            ident = ndt.ndt_id[:-8]

            if ident not in data:
                data[ident] = ndt

            else:
                if ndt.welding_date > data[ident].welding_date:
                    data[ident] = ndt

        result: dict[str, list[WelderNDTShema]] = {}

        for ndt in data.values():
            if ndt.kleymo not in result:
                result[ndt.kleymo] = [ndt]
                continue

            result[ndt.kleymo].append(ndt)

        return result
    

    def _welder_to_rows(self, welder: WelderShema, ndts: list[WelderNDTShema], certifications: dict[str, WelderCertificationShema]) -> list[WelderNDTRegistryRow]:
        methods: WelderMethodsData = self._get_welder_methods_data(certifications)
        rows = []
        ids = []

        for ndt in ndts:
            id = ndt.ndt_id[:-8]

            if id not in ids:
                ids.append(id)
                rows.append(WelderNDTRegistryRow.model_validate(welder.model_dump() | methods.model_dump() | ndt.model_dump()))

        return rows


    def _get_welder_methods_data(self, certifications: dict[str, WelderCertificationShema]) -> WelderMethodsData:
        data = WelderMethodsData()
        for method, certification in certifications.items():
            match method:
                case "РД":
                    data.RD_method_certification, data.RD_method_certification_date = (certification.certification_number, certification.certification_date)
                case "РАД":
                    data.RAD_method_certification, data.RAD_method_certification_date = (certification.certification_number, certification.certification_date)
                case "МП":
                    data.MP_method_certification, data.MP_method_certification_date = (certification.certification_number, certification.certification_date)
                case "МПГ":
                    data.MPG_method_certification, data.MPG_method_certification_date = (certification.certification_number, certification.certification_date)

        return data
