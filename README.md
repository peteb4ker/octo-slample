# Octo Slample

8-channel virtual sampler for creating and organizing sample packs for the
ALM Squid Salmple Eurorack sampler.

## What is this for?

The Octo slample application can take a single `json` bank file or multiple `json` bank
files and render them into the correct folder format, to be loaded onto the Squid Sample
USB drive, without modification.  This provides a straightforward way to create sample
banks through configuration, linking arbitrary audio files on your system to specific
slots in specific banks.   With one command, a complete set of banks can be created
with the correct folder structure, file name and audio format.

Iteratively adding to these configuration files allows you to build up banks and sets
over time.  JSON configuration files are greatly simplified approach to bank management
as, otherwise, its necessary to manually note which samples are in which banks. This
presents a problem of scale when you have dozens of banks.

With the octo slample application, bank management is distilled to a set of configuration
files that can be copied and amended easily.  This allows you to get the most out
of the Squid Salmple module, easily managing dozens or potentially hundreds of banks.

## Getting started

```shell
brew install pre-commit hadolint
```

```shell
pre-commit install --hook-type commit-msg
```

```shell
pre-commit run --all-files
```

## Repository conventions

### Commit messages

This repository uses the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) commit message format.  Formatting is checked upon commit.

## CI/CD

### Code formatting using black

```shell
poetry run black .
```

### Linting

```shell
poetry run flake8
```

### Testing

Run unit tests

```shell
poetry run pytest
```

View coverage report

```shell
open htmlcov/index.html
```

### Build documentation

Build docs

```shell
poetry run sphinx-build -b html . _build
```

### View documentation

```shell
open _build/index.html
```

## Capabilities

### Scaffold configuration files from existing sample directories

This is useful when using a sample manager such as XO.   XO generates
folders of processed samples, albeit without the correct sample rate,
bit rate, folder name or file names.

The Slample CLI inspects folders of these samples to create a stub
JSON configuration that can be augmented to map between these folders
into the file structure required by Squid Salmple.

```shell
poetry run octo-slample init <folder containing samples>
```

If the folder does not contain WAV files it is ignored.

Upon successful traversal of a sample folder, a JSON file called
`bank.json` is written into the folder with the following contents:

```json
{
    "name": "<folder name>",
    "description": "",
    "samples": [
        { "name": "1", "path": "/fully/qualified/path/to/sample" },
        { "name": "2", "path": "/fully/qualified/path/to/sample" },
        { "name": "3", "path": "/fully/qualified/path/to/sample" },
}
```

The order of the samples is based on the natural ordering of the
WAV files within the folder.   If there are 6 WAV files in the folder,
6 sample entries are created.

Subsequent calls of `poetry run octo-slample init` on the folder
will be ignored.   To overwrite an existing `bank.json`, run:

```shell
poetry run octo-slample init <folder containing samples> -f
```

or


```shell
poetry run octo-slample init <folder containing samples> --force
```

The `bank.json` file can be edited in-place to
update `name`, `description` and the `name` of each channel.

If there are channels with no sample, add `{ "path": null },`
as a sample entry to make up the number of sample entries to
the expected channel count (i.e. `8`).

### Play 8 samples based on keypress of 8 keys

```shell
poetry run octo-slample pads -b banks/tinlicker.voodoo.bank.json
```

### Play samples in a loop, with pattern and sample bank defined in a txt file

```shell
poetry run octo-slample loop -p patterns/pattern.json -b banks/sample_bank.json
```

### Play a 2-bar pattern

```shell
poetry run octo-slample loop --pattern patterns/organic_house.pattern.json --bank banks/sample_bank.json
```

### Save samples in the correct format and location

Squid Sample requires WAV files to have the following spec:

- 16 bit
- 44.1 kHz
- `Set {name}` folder name (optional)
   -  `Bank {n}` folder name
       -  `chan-00{x}.wav` file format

In addition to creating `wav` sample banks, the name of the bank can be added to a file
named `info.txt`, stored in the `Bank {n}` folder alongside the `wav` samples.  This
name is taken from the `name` attribute in the bank `json` definition.

#### Creating sample banks

When creating sample banks, the output directory is provided by the `--output`
or `-o` command-line flag.

#### Save a bank in Squid Salmple format

```shell
poetry run octo-slample export -b banks/sample_bank.json -n 1 -o "tmp/Set 1"
```

### Recursively save a directory of sample banks to a Set

To create a Set from multiple sample bank directories, use the `export-set` command:

```shell
poetry run octo-slample export-set ~/samples ~/tmp/Set\ 1
```

This command will create a folder that can be copied onto the Squid USB drive.

### Set the volume on a channel for loop playback

Loop playback volume can be set, per channel, within `pattern.json` files.
This setting only affects loop playback and does not impact the exported
sample banks / Squid Salmple module.

To set the pattern channel volume, add the `volume` attribute to pattern
entries.  Volume is defined in decibels so, for example, a ~50% gain reduction
on a channel can be achieved with `"volume": -3`.   Both integer and float values
are accepted.

```json
{
    "name": "My Pattern",
    "pattern": [
        { "name": "header", "steps": "1234123412341234" },
        { "name": "kick",   "steps": "x   x   x   x   " },
        { "name": "tom",    "steps": "   x  x    x  x " , "volume": -3 },
}
```

# TODO


### Set the channel swing for loop playback

### Simple UI to play 8 samples

### Drop samples onto the UI

### One shots and loops

### 16th matrix for sample trigger

### Project built with github actions

- Documentation available:
- Package available:

## Licence (MIT License)

Copyright © 2023 Pete Baker <peteb4ker@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
