"""JSON pattern class.

This class is used to load and store a pattern from a JSON file.
"""


from schema import And, Optional, Or, Schema, Use

from octo_slample.json import JsonMixin
from octo_slample.pattern.text_pattern import TextPattern


class JsonPattern(JsonMixin, TextPattern):
    """Read and writes patterns from JSON files.

    This helper class makes it easy to use JSON as a pattern
    configuration format.
    """

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
                    "1   1.2 1.3 1.4 ",
                    "x   x   x   x   ",
                    "  x   x   x   x ",
                ]
            }

        Note that the header row, ``"1   1.2 1.3 1.4"``, is optional.
        Header rows are recognized by the presence of a `1` in the
        first column. If a header row is present, it is removed on read.

        See Also:
            https://github.com/keleshev/schema

        Returns:
            The schema.
        """
        return Schema(
            {
                "name": And(str, len),
                Optional("description"): str,
                "pattern": Or(
                    [And(str, len)],
                    [
                        {
                            Optional("name"): And(str, len),
                            "steps": And(str, len),
                            Optional("volume"): And(Use(float), lambda n: 0 <= n <= 1),
                        }
                    ],
                ),
            }
        )

    def _load(self, json_pattern: dict):
        """Load the pattern from a JSON file.

        Validates the JSON pattern against the schema defined by
        `JsonPattern.schema`, then returns a Pattern instance.

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
        if (
            "name" in json_pattern["pattern"][0]
            and json_pattern["pattern"][0]["name"] == "header"
        ) or (json_pattern["pattern"][0]["steps"][0] == "1"):
            del json_pattern["pattern"][0]

        # reset the channel and step size
        self.reset(
            len(json_pattern["pattern"]), len(json_pattern["pattern"][0]["steps"])
        )

        # Load pattern list into pattern
        self.pattern = [channel["steps"] for channel in json_pattern["pattern"]]
