import typing


class LoadWelderNDTsService:

    def load_ndts(self, file_name: str, **kwargs) -> None | typing.NoReturn:
        save_format = self._detect_save_format(file_name)

        if save_format == "null":
            raise ValueError("Invalid file format")
        

    def _detect_save_format(self, file_name: str) -> typing.Literal["json", "excel", "null"]:
        extension = file_name.split(".")[-1]

        match extension:
            case "xlsx":
                return "excel"
            
            case "json":
                return "json"
            
            case _:
                return "null"
