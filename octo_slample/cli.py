"""Command line interface for Octo Slample.

Octo Slample is a sampler that can play 8 channels at once.
"""


import click
from click import BadParameter, ClickException
from schema import SchemaError

from octo_slample.constants import DEFAULT_BPM
from octo_slample.sampler.looping_sampler import LoopingSampler
from octo_slample.sampler.sampler import Sampler


def read_valid_channel():
    """Read a valid channel from the user.

    Returns None if the user enters an invalid channel.

    Channels are 1-indexed.

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


def print_menu():
    """Print the menu."""
    click.echo("Octo Slample")
    click.echo("============")
    click.echo("1-8: Play channel")
    click.echo("q: Quit")


def init_sampler():
    """Initialize the sampler.

    Loads the sounds from the wavs directory.

    Returns:
        Sampler: The initialized sampler.
    """
    s = Sampler()
    for x in range(1, 9):
        s.bank[x].sample = f"wavs/chan-00{x}.wav"

    return s


@click.group()
def octo_slample():
    """Octo Slample command line interface."""
    pass


@octo_slample.command()
@click.option("--pattern", help="Pattern file", required=True, type=str)
@click.option("--bpm", default=DEFAULT_BPM, help="Beats per minute", type=int)
def loop(pattern: str, bpm: int):
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
        raise BadParameter(f"Invalid pattern file '{pattern}': {e}")
    except Exception as e:
        raise ClickException("Unknown Error: " + str(e))


@octo_slample.command()
def pads():
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

        s.play_channel(channel)

        click.echo(f"Playing channel {channel}")


if __name__ == "__main__":
    octo_slample()
