from pathlib import Path

from json import load

from src.shemas import WelderShema


class WelderExtractor:

    def extract_from_json(path: str | Path) -> list[WelderShema]: 
        return [WelderShema.model_validate(el) for el in load(open(path, "r", encoding="utf-8"))]
    

    def extract_from_excel(path: str | Path) -> list[WelderShema]: ...