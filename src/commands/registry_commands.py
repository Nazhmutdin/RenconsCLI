from click import Option, Command

from src.services import WelderNDTRegistryService


class UpdateWelderNDTRegistryCommand(Command):
    def __init__(self) -> None:

        name = "update-ndt-registry"

        super().__init__(name=name, callback=self.execute)


    def execute(self) -> None:
        WelderNDTRegistryService().update_registry()
