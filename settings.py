import os
from pathlib import Path

from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseModel):

    @classmethod
    def DB_NAME(cls) -> str:
        return os.getenv("DATABASE_NAME")
    
    @classmethod
    def DB_PASSWORD(cls) -> str:
        return os.getenv("DATABASE_PASSWORD")
    
    @classmethod
    def HOST(cls) -> str:
        return os.getenv("HOST")
    
    @classmethod
    def USER(cls) -> str:
        return os.getenv("USER")
    
    @classmethod
    def PORT(cls) -> str:
        return os.getenv("PORT")
    
    @classmethod
    def MODE(cls) -> str:
        return os.getenv("MODE")
    
    @classmethod
    def BASE_DIR(cls) -> Path:
        return Path.cwd()
    
    @classmethod
    def STATIC_DIR(cls) -> Path:
        return Path(f"{cls.BASE_DIR()}/static")

    @classmethod
    def GROUPS_DIR(cls) -> Path:
        return Path(f"{cls.STATIC_DIR()}/groups")

    @classmethod
    def SRC_DIR(cls) -> Path:
        return Path(f"{cls.STATIC_DIR()}/src")

    @classmethod
    def PROCESSED_DIR(cls) -> Path:
        return Path(f"{cls.STATIC_DIR()}/processed")
    
    @classmethod
    def NDT_TABLES_DIR(cls) -> Path:
        return Path(f"{cls.STATIC_DIR()}/ndt_tables")
    
    @classmethod
    def WELDERS_DATA_JSON(cls) -> Path:
        return Path(f"{cls.STATIC_DIR()}/welders_certifications.json")
    
    @classmethod
    def ACSTS_DATA_JSON(cls) -> Path:
        return Path(f"{cls.STATIC_DIR()}/acsts.json")
    
    @classmethod
    def SEARCH_VALUES_FILE(cls) -> Path:
        return Path(f"{cls.STATIC_DIR()}/search_settings.json")
    

    @classmethod
    def NDT_REGISTRY_PATH(cls) -> Path:
        return Path(f"{Settings.STATIC_DIR()}/ndt_registry.xlsx")
