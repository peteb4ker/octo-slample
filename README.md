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
brew install pre-commit ffmpeg hadolint
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

## Audio support

This repository uses [pydub](https://github.com/jiaaro/pydub) for audio playback and
conversion support.

Pydub depends on [ffmpeg or libav](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up).
Setup of this is platform-dependent.

## Todo

### Play 8 samples based on keypress of 8 keys

```shell
poetry run octo-slample pads
```

### Play samples in a loop, with pattern and sample bank defined in a txt file

```shell
poetry run octo-slample loop --pattern tests/fixtures/patterns/pattern.json --bank tests/fixtures/sample_banks/sample_bank.json
```

### Play a 2-bar pattern

``shell
poetry run octo-slample loop --pattern tests/fixtures/patterns/organic_house.pattern.json --bank tests/fixtures/sample_banks/sample_bank.json
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

#### To save a bank in Squid Salmple format

```shell
poetry run octo-slample export -b tests/fixtures/sample_banks/sample_bank.json -n 1 -o "tmp/Set 1"
```

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
