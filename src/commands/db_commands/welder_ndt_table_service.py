from datetime import date
from os import listdir

from click import echo

from src.shemas import WelderNDTShema
from src.repositories import WelderNDTRepository
from settings import Settings
from src.utils.excel_service import ExcelService


class AddWelderNDTsService:

    def _get_file(self, folder: str) -> str | None:
        folder_path = f"{Settings.NDT_TABLES_DIR()}/{folder}"
        try:
            files = listdir(folder_path)
            if len(files) == 0:
                echo(f"{folder_path} is empty")
                return None
        except:
            echo("Invalid Path")
            return None
        
        return files[0]
    

    def _read_ndt_report(self, folder: str, file: str) -> list[list[str | int | float | date]]:
        wb = ExcelService.load_file(
            f"{Settings.NDT_TABLES_DIR()}/{folder}/{file}"
        )

        return ExcelService.read_worksheet_by_row(wb.active, min_row=4, values_only=True)
    

    def _row_ndt_data_to_shema(self, welder_ndt_row: list[str | int | float | date]) -> WelderNDTShema:
        return WelderNDTShema(
            kleymo=welder_ndt_row[4],
            comp=welder_ndt_row[8],
            subcon=welder_ndt_row[9],
            project=welder_ndt_row[10],
            welding_date=welder_ndt_row[11],
            total_weld_1=welder_ndt_row[12],
            total_ndt_1=welder_ndt_row[13],
            total_accepted_1=welder_ndt_row[14],
            total_repair_1=welder_ndt_row[15],
            repair_status_1=welder_ndt_row[16],
            total_weld_2=welder_ndt_row[17],
            total_ndt_2=welder_ndt_row[18],
            total_accepted_2=welder_ndt_row[19],
            total_repair_2=welder_ndt_row[20],
            repair_status_2=welder_ndt_row[21],
            total_weld_3=welder_ndt_row[22],
            total_ndt_3=welder_ndt_row[23],
            total_accepted_3=welder_ndt_row[24],
            total_repair_3=welder_ndt_row[25],
            repair_status_3=welder_ndt_row[26],
            ndt_id=WelderNDTShema.compute_ndt_id(
                kleymo=welder_ndt_row[4],
                comp=welder_ndt_row[8],
                subcomp=welder_ndt_row[9],
                project=welder_ndt_row[10],
                welding_date=welder_ndt_row[11]
            )
        )


    def _read(self, folder: str, file: str) -> list[WelderNDTShema] | None:
        if file == "*":
            file = self._get_file(folder)

            if not file:
                return None
            
        data = self._read_ndt_report(folder, file)
        return [self._row_ndt_data_to_shema(el) for el in data]

 
    def add_ndts(self, folder: str, file: str) -> None:
        repo = WelderNDTRepository()
        
        for ndt in self._read(folder, file):
            try:
                repo.add(ndt)
            except:
                echo("Invalid data")
