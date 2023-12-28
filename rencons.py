import click

from src.commands import *


@click.group()
def cli(): ...


cli.add_command(ParseNaksWeldersCommand())
cli.add_command(SortWelderFilesCommand())
cli.add_command(AddWelderNDTsCommand())
cli.add_command(UpdateWelderNDTRegistryCommand())
cli.add_command(AddWeldersCommand())
cli.add_command(DownloadWelderNDTsCommand())
cli.add_command(UpdateWeldersCommand())
cli.add_command(ParseNaksACSTCommand())
cli.add_command(AddUserCommand())
cli.add_command(UpdateUserCommand())


if __name__ == "__main__":
    cli()

