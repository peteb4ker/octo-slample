"""A mixin class for working with directories."""
from abc import ABCMeta
from pathlib import Path
from typing import Union


class DirectoryMixin(metaclass=ABCMeta):
    """A mixin class for working with directories."""

    @property
    def directory(self) -> str:
        """Get the directory to initialize.

        Returns:
            str: The directory to initialize.
        """
        return self._directory

    @directory.setter
    def directory(self, directory: Union[str, Path]) -> None:
        """Set the directory to initialize.

        Args:
            directory (str, Path): The directory to initialize.

        Raises:
            FileNotFoundError: If the directory does not exist.
            NotADirectoryError: If the directory is not a directory.
        """
        assert isinstance(
            directory, (str, Path)
        ), f"Directory must be a string or Path but got a {type(directory)}"

        directory = Path(directory).resolve()

        if not directory.is_dir():
            raise NotADirectoryError(f"'{directory}' must be a directory")

        self._directory = directory

    @classmethod
    def collect_subdirectories(
        self, directory: Path, with_file_suffix: str = ".wav"
    ) -> None:
        """Collect all subdirectories with WAV files.

        For the given `directory`, collect all subdirectories that contain
        WAV files, or subdirectories that contain subdirectories that can
        be iterated further.

        Args:
            directory (Path): The directory to collect subdirectories from.
            with_file_suffix (str): The file suffix to look for.

        Returns:
            list: The list of subdirectories.
        """
        directory = Path(directory)
        assert directory.is_dir(), "Directory must be a directory."

        return [
            subdirectory
            for subdirectory in directory.iterdir()
            if subdirectory.is_dir()
            and any(
                (file.suffix == with_file_suffix or file.is_dir())
                for file in subdirectory.iterdir()
            )
        ]

    @classmethod
    def create_directory(cls, path: Union[str, Path]) -> None:
        """Create the directory `path` if it does not exist.

        Args:
            path (str, Path): The path to create.
        """
        if not Path(path).exists():
            Path(path).mkdir(parents=True, exist_ok=True)
