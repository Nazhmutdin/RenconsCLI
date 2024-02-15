from click.testing import CliRunner
import pytest

from src.commands.db_commands.commands import *
from src.repositories import WelderRepository, WelderCertificationRepository
from src.shemas import WelderShema, WelderCertificationShema


runner = CliRunner()

class TestWelderDataBaseCommands:

    @pytest.mark.usefixtures('welders')
    def test_add_welders_command(self, welders: list[WelderShema]):
        repo = WelderRepository()
        AddWeldersCommand().execute("test/test_data/welders.json")

        for welder in welders:
            assert repo.get(welder.kleymo) == welder

        assert repo.count() == len(welders)

    
    @pytest.mark.usefixtures('welder_certifications')
    def test_add_welder_certifications_command(self, welder_certifications: list[WelderCertificationShema]):
        repo = WelderCertificationRepository()
        AddWelderCertificationsCommand().execute("test/test_data/welder_certifications.json")

        for certification in welder_certifications:
            assert repo.get(certification.certification_id) == certification

        assert repo.count() == len(welder_certifications)