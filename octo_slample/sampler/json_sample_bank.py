"""JSON bank class.

This class is used to load and store a bank from a JSON file.
"""


from schema import And, Optional, Or, Schema

from octo_slample.json import JsonMixin
from octo_slample.sampler.sample_bank import SampleBank


class JsonSampleBank(JsonMixin, SampleBank):
    """Read/write a JSON :class:`~octo_slample.sampler.sample_bank.SampleBank`.

    This helper class makes it easy to use JSON as a bank configuration
    format.
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
                "samples": [
                    {
                        "sample": "path/to/sample1.wav",
                        "sample": "path/to/sample2.wav",
                    },
                ]
            }

        Note that the header row, ``"1234123412341234"``, is optional.

        See Also:
            https://github.com/keleshev/schema

        Returns:
            The schema.
        """
        return Schema(
            {
                "name": And(str, len),
                Optional("description"): str,
                "samples": Or(
                    [
                        {
                            Optional("name"): And(str, len),
                            Optional("path"): Or(None, And(str, len)),
                        }
                    ],
                ),
            }
        )

    def _load(self, json_bank: dict):
        """Load a banks from a JSON file.

        Validates the JSON bank against the schema defined by
        `JsonSampleBank.schema`.

        If the json document does not match the schema, a `SchemaError` is raised.

        Args:
            json_bank (dict): The JSON pattern.

        Raises:
            SchemaError: If the JSON pattern does not match the schema.
        """
        # validate JSON pattern
        self.schema.validate(json_bank)

        # load samples into channels
        self.samples = [x["path"] for x in json_bank["samples"]]
