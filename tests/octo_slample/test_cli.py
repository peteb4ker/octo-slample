import pytest
from click.testing import CliRunner
from schema import SchemaError

import octo_slample.cli as cli


@pytest.fixture
def mock_looping_sampler(mocker):
    m = mocker.patch("octo_slample.cli.LoopingSampler")
    m.clock = mocker.Mock()
    m.loop = mocker.Mock()

    return m


@pytest.fixture
def mock_json_pattern(mocker):
    m = mocker.patch("octo_slample.cli.JsonPattern.from_file")

    return m


@pytest.fixture
def mock_json_sample_bank(mocker):
    m = mocker.patch("octo_slample.cli.JsonSampleBank.from_file")

    return m


@pytest.fixture
def mock_click_getchar(mocker):
    """Simulate the user clicking from 1-9, then x, then 0.

    1-8 are valid channels 9 is an invalid channel, which is ignored x
    is an invalid keypress, which is ignored
    """
    m = mocker.patch("octo_slample.cli.click.getchar")
    m.side_effect = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "x", "0"]

    return m


@pytest.fixture
def mock_play_channel(mocker):
    return mocker.patch("octo_slample.cli.Sampler.play_channel")


@pytest.fixture
def mock_wav_writer(mocker):
    m = mocker.patch("octo_slample.cli.WavWriter.write_bank")
    m.return_value = ["foo.wav", "bar.wav"]

    return m


def test_octo_slample_help():
    runner = CliRunner()
    result = runner.invoke(cli.octo_slample)

    assert result.exit_code == 0, "octo-slample --help should exit with code 0"
    assert "Usage: octo-slample [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "  Octo Slample command line interface." in result.output
    assert "  --help  Show this message and exit." in result.output
    assert "Commands:" in result.output
    assert "  export  Export a bank to a set of wav files." in result.output
    assert "  loop    Run the loop mode." in result.output
    assert "  pads    Run the pads mode." in result.output


def test_loop_help():
    runner = CliRunner()
    result = runner.invoke(cli.octo_slample, ["loop", "--help"])

    assert result.exit_code == 0, "octo-slample loop --help should exit with code 0"
    assert "Usage: octo-slample loop [OPTIONS]" in result.output
    assert "  Run the loop mode." in result.output
    assert "  In loop mode, the loop is played continuously." in result.output
    assert "Options:" in result.output
    assert "  -p, --pattern TEXT  Pattern file  [required]" in result.output
    assert "  -b, --bank TEXT     Bank file  [required]" in result.output
    assert "  --bpm INTEGER       Beats per minute" in result.output


def test_loop_starts_clock_and_loops(mock_looping_sampler):
    runner = CliRunner()
    result = runner.invoke(
        cli.octo_slample,
        [
            "loop",
            "--pattern",
            "patterns/pattern.json",
            "--bank",
            "banks/sample_bank.json",
            "--bpm",
            "120",
        ],
    )

    assert result.exit_code == 0, "octo-slample loop should exit with code 0"
    assert "Playing pattern: " in result.output
    mock_looping_sampler.return_value.clock.start.assert_called_once()
    mock_looping_sampler.return_value.loop.assert_called_once()


def test_loop_handles_invalid_pattern_file(mock_json_pattern, mock_json_sample_bank):
    mock_json_pattern.side_effect = SchemaError("Invalid pattern file")
    runner = CliRunner()
    result = runner.invoke(
        cli.octo_slample,
        ["loop", "--pattern", "invalid_pattern.json", "--bank", "valid_bank.json"],
    )

    assert result.exit_code == 1
    assert "Error: Invalid pattern file" in result.output


def test_loop_handles_invalid_sample_bank_file(
    mock_json_pattern, mock_json_sample_bank
):
    mock_json_sample_bank.side_effect = SchemaError("Invalid bank file")
    runner = CliRunner()
    result = runner.invoke(
        cli.octo_slample,
        ["loop", "--pattern", "valid_pattern.json", "--bank", "invalid_bank.json"],
    )

    assert result.exit_code == 1
    assert "Error: Invalid bank file" in result.output


def test_loop_handles_unknown_error(
    mock_looping_sampler, mock_json_pattern, mock_json_sample_bank
):
    mock_looping_sampler.side_effect = Exception("Unknown Error")
    runner = CliRunner()
    result = runner.invoke(
        cli.octo_slample,
        ["loop", "--pattern", "pattern.json", "--bank", "bank.json"],
    )

    assert result.exit_code == 1


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


def test_pads(mocker, mock_click_getchar, mock_play_channel):
    runner = CliRunner()
    result = runner.invoke(cli.octo_slample, ["pads", "-b", "banks/sample_bank.json"])

    assert result.exit_code == 0, "octo-slample pads should exit with code 0"
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

    # 0-indexed channel calls
    mock_play_channel.assert_has_calls([mocker.call(n) for n in range(0, 8)])


def test_export_help():
    runner = CliRunner()
    result = runner.invoke(cli.octo_slample, ["export", "--help"])

    assert result.exit_code == 0
    assert "Usage: octo-slample export [OPTIONS]" in result.output
    assert "  Export a bank to a set of wav files." in result.output
    assert "Options:" in result.output
    assert "  -b, --bank TEXT            Bank file  [required]" in result.output
    assert "  -n, --bank-number INTEGER  Bank number  [required]" in result.output
    assert "  -o, --output TEXT          Output path  [required]" in result.output


def test_export(mock_json_sample_bank, mock_wav_writer):
    runner = CliRunner()
    result = runner.invoke(
        cli.octo_slample,
        [
            "export",
            "--bank",
            "banks/sample_bank.json",
            "--bank-number",
            "1",
            "--output",
            "exported_samples",
        ],
    )

    mock_wav_writer.assert_called_once()
    mock_json_sample_bank.assert_called_once()

    assert result.exit_code == 0, "octo-slample export should exit with code 0"
    assert "Exporting bank to Squid format..." in result.output
    assert "- foo.wav" in result.output
    assert "- bar.wav" in result.output
    assert "Done!" in result.output


def test_export_handles_unknown_error(mock_json_sample_bank, mock_wav_writer):
    runner = CliRunner()

    mock_wav_writer.side_effect = Exception("Unknown Error")

    result = runner.invoke(
        cli.octo_slample,
        [
            "export",
            "--bank",
            "banks/sample_bank.json",
            "--bank-number",
            "1",
            "--output",
            "exported_samples",
        ],
    )

    assert result.exit_code == 1
    assert "Unknown Error" in result.output
