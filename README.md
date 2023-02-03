# Octo Slample

8-channel virtual sampler for creating and organizing sample packs for the
ALM Squid Salmple Eurorack sampler.

## Getting started

```shell
brew install pre-commit ffmpeg
```

```shell
pre-commit install
```

```shell
pre-commit run --all-files
```

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

## Todo

### Play 8 samples based on keypress of 8 keys

```shell
poetry run sampler pads
```

### Play samples on a loop

```shell
poetry run sampler loop
```

### Simple UI to play 8 samples

### Drop samples onto the UI

### Save samples in the correct format and location

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
