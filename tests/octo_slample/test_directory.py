import pytest

from octo_slample.directory import DirectoryMixin


@pytest.fixture
def directory_with_subdirectories(tmp_path):
    (tmp_path / "subdirectory1").mkdir()
    (tmp_path / "subdirectory2").mkdir()
    (tmp_path / "subdirectory1" / "sample.wav").touch()
    (tmp_path / "subdirectory2" / "sample.wav").touch()

    return tmp_path


@pytest.fixture
def directory_to_init(tmp_path):
    """Fixture for a bank to initialize."""
    (tmp_path / "sample1.wav").touch()
    (tmp_path / "sample2.wav").touch()
    return tmp_path


def test_create_directory_new_path_is_created(tmp_path):
    path = tmp_path / "foo" / "bar"

    DirectoryMixin.create_directory(path)

    assert path.exists()


def test_create_directory_existing_path_is_ignored(tmp_path):
    path = tmp_path / "foo" / "bar"
    path.mkdir(parents=True, exist_ok=True)

    DirectoryMixin.create_directory(path)

    assert path.exists()


def testcollect_subdirectories_no_subdirectories(directory_to_init):
    """Test the BankInitializer collect_subdirectories method with no
    subdirectories."""
    assert DirectoryMixin.collect_subdirectories(directory_to_init) == []


def testcollect_subdirectories_with_subdirectories_and_no_wavs(directory_to_init):
    """Test the BankInitializer collect_subdirectories method with
    subdirectories."""
    (directory_to_init / "subdirectory1").mkdir()
    (directory_to_init / "subdirectory2").mkdir()

    assert DirectoryMixin.collect_subdirectories(directory_to_init) == []


def testcollect_subdirectories_with_subdirectories(directory_with_subdirectories):
    assert DirectoryMixin.collect_subdirectories(directory_with_subdirectories) == [
        directory_with_subdirectories / "subdirectory1",
        directory_with_subdirectories / "subdirectory2",
    ]
