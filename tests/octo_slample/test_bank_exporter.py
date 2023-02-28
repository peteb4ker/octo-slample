import pytest

from octo_slample.bank_exporter import BankExporter


@pytest.fixture
def banks(tmp_path):
    input_banks = tmp_path / "banks"
    input_banks.mkdir()
    (input_banks / "bank_1").mkdir()
    (input_banks / "bank_2").mkdir()
    (input_banks / "bank_1" / "sample.wav").touch()
    (input_banks / "bank_1" / "bank.json").touch()
    (input_banks / "bank_2" / "sample.wav").touch()
    (input_banks / "bank_2" / "bank.json").touch()

    return input_banks


@pytest.fixture
def mock_export_bank(mocker):
    m = mocker.patch("octo_slample.bank_exporter.BankExporter.export_bank")
    m.side_effect = [["bank_1"], ["bank_2"]]

    return m


@pytest.fixture
def mock_wavwriter_write_bank(mocker):
    m = mocker.patch("octo_slample.wav_writer.WavWriter.write_bank")
    m.return_value = ["bank_1"]

    return m


@pytest.fixture
def mock_json_sample_bank_from_file(mocker):
    m = mocker.patch("octo_slample.sampler.json_sample_bank.JsonSampleBank.from_file")
    m.return_value = "bank_1"

    return m


def test_bank_exporter_export_set(banks, tmp_path, mock_export_bank):
    result = BankExporter.export_set(banks, tmp_path / "squid")

    assert (tmp_path / "squid").is_dir()

    assert mock_export_bank.call_count == 2

    assert result == ["bank_1", "bank_2"]


def test_bank_exporter_export_bank(
    mocker, banks, tmp_path, mock_wavwriter_write_bank, mock_json_sample_bank_from_file
):
    result = BankExporter.export_bank(
        banks / "bank_1" / "bank.json", 1, tmp_path / "squid"
    )

    assert result == ["bank_1"]

    assert mock_wavwriter_write_bank.call_count == 1
    assert mock_wavwriter_write_bank.call_args == mocker.call(
        "bank_1", 1, tmp_path / "squid"
    )
    assert mock_json_sample_bank_from_file.call_count == 1
    assert mock_json_sample_bank_from_file.call_args == mocker.call(
        banks / "bank_1" / "bank.json"
    )
