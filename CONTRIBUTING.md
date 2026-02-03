# Contributing to Agent Spreadsheet Protocol

Thank you for your interest in contributing to ASP! We welcome contributions of all kinds, including bug reports, feature requests, documentation improvements, and code submissions.

## Code of Conduct

Please be respectful and inclusive. We are committed to providing a welcoming environment for all contributors.

## How to Contribute

### 1. Reporting Bugs

Found a bug? Please create an issue with:

- **Clear title** describing the problem
- **Steps to reproduce** the issue
- **Expected behavior** vs. actual behavior
- **Environment details** (OS, Python version, etc.)
- **Screenshots or error logs** if applicable

### 2. Suggesting Features

Have an idea for improvement? Open an issue with:

- **Descriptive title**
- **Use case** explaining why this feature is needed
- **Proposed solution** (optional)
- **Alternative approaches** (optional)

### 3. Submitting Code Changes

#### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/Agent-Spreadsheet-Protocol.git
cd Agent-Spreadsheet-Protocol

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

#### Making Changes

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```

2. **Make your changes**
   - Follow the code style guidelines (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**

   ```bash
   python -m pytest tests/
   ```

4. **Commit with clear messages**

   ```bash
   git add .
   git commit -m "feat: Add new feature"
   # or
   git commit -m "fix: Resolve issue with X"
   git commit -m "docs: Update README with examples"
   ```

5. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Clear title and description
   - Reference any related issues (#123)
   - Explain the changes and why they're needed

## Code Style Guidelines

### Python

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these specific rules:

- **Line length**: Maximum 100 characters
- **Indentation**: 4 spaces
- **Imports**: Group standard library, third-party, local (alphabetically within groups)
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes

Example:

```python
# Standard library imports
import os
import json

# Third-party imports
from fastapi import FastAPI
import pandas as pd

# Local imports
from asp.core.backend import SpreadsheetBackend
from asp.core.envelope import asp_response

# Function naming
def parse_range(cell_range: str) -> tuple:
    """Parse cell range format like 'A1:D100'."""
    # implementation
    pass

# Class naming
class CSVBackend(SpreadsheetBackend):
    """Backend implementation for CSV files."""
    pass
```

### Type Hints

Use type hints for all functions:

```python
def read_range(self, sheet: str, cell_range: str) -> list[dict]:
    """
    Read a range of cells from a sheet.

    Args:
        sheet: Sheet name
        cell_range: Range in format 'A1:D100'

    Returns:
        List of dictionaries representing rows
    """
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def your_function(param1: str, param2: int) -> bool:
    """
    Brief one-line description.

    Longer description if needed, explaining purpose and behavior.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When X happens
        TypeError: When Y happens
    """
    pass
```

## Testing

All contributions should include tests.

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_csv_backend.py

# Run with coverage
python -m pytest --cov=asp tests/
```

### Writing Tests

```python
import pytest
from asp.backends.csv_backend import CSVBackend

class TestCSVBackend:
    """Test suite for CSVBackend."""

    @pytest.fixture
    def backend(self):
        """Create a test backend instance."""
        return CSVBackend(folder="test_data")

    def test_list_sheets(self, backend):
        """Test listing available sheets."""
        sheets = backend.list_sheets()
        assert isinstance(sheets, list)
        assert len(sheets) > 0

    def test_parse_range_valid(self, backend):
        """Test parsing valid range format."""
        result = backend.parse_range("A1:D100")
        assert result == (0, 100, 0, 4)

    def test_parse_range_invalid(self, backend):
        """Test parsing invalid range raises error."""
        with pytest.raises(ValueError):
            backend.parse_range("invalid")
```

## Documentation

### Updating README

- Keep it accurate and up-to-date
- Include examples where applicable
- Update the Table of Contents if adding new sections

### API Documentation

- Add docstrings to all public functions
- Document all parameters and return types
- Include error conditions

### Architecture Documentation

For significant changes to architecture:

- Update relevant `.md` files
- Include diagrams if helpful
- Explain design decisions

## File Structure

When adding new features:

```
asp/
├── backends/          # Spreadsheet backend implementations
├── handlers/          # Message type handlers
├── core/             # Core protocol logic
└── schemas/          # JSON schemas

tests/
├── test_backends/    # Backend tests
├── test_handlers/    # Handler tests
└── test_core/        # Core logic tests
```

## Commit Message Convention

Use conventional commits:

```
<type>: <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (no logic change)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Build, dependencies, etc.

**Examples:**

```
feat: Add Google Sheets backend

fix: Resolve parsing issue with quoted cells

docs: Update API endpoint documentation

test: Add test cases for col_to_index method
```

## Pull Request Process

1. **Before submitting:**
   - [ ] Tests pass locally
   - [ ] Code follows style guidelines
   - [ ] Documentation is updated
   - [ ] Commits are clean and well-described

2. **PR description should include:**
   - [ ] What problem does this solve?
   - [ ] How does it solve it?
   - [ ] Any breaking changes?
   - [ ] Screenshots/examples if applicable

3. **Review process:**
   - At least one review from maintainers
   - Address feedback constructively
   - Keep PR focused and reasonably sized (< 400 lines)

4. **Merging:**
   - All checks pass (tests, linting, coverage)
   - At least one approval
   - Branch is up to date with main

## Branching Strategy

- `main` – Production-ready code
- `develop` – Development branch (if used)
- `feature/name` – New features
- `fix/issue-number` – Bug fixes
- `docs/description` – Documentation updates

## Release Process

Maintainers will:

1. Update version number
2. Update CHANGELOG
3. Create release tag
4. Deploy to PyPI (when applicable)

## Getting Help

- **Questions?** Open a discussion or issue
- **Need clarification?** Ask in PR comments
- **Having trouble?** Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make ASP better! 🎉
