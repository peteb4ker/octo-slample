from contextlib import nullcontext as does_not_raise

import pytest

from octo_slample.sampler.channel import Channel
from octo_slample.sampler.sample_bank import SampleBank
from octo_slample.wav_writer import WavWriter


@pytest.fixture
def mock_channel(mocker):
    m = mocker.MagicMock(spec=Channel)

    type(m).number = mocker.PropertyMock(side_effect=[1, 2, 3])

    return m


@pytest.fixture
def mock_channel_sample_is_none(mock_channel):
    mock_channel.sample = None
    return mock_channel


@pytest.fixture
def mock_sample_bank(mocker, mock_channel):
    m = mocker.MagicMock(spec=SampleBank)
    m.__getitem__.side_effect = [mock_channel, mock_channel, mock_channel]
    return m


@pytest.fixture
def sample_banks(mocker, mock_sample_bank):
    return [
        mock_sample_bank,
        mock_sample_bank,
        mock_sample_bank,
    ]


@pytest.fixture
def patched_write_channel(mocker, tmp_path):
    m = mocker.patch.object(WavWriter, "write_channel")
    m.side_effect = [
        f"{tmp_path}/Bank 1/chan-001.wav",
        f"{tmp_path}/Bank 1/chan-002.wav",
        f"{tmp_path}/Bank 1/chan-003.wav",
    ]

    return m


@pytest.fixture
def patched_write_bank(mocker, tmp_path):
    m = mocker.patch.object(WavWriter, "write_bank")
    m.side_effect = [
        f"{tmp_path}/Bank 1",
        f"{tmp_path}/Bank 2",
        f"{tmp_path}/Bank 3",
    ]

    return m


def test_build_sample_output_path(tmp_path):
    result = WavWriter.build_sample_output_path(
        bank_output_path=str(tmp_path), channel_number=5
    )

    assert result == str(tmp_path / "chan-005.wav")


def test_build_bank_output_path(tmp_path):
    result = WavWriter.build_bank_output_path(
        set_output_path=str(tmp_path), bank_number=5
    )

    assert result == str(tmp_path / "Bank 5")


@pytest.mark.parametrize(
    ("channel", "bank_output_path", "expected", "exception"),
    [
        (
            pytest.lazy_fixture("mock_channel"),
            pytest.lazy_fixture("tmp_path"),
            "chan-001.wav",
            does_not_raise(),
        ),
        (
            None,
            pytest.lazy_fixture("tmp_path"),
            "chan-001.wav",
            pytest.raises(AssertionError),
        ),
        (
            pytest.lazy_fixture("mock_channel"),
            None,
            "chan-001.wav",
            pytest.raises(AssertionError),
        ),
        (
            pytest.lazy_fixture("mock_channel_sample_is_none"),
            pytest.lazy_fixture("tmp_path"),
            "chan-001.wav",
            pytest.raises(ValueError),
        ),
    ],
    ids=[
        "valid",
        "invalid_channel",
        "invalid_bank_output_path",
        "channel.sample is None",
    ],
)
def test_write_channel(tmp_path, channel, bank_output_path, expected, exception):
    expected = str(tmp_path / expected)

    with exception:
        result = WavWriter.write_channel(
            channel=channel, bank_output_path=str(bank_output_path)
        )

        assert result == expected
        channel.sample.export.assert_called_once_with(
            expected,
            format="wav",
            parameters=["-ac", "1", "-ar", "44100", "-b:a", "16"],
        )


@pytest.mark.parametrize(
    ("sample_bank", "set_output_path", "bank_number", "expected", "exception"),
    [
        (
            pytest.lazy_fixture("mock_sample_bank"),
            pytest.lazy_fixture("tmp_path"),
            1,
            "Bank 1",
            does_not_raise(),
        ),
        (None, pytest.lazy_fixture("tmp_path"), 1, "", pytest.raises(AssertionError)),
        (
            pytest.lazy_fixture("mock_sample_bank"),
            None,
            1,
            "",
            pytest.raises(AssertionError),
        ),
        (
            pytest.lazy_fixture("mock_sample_bank"),
            pytest.lazy_fixture("tmp_path"),
            0,
            "",
            pytest.raises(AssertionError),
        ),
    ],
    ids=["valid", "sample_bank_none", "set_output_path_none", "bank_number_zero"],
)
def test_write_bank(
    mocker,
    tmp_path,
    patched_write_channel,
    mock_channel,
    sample_bank,
    set_output_path,
    bank_number,
    expected,
    exception,
):
    expected = [
        str(tmp_path / expected / wav)
        for wav in ["chan-001.wav", "chan-002.wav", "chan-003.wav"]
    ]

    with exception:
        result = WavWriter.write_bank(
            bank=sample_bank, bank_number=bank_number, set_output_path=set_output_path
        )

        assert result == expected

        patched_write_channel.assert_has_calls(
            [
                mocker.call(mock_channel, str(tmp_path / "Bank 1")),
                mocker.call(mock_channel, str(tmp_path / "Bank 1")),
                mocker.call(mock_channel, str(tmp_path / "Bank 1")),
            ]
        )


@pytest.mark.parametrize(
    ("banks", "set_output_path", "expected", "exception"),
    [
        (
            pytest.lazy_fixture("sample_banks"),
            pytest.lazy_fixture("tmp_path"),
            ["Bank 1"],
            does_not_raise(),
        ),
    ],
    ids=["valid"],
)
def test_write_set(
    mocker, tmp_path, patched_write_bank, banks, set_output_path, expected, exception
):
    set_output_path = str(set_output_path)

    with exception:
        result = WavWriter.write_set(banks=banks, set_output_path=set_output_path)

        assert result == [
            str(tmp_path / "Bank 1"),
            str(tmp_path / "Bank 2"),
            str(tmp_path / "Bank 3"),
        ]

        patched_write_bank.assert_has_calls(
            [
                mocker.call(banks[0], set_output_path),
                mocker.call(banks[1], set_output_path),
                mocker.call(banks[2], set_output_path),
            ]
        )