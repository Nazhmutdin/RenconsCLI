import typing as t
from datetime import datetime
from pathlib import Path

from click import Option, Command, echo

from src.commands.db_commands.welder_ndt_table_service import AddWelderNDTsService
from src.services import WelderDataBaseService, WelderCertificationDataBaseService
from src.repositories import UserRepository
from src.shemas import UserShema
from src.utils.funcs import load_json, hash_password
from src._types import UserData
from settings import Settings


__all__ = [
    "AddWeldersCommand",
    "UpdateWeldersCommand",
    "AddWelderCertificationsCommand",
    "AddWelderNDTsCommand",
    "AddUserCommand",
    "UpdateUserCommand",
    "DeleteUserCommand",
]


"""
====================================================================================
welder commands
====================================================================================
"""


class AddWeldersCommand(Command):
    def __init__(self) -> None:

        name = "add-welders"
        path_option = Option(["--path"], type=t.Union[str, Path], default=Settings.WELDERS_DATA_JSON())

        super().__init__(name=name, params=[path_option], callback=self.execute)


    def execute(self, path: str | Path) -> None:
        welders = load_json(path)
        service = WelderDataBaseService()

        for welder in welders:
            service.add(**welder)


class UpdateWeldersCommand(Command):
    def __init__(self) -> None:

        name = "update-welders"
        path_option = Option(["--path"], type=t.Union[str, Path], default=Settings.WELDERS_DATA_JSON())

        super().__init__(
            name=name,
            params=[path_option],
            callback=self.execute
        )

    def execute(self, path: str | Path) -> None:

        welders = load_json(path)
        service = WelderDataBaseService()

        for welder in welders:
            service.update(**welder)


"""
====================================================================================
welder certification commands
====================================================================================
"""


class AddWelderCertificationsCommand(Command):
    def __init__(self) -> None:

        name = "add-welder-certification"
        path_option = Option(["--path"], type=t.Union[str, Path], default=Settings.WELDERS_DATA_JSON())

        super().__init__(
            name=name,
            params=[path_option],
            callback=self.execute
        )


    def execute(self, path: str | Path) -> None:

        certifications = load_json(path)
        service = WelderCertificationDataBaseService()

        for certification in certifications:
            service.add(**certification)


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
        **kwargs: t.Unpack[UserData]
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
        **kwargs: t.Unpack[UserData]
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
