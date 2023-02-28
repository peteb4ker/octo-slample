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

    def _collect_subdirectories(self, directory: Path) -> None:
        """Collect all subdirectories with WAV files.

        For the given `directory`, collect all subdirectories that contain
        WAV files, or subdirectories that contain subdirectories that can
        be iterated further.

        Args:
            directory (Path): The directory to collect subdirectories from.

        Returns:
            list: The list of subdirectories.
        """
        assert isinstance(directory, Path), "Directory must be a Path."
        assert directory.is_dir(), "Directory must be a directory."

        return [
            subdirectory
            for subdirectory in directory.iterdir()
            if subdirectory.is_dir()
            and any(
                (file.suffix == ".wav" or file.is_dir())
                for file in subdirectory.iterdir()
            )
        ]
