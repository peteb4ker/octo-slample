"""Command line interface for Octo Slample.

Octo Slample is a sampler that can play 8 channels at once.
"""

import traceback
from pathlib import Path
from typing import Union

import click
from click import ClickException
from schema import SchemaError

from octo_slample.bank_exporter import BankExporter
from octo_slample.bank_initializer import BankInitializer
from octo_slample.constants import DEFAULT_BPM
from octo_slample.exception import BankExistsError
from octo_slample.pattern.json_pattern import JsonPattern
from octo_slample.sampler.json_sample_bank import JsonSampleBank
from octo_slample.sampler.looping_sampler import LoopingSampler
from octo_slample.sampler.sampler import Sampler


def read_valid_channel() -> Union[int, None]:
    """Read a valid channel from the user.

    Returns None if the user enters an invalid channel.

    Valid input channels are 1-8.
    For presentation purposes, channels are 1-indexed.
    Internally, channels are 0-indexed.

    Returns:
        int: The channel the user entered.
    """
    c = click.getchar()

    try:
        channel = int(c)
    except ValueError:
        return None

    if channel > 8:
        return None

    return channel


def print_pads_menu(sampler) -> None:
    """Print the menu."""
    click.echo("Octo Slample")
    click.echo("============")
    click.echo(sampler.bank)
    click.echo("1-8: Play channel")
    click.echo("q: Quit")


@click.group()
def octo_slample() -> None:
    """Octo Slample command line interface."""
    pass


@octo_slample.command()
@click.option("--pattern", "-p", help="Pattern file", required=True, type=str)
@click.option("--bank", "-b", help="Bank file", required=True, type=str)
@click.option("--bpm", default=DEFAULT_BPM, help="Beats per minute", type=int)
def loop(pattern: str, bank: str, bpm: int) -> None:
    """Run the loop mode.

    In loop mode, the loop is played continuously.

    Args:
        pattern (str): The pattern file.
        bank (str): The bank file.
        bpm (int): (Optional) Playback beats per minute.

    Raises:
        ClickException: If an error occurred.
    """
    try:
        s = LoopingSampler(
            bpm=bpm,
            pattern=JsonPattern.from_file(pattern),
            bank=JsonSampleBank.from_file(bank),
        )
        click.echo("Playing pattern: \n")
        click.echo(s.pattern)
        s.clock.start()
        s.loop()
    except SchemaError as e:
        raise ClickException(f"{e}")
    except Exception as e:
        raise ClickException("Unknown Error: " + str(e))


@octo_slample.command()
@click.option("--bank", "-b", help="Bank file", required=True, type=str)
def pads(bank: str) -> None:
    """Run the pads mode.

    In pads mode, the user can play channels by pressing the corresponding
    number key.

    The user can quit by pressing `0`.

    Args:
        bank (str): The bank file.

    Raises:
        ClickException: If an error occurred.

    Returns:
        None: If the user quits.
    """
    click.clear()

    s = Sampler()
    s.bank = JsonSampleBank.from_file(bank)

    print_pads_menu(s)

    while (channel := read_valid_channel()) != 0:
        if channel is None:
            continue

        click.clear()
        print_pads_menu(s)

        # subtract 1 to convert from 1-indexed to 0-indexed
        s.play_channel(channel - 1)

        click.echo(f"Playing channel {channel}")


@octo_slample.command()
@click.option("--bank", "-b", help="Bank file", required=True, type=str)
@click.option("--bank-number", "-n", help="Bank number", required=True, type=int)
@click.option("--output", "-o", help="Output path", required=True, type=str)
def export(bank: str, bank_number: int, output: str) -> None:
    """Export a bank to a set of wav files."""
    try:
        click.echo("Exporting bank to Squid format...")

        paths = BankExporter.export_bank(bank, bank_number, output)

        click.echo("Exported:")
        for path in paths:
            click.echo(f"- {path}")

        click.echo("Done!")
    except Exception as e:
        traceback.print_exception(e)
        raise ClickException(f"Invalid bank file '{bank}': {e}")


@octo_slample.command()
@click.argument("input_directory", type=click.Path(exists=True))
@click.argument("output_directory", type=click.Path(exists=False))
def export_set(input_directory: Path, output_directory: Path) -> None:
    """Export a set of banks to a Squid formatted Set.

    Usage:
        octo-slample export-set <input_directory> <output_directory>

    Args:
        input_directory (Path): The input directory. Must exist.
        output_directory (Path): The output directory. Does not need to exist.

    Raises:
        ClickException: If an error occurred.
    """
    try:
        click.echo(f"- Creating '{output_directory}' if it doesn't exist")
        BankExporter.create_directory(output_directory)

        click.echo(f"- Exporting banks in '{input_directory}' to '{output_directory}'")
        paths = BankExporter.export_set(input_directory, output_directory)

        for path in paths:
            click.echo(f" - {path}")
    except Exception as e:
        traceback.print_exception(e)
        raise ClickException(f"Export error: {e}")


@octo_slample.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="If true, overwrite an existing bank.json",
    required=False,
    type=bool,
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="If true, initialize all subdirectories",
    required=False,
    type=bool,
)
def init(directory: Path, force: bool = False, recursive: bool = False) -> None:
    """Initialize a sample directory."""
    try:
        if recursive:
            click.echo(f"Initializing sample directory '{directory}' recursively")
            BankInitializer.init_recursive(directory, force)
        else:
            BankInitializer.init(directory, force)

        click.echo(f"Initialized sample directory '{directory}'")
        click.echo(
            "Bank file can be found at 'bank.json' for name and description updates."
        )
    except BankExistsError:
        raise ClickException(f"Skipping as bank.json already exists in '{directory}'")
    except OSError as e:
        raise ClickException(
            f"Skipping as a {type(e).__name__} occurred while "
            + f"initializing '{directory}'"
        )


if __name__ == "__main__":
    octo_slample()
