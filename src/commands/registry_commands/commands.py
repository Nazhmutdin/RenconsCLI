from click import Option, Command

from src.commands.registry_commands.update_welder_ndt_registry_service import UpdateWelderNDTRegistryService


class UpdateWelderNDTRegistryCommand(Command):
    def __init__(self) -> None:

        name = "update-welder-ndt-registry"

        super().__init__(name=name, callback=self.execute)


    def execute(self) -> None:
        UpdateWelderNDTRegistryService().update_registry()
