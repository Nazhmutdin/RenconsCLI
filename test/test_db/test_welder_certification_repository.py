import pytest

from src.repositories import WelderCertificationRepository, WelderRepository
from src.shemas import WelderCertificationShema


@pytest.mark.run(order=2)
class TestWelderCertificationRepository:
    repo = WelderCertificationRepository()

    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.usefixtures('welders')
    def test_add_welder_certification(self, welder_certifications: list[WelderCertificationShema]) -> None:

        assert WelderRepository().count() == 100
            
        for certification in welder_certifications:
            self.repo.add(certification)
            res = self.repo.get(certification.certification_id)

            assert res.certification_id == certification.certification_id

    
    @pytest.mark.parametrize(
            "id, expectation",
            [
                ("007bмр1гацi4291120230510", WelderCertificationShema),
                ("04pcюр2гацi2055620141016", WelderCertificationShema),
                ("04vnцр5ацi0702520221124", WelderCertificationShema),
            ]
    )
    def test_res_is_welder_certification_shema(self, id: int | str, expectation: WelderCertificationShema | None) -> None:
        assert type(self.repo.get(id)) == expectation


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 3, 4, 5, 6]
    )
    def test_get_welder_certification(self, index: int, welder_certifications: list[WelderCertificationShema]) -> None:
        certification = welder_certifications[index]
        assert self.repo.get(certification.certification_id) == certification


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 13, 63, 31, 75, 89]
    )
    def test_add_with_existing_welder_certification(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        self.repo.add(welder_certifications[index])

        assert self.repo.count() == len(welder_certifications)

    
    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 42, 76, 99, 33, 15]
    )
    def test_update_welder_certification(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        certification = welder_certifications[index]
        certification.gtd = ["111", "222"]

        self.repo.update(certification.certification_id, **certification.model_dump())
        updated_certification = self.repo.get(certification.certification_id)
        assert updated_certification.gtd == certification.gtd


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete_welder_certification(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        certification = welder_certifications[index]

        self.repo.delete(certification.certification_id)

        assert self.repo.get(certification.certification_id) == None
