"""Exceptions for the Octo Slample library."""


class BankExistsError(Exception):
    """Raised when trying to init a directory with an existing bank file."""

    def __init__(self, directory: str) -> None:
        """Initialize the exception.

        Args:
            directory (str): The directory that already has a bank file.
        """
        self.directory = directory
