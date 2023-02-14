"""A mixin class for loading and saving JSON documents."""

import json
from abc import ABCMeta, abstractmethod


class JsonMixin(metaclass=ABCMeta):
    """A mixin class for loading and saving JSON documents.

    This class provides methods for loading and saving JSON documents.

    This class is also an abstract base class. Subclasses must implement
    the schema and _load methods.
    """

    @abstractmethod
    def schema(self) -> dict:
        """Return the JSON schema for this class.

        Returns:
            A JSON schema.
        """
        pass

    @abstractmethod
    def _load(self, json_dict: dict):
        """Load the instance from a JSON dictionary.

        Args:
            json_dict (dict): The JSON document containing the
                instance configuration.
        """
        pass

    @classmethod
    def from_file(cls, file_path: str):
        """Create a new instance from a JSON file.

        Args:
            filename (str): The path to the JSON file.

        Returns:
            A new instance.
        """
        with open(file_path, "r") as f:
            json_dict = json.load(f)

        return cls.from_json(json_dict)

    @classmethod
    def from_json(cls, json_dict: dict):
        """Create a new instance from a JSON dictonary.

        Args:
            json_dict (dict): The JSON document containing the
                instance configuration.

        Returns:
            A new class instance.
        """
        instance = cls()

        instance._load(json_dict)

        return instance
