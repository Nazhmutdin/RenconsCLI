import pytest
import json

from src.db_engine import Base, engine
from settings import Settings

from src.shemas import WelderShema, WelderCertificationShema, WelderNDTShema, UserShema
from src.repositories import WelderRepository, WelderCertificationRepository, WelderNDTRepository, UserRepository


settings = Settings()


@pytest.fixture(scope="package", autouse=True)
def prepare_db():
    assert settings.MODE() == "TEST"

    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def get_welders() -> list[WelderShema]:
    welders = json.load(open("test/test_data/welders.json", "r", encoding="utf-8"))
    return [WelderShema.model_validate(welder) for welder in welders]


def get_welder_certifications() -> list[WelderCertificationShema]:
    certifications = json.load(open("test/test_data/welder_certifications.json", "r", encoding="utf-8"))
    return [WelderCertificationShema.model_validate(certification) for certification in certifications]


def get_welder_ndts() -> list[WelderNDTShema]:
    ndts = json.load(open("test/test_data/welder_ndts.json", "r", encoding="utf-8"))
    return [WelderNDTShema.model_validate(ndt) for ndt in ndts]


def get_users() -> list[UserShema]:
    ndts = json.load(open("test/test_data/users.json", "r", encoding="utf-8"))
    return [UserShema.model_validate(ndt) for ndt in ndts]


@pytest.fixture
def welders() -> list[WelderShema]:
    return get_welders()


@pytest.fixture
def welder_certifications() -> list[WelderCertificationShema]:
    return get_welder_certifications()


@pytest.fixture
def welder_ndts() -> list[WelderNDTShema]:
    return get_welder_ndts()

@pytest.fixture
def users() -> list[UserShema]:
    return get_users()


@pytest.fixture
def test_welders() -> list[WelderShema]:
    welders = json.load(open("test/test_data/_test_welders.json", "r", encoding="utf-8"))
    return [WelderShema.model_validate(welder) for welder in welders]


@pytest.fixture
def test_welder_certifications() -> list[WelderCertificationShema]:
    certifications = json.load(open("test/test_data/_test_welder_certifications.json", "r", encoding="utf-8"))
    return [WelderCertificationShema.model_validate(certification) for certification in certifications]


@pytest.fixture
def test_welder_ndts() -> list[WelderNDTShema]:
    ndts = json.load(open("test/test_data/_test_welder_ndts.json", "r", encoding="utf-8"))
    return [WelderNDTShema.model_validate(ndt) for ndt in ndts]


@pytest.fixture(scope="class")
def add_data():
    welder_repo = WelderRepository()
    certification_repo = WelderCertificationRepository()
    ndt_repo = WelderNDTRepository()

    for welder in get_welders():
        welder_repo.add(welder)

    for certification in get_welder_certifications():
        certification_repo.add(certification)

    for ndt in get_welder_ndts():
        ndt_repo.add(ndt)


# @pytest.fixture(scope="session")
# def add_users():
#     repo = UserRepository()
#     users = json.load(open("test/test_data/users.json", "r", encoding="utf-8"))

#     for user in [UserShema.model_validate(user) for user in users]:
#         repo.add(user)
