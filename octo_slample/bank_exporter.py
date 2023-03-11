"""Export a bank to a set of wav files."""
from pathlib import Path

from octo_slample.directory import DirectoryMixin
from octo_slample.sampler.json_sample_bank import JsonSampleBank
from octo_slample.wav_writer import WavWriter


class BankExporter(DirectoryMixin):
    """Export a bank to a set of wav files.

    This class contains methods that can be used to export banks to a
    set of wav files that are compatible with the ALM Squid Salmple
    format.
    """

    @classmethod
    def export_bank(
        self, bank_file: Path, bank_number: int, set_output_path: Path
    ) -> tuple[Path, list[str | ValueError]]:
        """Export a bank to a set of wav files.

        Args:
            bank_file (Path): The path to the bank file.
            bank_number (int): The bank number.
            set_output_path (Path): The Squid Set output path.

        Returns:
            tuple[Path, list[str]]: A tuple containing:
                The path at which the bank is saved
                A list of paths of the exported files, or ValueError if
                a sample could not be written.

        Raises:
            ValueError: If the bank file does not exist.
            SchemaError: If the bank file is not valid.
        """
        bank = JsonSampleBank.from_file(bank_file)

        bank_path, sample_paths = WavWriter.write_bank(
            bank, bank_number, set_output_path
        )

        WavWriter.write_info_txt(bank, bank_path)

        return bank_path, sample_paths

    @classmethod
    def export_set(self, input_directory: Path, output_directory: Path) -> None:
        """Export a set of sample banks to a Squid Sample set.

        This method always overwrites the output directory, so be careful
        when using it and ensure that your samples are stored elsewhere.

        Args:
            iinput_directorynput (Path): The input path.
            output_directory (Path): The output path.

        Returns:
            list[Tuple[Path, str|ValueError]]: A list of tuples containing:
                The path at which the bank is saved
                A list of paths of the exported files, or ValueError if
                a sample could not be written.

        Raises:
            ValueError: If the input directory does not exist.
            SchemaError: If the bank file is not valid.
        """
        self.directory = input_directory

        self.create_directory(output_directory)

        bank_directories = self.collect_subdirectories(
            self.directory, with_file_suffix=".json"
        )
        squid_banks = []

        # for each bank directory, export the bank.  The bank number is
        # the index of the bank directory in the list of bank directories.
        for bank_number, bank_directory in enumerate(bank_directories):
            bank_file = next(bank_directory.glob("*.json"))

            result = self.export_bank(bank_file, bank_number + 1, output_directory)

            squid_banks.append(result)

        return squid_banks
