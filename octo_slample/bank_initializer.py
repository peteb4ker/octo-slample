"""Initialize a sample directory.

Usage:
    octo_slample init <dir>

Side Effects:
    Creates a sample bank configuration file in the given directory.

Arguments:
    dir: The directory to initialize.
"""
import json

from octo_slample.directory import DirectoryMixin
from octo_slample.exception import BankExistsError


class BankInitializer(DirectoryMixin):
    """Initialize a sample bank directory."""

    def __init__(
        self,
        directory: str,
        force: bool = False,
        recursive: bool = False,
        ignore_existing_bank_file: bool = False,
    ) -> None:
        """Initialize a sample directory.

        Args:
            directory (str): The directory to initialize.
            force (bool, optional): Whether to force initialization. Defaults to False.
            recursive (bool, optional): Whether to initialize recursively.
                Defaults to False.
            ignore_existing_bank_file (bool, optional): Whether to ignore an existing
                bank file. Defaults to False.
                If set, this will not throw an exception if there is an existing bank
                file and execution will continue.
        """
        self.directory = directory
        self._force = force
        self._recursive = recursive
        self._ignore_existing_bank_file = ignore_existing_bank_file

    def run(self) -> None:
        """Run the initializer, creating a bank file.

        If `is_recursive` is `True` and there are subdirectories containing
        WAV files, this will recursively run the initializer
        on subdirectories.

        Raises:
            BankExistsError: If there is an existing bank file and we're
                not forcing.
            FileNotFoundError: If there are no WAV files in the directory.
        """
        if self._recursive and self.collect_subdirectories(self.directory) != []:
            self.recursively_run()
        else:
            self.write_bank_file()

    def recursively_run(self) -> None:
        """Recursively run the initializer on subdirectories, if they exist."""
        for subdirectory in self.collect_subdirectories(self.directory):
            BankInitializer.init(
                subdirectory,
                self._force,
                self._recursive,
                self._ignore_existing_bank_file,
            )

    def to_bank_dict(self) -> dict:
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
        """Write the bank file.

        Raises:
            BankExistsError: If there is an existing bank file and we're
                not forcing.
            FileNotFoundError: If there are no WAV files in the directory.
        """
        if (self.directory / "bank.json").exists() and self._ignore_existing_bank_file:
            return

        if (self.directory / "bank.json").exists() and not self._force:
            raise BankExistsError(self.directory)

        # if there are no WAV files in the folder and we're not recursive,
        # throw an exception
        if (
            not any(file.suffix == ".wav" for file in self.directory.iterdir())
            and not self._recursive
        ):
            raise FileNotFoundError(self.directory)

        with open(self.directory / "bank.json", "w") as bank_file:
            json.dump(self.to_bank_dict(), bank_file, indent=4)

    @classmethod
    def init(
        cls,
        directory: str,
        force: bool = False,
        recursive=False,
        ignore_existing_bank_file=False,
    ) -> None:
        """Initialize a sample directory.

        Args:
            directory (str): The directory to initialize.
            force (bool, optional): Whether to force initialization.
                Defaults to False.
            recursive (bool, optional): Whether to initialize recursively.
                Defaults to False.
            ignore_existing_bank_file (bool, optional): Whether to ignore
                an existing bank file. Defaults to False.
        """
        initializer = cls(directory, force, recursive, ignore_existing_bank_file)
        initializer.run()

        return initializer

    @classmethod
    def init_recursive(cls, directory: str, force: bool = False) -> None:
        """Initialize a sample directory recursively.

        Ignores existing bank files if they exist.

        Args:
            directory (str): The directory to initialize.
            force (bool, optional): Whether to force initialization. Defaults to False.
        """
        initializer = cls(directory, force, True, True)
        initializer.run()

        return initializer
