"""JSON pattern class.

This class is used to load and store a pattern from a JSON file.
"""


from schema import And, Optional, Schema, Use

from octo_slample.pattern.text_pattern import TextPattern
from octo_slample.sampler.sample_bank import SampleBank


class JsonPatternBank:
    """Loads pattern + banks from JSON.

    This helper class makes it easy to use JSON as a pattern and bank
    configuration format.
    """

    def __init__(self):
        """Initialize the pattern bank loader."""
        pass

    @classmethod
    @property
    def schema(self):
        """Get the schema for the JSON pattern.

        The JSON schema has the following format:

        .. code-block:: json
            {
                "name": "pattern name",
                "description": "pattern description",
                "pattern": [
                    "1234123412341234",
                    "x   x   x   x   ",
                    "  x   x   x   x ",
                    ...
                ],
                "samples": [
                    {
                        "sample": "path/to/sample1.wav",
                        "sample": "path/to/sample2.wav",
                    },
                    ...
                ]
            }

        Note that the header row, `"1234123412341234"`, is optional.

        See Also:
            https://github.com/keleshev/schema

        Returns:
            The schema.
        """
        return Schema(
            {
                "name": And(str, len),
                Optional("description"): And(str, len),
                "pattern": [And(str, len)],
                "samples": [
                    {
                        "sample": And(str, len),
                        Optional("volume"): And(Use(float), lambda n: 0 <= n <= 1),
                    }
                ],
            }
        )

    def load(self, json_pattern: dict):
        """Load the pattern and banks from a JSON pattern.

        Validates the JSON pattern against the schema defined by
        `JsonPatternBank.schema`, then loads the pattern and bank.

        If the json document does not match the schema, a `SchemaError` is raised.

        If the pattern has a header, it is removed.

        Args:
            json_pattern (dict): The JSON pattern.

        Raises:
            SchemaError: If the JSON pattern does not match the schema.
        """
        # validate JSON pattern
        self.schema.validate(json_pattern)

        # remove header row
        if json_pattern["pattern"][0].startswith("1"):
            json_pattern["pattern"].pop(0)

        # Load pattern list into pattern
        step_count = len(json_pattern["pattern"][0])
        self._pattern = TextPattern(step_count=step_count)
        self._pattern.pattern = json_pattern["pattern"]

        # load samples into channels
        self._bank = SampleBank(len(json_pattern["samples"]))
        self._bank.samples = [x["sample"] for x in json_pattern["samples"]]

    @classmethod
    def from_file(cls, filename: str):
        """Load a pattern from a JSON file.

        Args:
            filename (str): The path to the JSON file.

        Returns:
            The pattern.
        """
        import json

        with open(filename, "r") as f:
            json_pattern = json.load(f)

        return cls.from_json(json_pattern)

    @classmethod
    def from_json(cls, json_pattern: dict):
        """Create a pattern from a JSON pattern.

        Args:
            json_pattern (dict): The JSON pattern.

        Returns:
            The pattern.
        """
        pattern = cls()
        pattern.load(json_pattern)

        return pattern

    @property
    def pattern(self):
        """Get the pattern.

        Returns:
            The pattern.
        """
        return self._pattern

    @property
    def bank(self):
        """Get the sample bank.

        Returns:
            The sample bank.
        """
        return self._bank

    def __str__(self):
        """Get a string representation of the pattern.

        Returns:
            A string representation of the pattern.
        """
        return f"{self.pattern}\n{self.bank}"
