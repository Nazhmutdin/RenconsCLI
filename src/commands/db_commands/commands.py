from time import sleep
from typing import TypedDict, Unpack
from datetime import datetime, date

from click import Option, Command, echo

from src.commands.db_commands.welder_ndt_table_service import AddWelderNDTsService
from src.repositories import WelderRepository, WelderCertificationRepository, UserRepository
from src.shemas import WelderShema, UserShema
from src.utils.funcs import load_json, hash_password
from src.utils.progress_bar import init_progress_bar
from passlib.hash import sha256_crypt
from settings import Settings



"""
====================================================================================
welder commands
====================================================================================
"""


class WelderDict(TypedDict):
    kleymo: str
    name: str
    birthday: date
    passport_id: str
    sicil_number: str
    nation: str
    status: int


class AddWeldersCommand(Command):
    def __init__(self) -> None:

        name = "add-welders"

        super().__init__(name=name, callback=self.execute)


    def execute(self) -> None:

        welders = [WelderShema.model_validate(welder) for welder in load_json(Settings.WELDERS_DATA_JSON())]

        welder_repo = WelderRepository()
        progress = init_progress_bar("[blue]Adding...")
        progress.start()
        task = progress.add_task("[blue]Adding...", total=len(welders))

        for welder in welders:
            welder_repo.add(welder)

            progress.update(task, advance=1)
        
        sleep(.1)


class UpdateWeldersCommand(Command):
    def __init__(self) -> None:

        name = "update-welders"

        super().__init__(
            name=name,
            callback=self.execute
        )

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


"""
====================================================================================
welder certification commands
====================================================================================
"""


class AddWelderCertificationsCommand(Command):
    def __init__(self) -> None:

        name = "add-welder-certification"

        super().__init__(name=name, callback=self.execute)


    def execute(self) -> None:

        welders = [WelderShema.model_validate(welder) for welder in load_json(Settings.WELDERS_DATA_JSON())]

        repo = WelderCertificationRepository()
        progress = init_progress_bar("[blue]Adding...")
        progress.start()
        task = progress.add_task("[blue]Adding...", total=len(welders))

        for welder in welders:
            for certification in welder.certifications:
                repo.add(certification)

            progress.update(task, advance=1)
        
        sleep(.1)


"""
====================================================================================
welder ndt commands
====================================================================================
"""


class AddWelderNDTsCommand(Command):
    def __init__(self) -> None:

        name = "add-welder-ndts"

        folder_option = Option(["--folder"], type=str)
        file_option = Option(["--file"], type=str, default="*")


        super().__init__(name=name, params=[folder_option, file_option], callback=self.execute)


    def execute(self, folder: str, file: str) -> None:
        AddWelderNDTsService().add_ndts(folder, file)


"""
====================================================================================
user commands
====================================================================================
"""


class UserDict(TypedDict):
    name: str
    login: str
    password: str
    email: str | None
    is_active: bool
    is_superuser: bool


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
        **kwargs: Unpack[UserDict]
    ) -> None:
        if not self._check_input_data(kwargs["name"], kwargs["login"], kwargs["password"]):
            echo("name, login and password are required!")
            return
        
        repo = UserRepository()

        kwargs["hashed_password"] = hash_password(kwargs["password"])
        user = UserShema.model_validate(kwargs, from_attributes=True)

        user.sign_date = datetime.utcnow()
        user.login_date = datetime.utcnow()
        user.update_date = datetime.utcnow()
        repo.add(user)
        echo("User successfully added!")


class UpdateUserCommand(Command):
    def __init__(self) -> None:

        name = "update-user"

        name_option = Option(["--name", "-n"], type=str)
        login_option = Option(["--login", "-l"], type=str)
        password_option = Option(["--password", "-p"], type=str)
        email_option = Option(["--email", "-e"], type=str)
        is_superuser_option = Option(["--is_superuser", "-su"], type=bool)

        super().__init__(
            name=name, 
            params=[name_option, login_option, password_option, email_option, is_superuser_option], 
            callback=self.execute
        )


    def execute(
        self, 
        **kwargs: Unpack[UserDict]
    ) -> None:
        if not kwargs["login"]:
            echo("login is required!")
            return

        repo = UserRepository()

        kwargs = {key: value for key, value in kwargs.items() if value != None}

        if kwargs.get("password"):
            password = kwargs.pop("password")
            kwargs["hashed_password"] = hash_password(password)

        kwargs["update_date"] = datetime.utcnow()
        repo.update(kwargs["login"], **kwargs)
        echo("User successfully updated!")


class DeleteUserCommand(Command):
    def __init__(self) -> None:

        name = "delete-user"

        login_option = Option(["--login", "-l"], type=str)

        super().__init__(name=name, params=[login_option], callback=self.execute)

    
    def execute(self, login: str) -> None: 
        UserRepository().delete(login)
        echo("User successfully deleted!")
