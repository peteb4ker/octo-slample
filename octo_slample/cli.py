"""Command line interface for Octo Slample.

Octo Slample is a sampler that can play 8 channels at once.
"""

import traceback
from typing import Union

import click
from click import ClickException
from schema import SchemaError

from octo_slample.constants import DEFAULT_BPM
from octo_slample.pattern.json_pattern import JsonPattern
from octo_slample.sampler.json_sample_bank import JsonSampleBank
from octo_slample.sampler.looping_sampler import LoopingSampler
from octo_slample.sampler.sampler import Sampler
from octo_slample.wav_writer import WavWriter


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

        paths = WavWriter.write_bank(
            JsonSampleBank.from_file(bank), bank_number, output
        )

        click.echo("Exported:")
        for path in paths:
            click.echo(f"- {path}")

        click.echo("Done!")
    except Exception as e:
        traceback.print_exception(e)
        raise ClickException(f"Invalid bank file '{bank}': {e}")


if __name__ == "__main__":
    octo_slample()
