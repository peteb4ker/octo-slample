from __future__ import annotations

import click

import octo_slample.sampler as sampler


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
    """Initialize the sampler."""
    s = sampler.Sampler()
    for x in range(1, 9):
        s.set_sound(x, f"wavs/chan-00{x}.wav")

    return s


@click.command()
def loop():
    c = None
    click.clear()
    print_menu()

    s = init_sampler()
    c = click.getchar()

    while c != "q":
        click.clear()
        click.echo("Octo Slample")

        channel = read_valid_channel()
        if channel is None:
            continue

        if c == "q":
            break

        s.play_channel(channel)

        click.echo(f"Playing channel {channel}")


if __name__ == "__main__":
    loop()
