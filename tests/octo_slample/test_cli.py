import pytest
from click.testing import CliRunner
from schema import SchemaError

import octo_slample.cli as cli


@pytest.fixture
def mock_looping_sampler_from_pattern_file(mocker):
    m = mocker.patch("octo_slample.cli.LoopingSampler.from_pattern_file")
    m.clock = mocker.Mock()
    m.loop = mocker.Mock()

    return m


@pytest.fixture
def mock_click_getchar(mocker):
    """Simulate the user clicking from 1-9, then x, then 0.

    1-8 are valid channels 9 is an invalid channel, which is ignored x
    is an invalid keeypress, which is ignored
    """
    m = mocker.patch("octo_slample.cli.click.getchar")
    m.side_effect = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "x", "0"]

    return m


@pytest.fixture
def mock_play_channel(mocker):
    return mocker.patch("octo_slample.cli.Sampler.play_channel")


def test_octo_slample_help():
    runner = CliRunner()
    result = runner.invoke(cli.octo_slample)

    assert result.exit_code == 0
    assert "Usage: octo-slample [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "  Octo Slample command line interface." in result.output
    assert "  --help  Show this message and exit." in result.output
    assert "Commands:" in result.output
    assert "  loop  Run the loop mode." in result.output
    assert "  pads  Run the pads mode." in result.output


def test_loop_help():
    runner = CliRunner()
    result = runner.invoke(cli.octo_slample, ["loop", "--help"])

    assert result.exit_code == 0
    assert "Usage: octo-slample loop [OPTIONS]" in result.output
    assert "  Run the loop mode." in result.output
    assert "  In loop mode, the loop is played continuously." in result.output
    assert "Options:" in result.output
    assert "  --pattern TEXT  Pattern file  [required]" in result.output
    assert "  --bpm INTEGER   Beats per minute" in result.output
    assert "  --help          Show this message and exit." in result.output


def test_loop_starts_clock_and_loops(mock_looping_sampler_from_pattern_file):
    runner = CliRunner()
    result = runner.invoke(
        cli.octo_slample, ["loop", "--pattern", "patterns/pattern_bank.json"]
    )

    assert result.exit_code == 0
    assert "Playing pattern: " in result.output
    mock_looping_sampler_from_pattern_file.return_value.clock.start.assert_called_once()
    mock_looping_sampler_from_pattern_file.return_value.loop.assert_called_once()


def test_loop_handles_invalid_pattern_file(mock_looping_sampler_from_pattern_file):
    mock_looping_sampler_from_pattern_file.side_effect = SchemaError(
        "Invalid pattern file"
    )
    runner = CliRunner()
    result = runner.invoke(
        cli.octo_slample, ["loop", "--pattern", "invalid_pattern.json"]
    )

    assert result.exit_code == 2
    assert "Invalid pattern file 'invalid_pattern.json'" in result.output


def test_loop_handles_unknown_error(mock_looping_sampler_from_pattern_file):
    mock_looping_sampler_from_pattern_file.side_effect = Exception("Unknown Error")
    runner = CliRunner()
    result = runner.invoke(
        cli.octo_slample, ["loop", "--pattern", "invalid_pattern.json"]
    )

    assert result.exit_code == 1
    assert "Unknown Error" in result.output


def test_pads_help():
    runner = CliRunner()
    result = runner.invoke(cli.octo_slample, ["pads", "--help"])

    assert result.exit_code == 0
    assert "Usage: octo-slample pads [OPTIONS]" in result.output
    assert "  Run the pads mode." in result.output
    assert (
        "  In pads mode, the user can play channels by pressing the corresponding number"  # noqa: E501
        in result.output
    )
    assert "  key." in result.output
    assert "  The user can quit by pressing `0`" in result.output
    assert "Options:" in result.output
    assert "  --help  Show this message and exit." in result.output


def test_pads(mocker, mock_click_getchar, mock_play_channel):
    runner = CliRunner()
    result = runner.invoke(cli.octo_slample, ["pads"])

    assert result.exit_code == 0
    assert "Octo Slample" in result.output
    assert "Playing channel 1" in result.output
    assert "Playing channel 2" in result.output
    assert "Playing channel 3" in result.output
    assert "Playing channel 4" in result.output
    assert "Playing channel 5" in result.output
    assert "Playing channel 6" in result.output
    assert "Playing channel 7" in result.output
    assert "Playing channel 8" in result.output

    assert mock_click_getchar.call_count == 11

    mock_play_channel.assert_has_calls([mocker.call(n) for n in range(1, 9)])
