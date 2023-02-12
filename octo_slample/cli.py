"""Command line interface for Octo Slample.

Octo Slample is a sampler that can play 8 channels at once.
"""

import traceback

import click
from click import ClickException
from schema import SchemaError

from octo_slample.constants import DEFAULT_BPM
from octo_slample.json_pattern_bank import JsonPatternBank
from octo_slample.sampler.looping_sampler import LoopingSampler
from octo_slample.sampler.sampler import Sampler
from octo_slample.wav_writer import WavWriter


def read_valid_channel() -> int:
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


def print_menu() -> None:
    """Print the menu."""
    click.echo("Octo Slample")
    click.echo("============")
    click.echo("1-8: Play channel")
    click.echo("q: Quit")


def init_sampler() -> Sampler:
    """Initialize the sampler.

    Loads the sounds from the wavs directory.

    Returns:
        Sampler: The initialized sampler.
    """
    s = Sampler()
    for x in range(0, 8):
        s.bank[x].sample = f"wavs/chan-00{x + 1}.wav"

    return s


@click.group()
def octo_slample() -> None:
    """Octo Slample command line interface."""
    pass


@octo_slample.command()
@click.option("--pattern", help="Pattern file", required=True, type=str)
@click.option("--bpm", default=DEFAULT_BPM, help="Beats per minute", type=int)
def loop(pattern: str, bpm: int) -> None:
    """Run the loop mode.

    In loop mode, the loop is played continuously.
    """
    try:
        s = LoopingSampler.from_pattern_file(pattern, bpm=bpm)
        click.echo("Playing pattern: \n")
        click.echo(s.pattern)
        s.clock.start()
        s.loop()
    except SchemaError as e:
        raise ClickException(f"Invalid pattern file '{pattern}': {e}")
    except Exception as e:
        raise ClickException("Unknown Error: " + str(e))


@octo_slample.command()
def pads() -> None:
    """Run the pads mode.

    In pads mode, the user can play channels by pressing the corresponding
    number key.

    The user can quit by pressing `0`.
    """
    click.clear()
    print_menu()

    s = init_sampler()

    while (channel := read_valid_channel()) != 0:
        if channel is None:
            continue

        click.clear()
        click.echo("Octo Slample")

        # subtract 1 to convert from 1-indexed to 0-indexed
        s.play_channel(channel - 1)

        click.echo(f"Playing channel {channel}")


@octo_slample.command()
@click.option("--pattern", "-p", help="Pattern file", required=True, type=str)
@click.option("--bank-number", "-b", help="Bank number", required=True, type=int)
@click.option("--output", "-o", help="Output path", required=True, type=str)
def export(pattern: str, bank_number: int, output: str) -> None:
    """Export a bank to a set of wav files."""
    try:
        pattern_bank = JsonPatternBank.from_file(pattern)

        click.echo("Exporting bank to Squid format...")

        paths = WavWriter.write_bank(pattern_bank.bank, bank_number, output)

        click.echo("Exported:")
        for path in paths:
            click.echo(f"- {path}")

        click.echo("Done!")
    except Exception as e:
        traceback.print_exception(e)
        raise ClickException(f"Invalid pattern file '{pattern}': {e}")


if __name__ == "__main__":
    octo_slample()
