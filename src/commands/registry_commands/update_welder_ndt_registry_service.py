from datetime import date

from click import echo
from pydantic import BaseModel, Field
from openpyxl.worksheet.worksheet import Worksheet

from src.utils.excel_service import ExcelService
from src.repositories import WelderNDTRepository, WelderRepository
from src.shemas import WelderNDTShema, WelderShema, WelderCertificationShema
from settings import Settings


class WelderWelderNDTData(BaseModel):
    kleymo: str | None = Field(default=None)
    ndts: list[WelderNDTShema] | None = Field(default=None)
    welder: WelderShema | None = Field(default=None)
    RD_method_certification: str | None = Field(default="-")
    RD_method_certification_date: date | str = Field(default="-")
    RAD_method_certification: str | None = Field(default="-")
    RAD_method_certification_date: date | str = Field(default="-")
    MP_method_certification: str | None = Field(default="-")
    MP_method_certification_date: date | str = Field(default="-")
    MPG_method_certification: str | None = Field(default="-")
    MPG_method_certification_date: date | str = Field(default="-")


    def certifications_data(self) -> dict[str, str | date]:
        return {
            "RD_method_certification": self.RD_method_certification,
            "RD_method_certification_date": self.RD_method_certification_date,
            "RAD_method_certification": self.RAD_method_certification,
            "RAD_method_certification_date": self.RAD_method_certification_date,
            "MP_method_certification": self.MP_method_certification,
            "MP_method_certification_date": self.MP_method_certification_date,
            "MPG_method_certification": self.MPG_method_certification,
            "MPG_method_certification_date": self.MPG_method_certification_date
        }



class WelderNDTRegistryRow(BaseModel):
    name: str | None  = Field(default=None)
    kleymo: str | int = Field(default=None)
    comp: str | None = Field(default=None)
    subcon: str | None = Field(default=None)
    project: str | None = Field(default=None)
    welding_date: date = Field()
    total_weld_1: float | None = Field(default=None)
    total_ndt_1: float | None = Field(default=None)
    total_accepted_1: float | None = Field(default=None)
    total_repair_1: float | None = Field(default=None)
    repair_status_1: float | None = Field(default=None)
    total_weld_2: float | None = Field(default=None)
    total_ndt_2: float | None = Field(default=None)
    total_accepted_2: float | None = Field(default=None)
    total_repair_2: float | None = Field(default=None)
    repair_status_2: float | None = Field(default=None)
    total_weld_3: float | None = Field(default=None)
    total_ndt_3: float | None = Field(default=None)
    total_accepted_3: float | None = Field(default=None)
    total_repair_3: float | None = Field(default=None)
    repair_status_3: float | None = Field(default=None)
    RD_method_certification: str | None = Field(default="-")
    RD_method_certification_date: date | str = Field(default="-")
    RAD_method_certification: str | None = Field(default="-")
    RAD_method_certification_date: date | str = Field(default="-")
    MP_method_certification: str | None = Field(default="-")
    MP_method_certification_date: date | str = Field(default="-")
    MPG_method_certification: str | None = Field(default="-")
    MPG_method_certification_date: date | str = Field(default="-")


    def as_tuple(self) -> tuple[str | int | date | float | None]:
        return [value for value in self.model_dump().values()]


class UpdateWelderNDTRegistryService:

    def update_registry(self) -> None:
        wb = ExcelService.load_file(Settings.NDT_REGISTRY_PATH())
        welders = self._collect_welders()
        welder_ndts = self._collect_ndts()

        self.sorted_data = self._sort_welder_ndt_and_welder_shemas(welders, welder_ndts)
        self._set_certification_data()
        self.registry_row_dict: dict[str, WelderNDTRegistryRow] = {}
        ws: Worksheet = wb.active

        self._truncate_table(ws)

        rows = [ExcelService.data_to_cells([e] + row.as_tuple(), ws) for e, row in enumerate(self._get_rows())]
        rows = ExcelService.style_like_body_rows(rows)
        for row in rows:
            ws.append(row)

        wb.save(Settings.NDT_REGISTRY_PATH())


    def _truncate_table(self, ws: Worksheet) -> None:
        ws.delete_rows(idx=3, amount=ws.max_row)


    def _get_certification_date_number(self, method: str, certifications: list[WelderCertificationShema]) -> date | None:
        dates = {certification.certification_number: certification.certification_date for certification in certifications if certification.method == method}

        max_date = "-"
        certification_number = "-"

        for cert_number, certification_date in dates.items():
            if max_date == "-":
                max_date = certification_date
                certification_number = cert_number
                continue

            if certification_date > max_date:
                max_date = certification_date
                certification_number = cert_number

        return (certification_number, max_date)
    

    def _get_rows(self) -> list[WelderNDTRegistryRow]:
        result: dict[str, list[WelderNDTRegistryRow]] = {}

        for value in self.sorted_data.values():
            for ndt in value.ndts:
                key = f"{ndt.kleymo}{ndt.comp}{ndt.subcon}{ndt.project}".lower()

                if key not in result:
                    result[key] = [
                            WelderNDTRegistryRow(
                            name=value.welder.name,
                            **ndt.model_dump(),
                            **value.certifications_data()
                        )
                    ]

                if key in result:
                    new_row = WelderNDTRegistryRow(
                        name=value.welder.name,
                        **ndt.model_dump(),
                        **value.certifications_data()
                    )

                    result[key].append(new_row)

        
        return [self._choose_max_row(value) for value in result.values()]
    

    def _choose_max_row(self, rows: list[WelderNDTRegistryRow]) -> WelderNDTRegistryRow:
        max_row = rows[0]

        for row in rows[1:]:
            if row.welding_date > max_row.welding_date:
                max_row = row

        return max_row


    def _set_certification_data(self) -> None:
        for value in self.sorted_data.values():
            RD_method_certification, RD_method_certification_date = self._get_certification_date_number("РД", certifications=value.welder.certifications)
            RAD_method_certification, RAD_method_certification_date = self._get_certification_date_number("РАД", certifications=value.welder.certifications) 
            MP_method_certification, MP_method_certification_date = self._get_certification_date_number("МП", certifications=value.welder.certifications)
            MPG_method_certification, MPG_method_certification_date = self._get_certification_date_number("МПГ", certifications=value.welder.certifications)

            value.RD_method_certification = RD_method_certification
            value.RD_method_certification_date = RD_method_certification_date
            value.RAD_method_certification = RAD_method_certification
            value.RAD_method_certification_date = RAD_method_certification_date
            value.MP_method_certification = MP_method_certification
            value.MP_method_certification_date = MP_method_certification_date
            value.MPG_method_certification = MPG_method_certification
            value.MPG_method_certification_date = MPG_method_certification_date



    def _collect_ndts(self) -> list[WelderNDTShema]:
        repo = WelderNDTRepository()

        return repo.get_many()
    

    def _collect_welders(self) -> list[WelderShema]:
        repo = WelderRepository()

        return repo.get_many()
    

    def _sort_welder_ndt_and_welder_shemas(self, welders: list[WelderShema], welder_ndts: list[WelderNDTShema]) -> dict[str, WelderWelderNDTData]:
        result: dict[str, WelderWelderNDTData] = {}

        for ndt in welder_ndts:
            if ndt.kleymo not in result:
                result[ndt.kleymo] = WelderWelderNDTData(
                    kleymo = ndt.kleymo,
                    ndts = [ndt]
                )

            if ndt.kleymo in result:
                result[ndt.kleymo].ndts.append(ndt)

        
        for welder in welders:
            if welder.kleymo in result:
                result[welder.kleymo].welder = welder

        return result
