# FormBadger

*FormBadger is intended to automate repetitive PDF form filling while keeping field mappings reusable and easy to edit.*

![Logo](docs/logo.jpg)

## Features

- Batch-fill interactive PDF forms
- Analyze PDF fields automatically
- Reusable field mappings
- CSV-based input
- Generates one PDF per CSV row

## Installation

**Requirements**

- Python 3.13 or newer

Clone the repository:

```bash
git clone https://github.com/ChriGaf/FormBadger.git
cd FormBadger
```

Create and activate a virtual environment:

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

Install FormBadger including dependencies:

```bash
pip install .
```

## Development

If you want to contribute to FormBadger, install it in editable mode together with the development dependencies:

```bash
pip install -e ".[dev]"
```

After installing the development dependencies, the following tools are available.

This project uses **Black** for code formatting. ✨ 🍰 ✨

Format the source code with:

```bash
black .
```

This project uses **Ruff** for linting.

Check the code:

```bash
ruff check .
```

Automatically fix issues where possible:

```bash
ruff check . --fix
```

This project uses **pytest** for unit testing.

Run the test suite with:

```bash
pytest
```

Typical workflow before committing:

```bash
ruff check . --fix
black .
pytest
```

## Quick Start

1. Analyze a PDF template to generate a field mapping.
2. Edit the generated CSV field mapping if necessary.
3. Fill the template using your input CSV data.

## Examples

*More to come*

## License

This project is dual-licensed under the MIT License and the Apache License (Version 2.0). 
You may choose to use this project under the terms of either license.

* See [LICENSE-MIT](LICENSE-MIT) for details.
* See [LICENSE-APACHE](LICENSE-APACHE) for details.