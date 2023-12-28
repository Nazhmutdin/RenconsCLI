from time import sleep

from click import Option, Command, echo

from src.commands.db_commands.add_welder_ndts_service import AddWelderNDTsService
from src.commands.db_commands.load_welder_ndts_service import LoadWelderNDTsService
from src.repositories import WelderRepository, WelderCertificationRepository
from src.shemas import WelderShema
from src.utils.funcs import load_json
from src.utils.progress_bar import init_progress_bar
from src.commands.db_commands.user_table_service import add_user, update_user
from settings import Settings


class AddWelderNDTsCommand(Command):
    def __init__(self) -> None:

        name = "add-welder-ndts"

        folder_option = Option(["--folder"], type=str)
        file_option = Option(["--file"], type=str, default="*")


        super().__init__(name=name, params=[folder_option, file_option], callback=self.execute)


    def execute(self, folder: str, file: str) -> None:
        AddWelderNDTsService().add_ndts(folder, file)


class AddWeldersCommand(Command):
    def __init__(self) -> None:

        name = "add-welders"

        super().__init__(name=name, callback=self.execute)


    def execute(self) -> None:

        welders = [WelderShema.model_validate(welder) for welder in load_json(Settings.WELDERS_DATA_JSON())]

        welder_repo = WelderRepository()
        welder_cert_repo = WelderCertificationRepository()
        progress = init_progress_bar("[blue]Adding...")
        progress.start()
        task = progress.add_task("[blue]Adding...", total=len(welders))

        for welder in welders:
            welder_repo.add(welder)

            for certification in welder.certifications:
                welder_cert_repo.add(certification)

            progress.update(task, advance=1)
        
        sleep(.1)


class UpdateWeldersCommand(Command):
    def __init__(self) -> None:

        name = "update-welders"

        super().__init__(name=name, callback=self.execute)


    def execute(self) -> None:

        welders = [WelderShema.model_validate(welder) for welder in load_json(Settings.WELDERS_DATA_JSON())]

        welder_repo = WelderRepository()
        welder_cert_repo = WelderCertificationRepository()

        progress = init_progress_bar("[blue]Updating...")
        progress.start()
        task = progress.add_task("[blue]Updating...", total=len(welders))

        for welder in welders:
            welder_repo.update(welder)

            for certification in welder.certifications:
                welder_cert_repo.update(certification)

            progress.update(task, advance=1)
        
        sleep(.1)


class DownloadWelderNDTsCommand(Command):
    def __init__(self) -> None:

        name = "download-welder-ndts"

        file_name_option = Option(["--file-name"], type=str, help="support .json, .xlsx formats")
        welding_date_from_option = Option(["--welding-date-from"], type=str, default="-")
        welding_date_before_option = Option(["--welding-date-before"], type=str, default="-")

        super().__init__(name=name, params=[file_name_option, welding_date_from_option, welding_date_before_option], callback=self.execute)


    def execute(self, file_name: str, welding_date_from: str, welding_date_before: str) -> None:
        try:
            LoadWelderNDTsService().load_ndts(file_name=file_name, welding_date_from=welding_date_from, welding_date_before=welding_date_before)
        except ValueError:
            echo("Invalid file format")


class AddUserCommand(Command):
    def __init__(self) -> None:

        name = "add-user"

        name_option = Option(["--name", "-n"], type=str, default=None)
        login_option = Option(["--login", "-l"], type=str, default=None)
        password_option = Option(["--password", "-p"], type=str, default=None)
        email_option = Option(["--email", "-e"], type=str, default=None)
        is_superuser_option = Option(["--is_superuser", "-su"], type=bool, default=False)

        super().__init__(
            name=name, 
            params=[name_option, login_option, password_option, email_option, is_superuser_option], 
            callback=self.execute
        )


    def _check_input_data(
        self, 
        name: str | None, 
        login: str | None,
        password: str | None
    ) -> bool:
        if name and login and password:
            return True
        
        return False

    
    def execute(
        self, 
        name: str | None, 
        login: str | None,
        password: str | None,
        email: str | None,
        is_superuser: bool | None
    ) -> None:
        if not self._check_input_data(name, login, password):
            echo("name, login and password are required!")
            return

        add_user(
            name=name,
            login=login,
            password=password,
            email=email,
            is_superuser=is_superuser
        )
        echo("User successfully added!")


class UpdateUserCommand(Command):
    def __init__(self) -> None:

        name = "update-user"

        name_option = Option(["--name", "-n"], type=str, default=None)
        login_option = Option(["--login", "-l"], type=str, default=None)
        password_option = Option(["--password", "-p"], type=str, default=None)
        email_option = Option(["--email", "-e"], type=str, default=None)
        is_superuser_option = Option(["--is_superuser", "-su"], type=bool, default=False)

        super().__init__(
            name=name, 
            params=[name_option, login_option, password_option, email_option, is_superuser_option], 
            callback=self.execute
        )

    
    def execute(
        self, 
        name: str | None, 
        login: str | None,
        password: str | None,
        email: str | None,
        is_superuser: bool | None
    ) -> None:
        if not login:
            echo("login is required!")
            return

        update_user(
            login=login,
            name=name,
            password=password,
            email=email,
            is_superuser=is_superuser
        )
        echo("User successfully updated!")
