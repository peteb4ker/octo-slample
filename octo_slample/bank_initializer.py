"""Initialize a sample directory.

Usage:
    octo_slample init <dir>

Side Effects:
    Creates a sample bank configuration file in the given directory.

Arguments:
    dir: The directory to initialize.
"""
import json
from pathlib import Path

from octo_slample.exception import BankExistsError


class BankInitializer:
    """Initialize a sample bank directory."""

    def __init__(self, directory: str, force: bool = False) -> None:
        """Initialize a sample directory.

        Args:
            directory (str): The directory to initialize.
        """
        self.directory = directory
        self._force = force

    def run(self) -> None:
        """Run the initializer.

        Raises:
            BankExistsError: If there is an existing bank file and we're not forcing.
            FileNotFoundError: If there are no WAV files in the directory.
        """
        # If there is an existing bank file and we're not forcing, throw an exception
        if (self.directory / "bank.json").exists() and not self._force:
            raise BankExistsError(self.directory)

        # if there are no WAV files in the folder, throw an exception
        if not any(file.suffix == ".wav" for file in self.directory.iterdir()):
            raise FileNotFoundError(self.directory)

        # create a bank file with the WAV files in the folder
        self.write_bank_file()

    def to_bank_dict(self):
        """Convert the initializer instance to a bank dictionary.

        Returns:
            dict: The bank dictionary.
        """
        return {
            "name": self.directory.name,
            "description": "",
            "samples": [
                {
                    "name": file.stem,
                    "path": str(file.resolve()),
                }
                for file in sorted(self.directory.iterdir())
                if file.suffix == ".wav"
            ],
        }

    def write_bank_file(self) -> None:
        """Write the bank file."""
        with open(self.directory / "bank.json", "w") as bank_file:
            json.dump(self.to_bank_dict(), bank_file, indent=4)

    @property
    def directory(self) -> str:
        """Get the directory to initialize.

        Returns:
            str: The directory to initialize.
        """
        return self._directory

    @directory.setter
    def directory(self, directory: str) -> None:
        """Set the directory to initialize.

        Args:
            directory (str): The directory to initialize.

        Raises:
            FileNotFoundError: If the directory does not exist.
            NotADirectoryError: If the directory is not a directory.
        """
        directory = Path(directory).resolve()

        if not directory.is_dir():
            raise NotADirectoryError(f"'{directory}' must be a directory")

        self._directory = directory

    @classmethod
    def init(cls, directory: str, force: bool = False) -> None:
        """Initialize a sample directory.

        Args:
            directory (str): The directory to initialize.
        """
        initializer = cls(directory, force)
        initializer.run()

        return initializer
