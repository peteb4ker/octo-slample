import pytest

from octo_slample.bank_initializer import BankInitializer
from octo_slample.exception import BankExistsError


@pytest.fixture
def existing_bank(tmp_path):
    """Fixture for an existing bank file."""
    (tmp_path / "bank.json").touch()
    (tmp_path / "sample.wav").touch()
    return tmp_path


@pytest.fixture
def directory_to_init(tmp_path):
    """Fixture for a bank to initialize."""
    (tmp_path / "sample1.wav").touch()
    (tmp_path / "sample2.wav").touch()
    return tmp_path


@pytest.fixture
def directory_with_subdirectories(tmp_path):
    (tmp_path / "subdirectory1").mkdir()
    (tmp_path / "subdirectory2").mkdir()
    (tmp_path / "subdirectory1" / "sample.wav").touch()
    (tmp_path / "subdirectory2" / "sample.wav").touch()

    return tmp_path


@pytest.fixture
def mock_json_dump(mocker):
    """Fixture for mocking json.dump."""
    return mocker.patch("octo_slample.bank_initializer.json.dump")


def test_bank_initializer_constructor(directory_to_init):
    """Test the BankInitializer initializer."""
    initializer = BankInitializer(directory_to_init)
    assert initializer.directory == directory_to_init


def test_bank_initializer_bad_directory(directory_to_init):
    """Test the BankInitializer initializer with a bad directory."""
    with pytest.raises(NotADirectoryError):
        BankInitializer(directory_to_init / "bad_directory")


def test_run(directory_to_init):
    """Test the BankInitializer run method."""
    initializer = BankInitializer(directory_to_init)
    initializer.run()


def test_run_with_existing_bank(existing_bank):
    """Test the BankInitializer run method with an existing bank file."""
    initializer = BankInitializer(existing_bank)
    with pytest.raises(BankExistsError):
        initializer.run()


def test_run_ignoring_existing_bank_file(existing_bank, mock_json_dump):
    """Test the BankInitializer run method with an existing bank file."""
    initializer = BankInitializer(existing_bank, ignore_existing_bank_file=True)

    initializer.run()

    mock_json_dump.assert_not_called()


def test_run_with_no_wav_files(tmp_path):
    """Test the BankInitializer run method with no WAV files."""

    initializer = BankInitializer(tmp_path)
    with pytest.raises(FileNotFoundError):
        initializer.run()


def test_run_recursively(directory_with_subdirectories):
    """Test the BankInitializer run method with an existing bank file and
    force."""
    initializer = BankInitializer(directory_with_subdirectories, recursive=True)
    initializer.run()

    assert (directory_with_subdirectories / "subdirectory1" / "bank.json").exists()
    assert (directory_with_subdirectories / "subdirectory2" / "bank.json").exists()


def test_bank_initializer_to_bank_dict(directory_to_init):
    """Test the BankInitializer to_bank_dict method."""
    initializer = BankInitializer(directory_to_init)

    assert initializer.to_bank_dict() == {
        "name": directory_to_init.name,
        "description": "",
        "samples": [
            {
                "name": "sample1",
                "path": str((directory_to_init / "sample1.wav").resolve()),
            },
            {
                "name": "sample2",
                "path": str((directory_to_init / "sample2.wav").resolve()),
            },
        ],
    }


def test_bank_initializer_write_bank_file(directory_to_init):
    """Test the BankInitializer write_bank_file method."""
    initializer = BankInitializer(directory_to_init)
    initializer.write_bank_file()

    assert (directory_to_init / "bank.json").exists()


def test_bank_initializer_init(directory_to_init):
    """Test the BankInitializer initializer."""
    initializer = BankInitializer.init(directory_to_init)

    assert isinstance(initializer, BankInitializer)
    assert initializer.directory == directory_to_init


def test_init_recursive(directory_with_subdirectories):
    """Test the BankInitializer run method with an existing bank file and
    force."""
    BankInitializer.init_recursive(directory_with_subdirectories)

    assert (directory_with_subdirectories / "subdirectory1" / "bank.json").exists()
    assert (directory_with_subdirectories / "subdirectory2" / "bank.json").exists()
