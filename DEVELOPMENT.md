# Development Guide

This guide covers development setup, architecture, and best practices for ASP.

## Table of Contents

- [Setup](#setup)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Adding New Backends](#adding-new-backends)
- [Adding New Handlers](#adding-new-handlers)
- [Testing](#testing)
- [Debugging](#debugging)

## Setup

### Prerequisites

- Python 3.8+
- pip or conda
- Git

### Initial Setup

```bash
# Clone repository
git clone https://github.com/yourusername/Agent-Spreadsheet-Protocol.git
cd Agent-Spreadsheet-Protocol

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Verify setup
python -m asp.server
```

## Project Structure

```
asp/
├── __init__.py
├── server.py              # FastAPI application entry point
├── discover.py            # Tool discovery
├── core/
│   ├── __init__.py
│   ├── backend.py         # Abstract base class for backends
│   ├── envelope.py        # ASP message envelope handling
│   ├── registry.py        # Message handler registry
│   └── context.py         # Request context
├── backends/
│   ├── __init__.py
│   └── csv_backend.py     # CSV file backend
├── handlers/
│   ├── __init__.py
│   ├── sheet_list.py      # SHEET_LIST handler
│   └── read_range.py      # READ_RANGE handler
└── data/
    └── sales.csv          # Sample data

tests/
├── test_backends.py
├── test_handlers.py
└── test_core.py

schemas/
├── envelope.schema.json
├── read_range.schema.json
├── write_range.schema.json
└── action_propose.schema.json
```

## Architecture

### Core Components

#### 1. **Backend System** (`core/backend.py`)

Abstract base class defining the spreadsheet backend interface:

```python
class SpreadsheetBackend(ABC):
    @abstractmethod
    def list_sheets(self) -> list[str]:
        """List all available sheets."""

    @abstractmethod
    def read_range(self, sheet: str, cell_range: str) -> list[dict]:
        """Read a specific range from a sheet."""
```

Implementations:

- `CSVBackend` – Local CSV files
- `GoogleSheetsBackend` – Google Sheets API (coming soon)
- `ExcelBackend` – Excel files (coming soon)

#### 2. **Message Envelope** (`core/envelope.py`)

Handles ASP message format and validation:

```python
def asp_response(status: str, data: dict) -> dict:
    """Wrap response in ASP envelope."""

def validate_message(message: dict, schema_name: str) -> bool:
    """Validate message against JSON schema."""
```

#### 3. **Handler Registry** (`core/registry.py`)

Maps message types to handler functions:

```python
def register_handler(message_type: str, handler: callable) -> None:
    """Register a handler for a message type."""

def get_handler(message_type: str) -> callable:
    """Get handler for a message type."""
```

#### 4. **Message Handlers** (`handlers/`)

Each handler processes a specific message type and delegates to appropriate backend:

```python
def handle_sheet_list(message: dict, backend: SpreadsheetBackend) -> dict:
    """Handle SHEET_LIST message."""
    return {"sheets": backend.list_sheets()}
```

### Request Flow

```
HTTP Request
    ↓
server.py: /asp endpoint
    ↓
registry.get_handler(message_type)
    ↓
handler_function(message)
    ↓
backend.method(...)
    ↓
asp_response(status, data)
    ↓
HTTP Response
```

## Adding New Backends

### Step 1: Create Backend Class

Create `asp/backends/yourbackend.py`:

```python
from abc import ABC, abstractmethod
from asp.core.backend import SpreadsheetBackend

class YourBackend(SpreadsheetBackend):
    """Backend for [Your System]."""

    def __init__(self, config: dict):
        """Initialize backend with configuration."""
        self.config = config

    def list_sheets(self) -> list[str]:
        """List all available sheets."""
        # Implementation here
        pass

    def read_range(self, sheet: str, cell_range: str) -> list[dict]:
        """Read a specific range from a sheet."""
        # Implementation here
        pass
```

### Step 2: Register in Server

Update `server.py`:

```python
from asp.backends.yourbackend import YourBackend

# Create instance
backend = YourBackend(config={...})

@app.post("/asp")
async def asp_endpoint(message: dict):
    handler = get_handler(message.get("type"))
    result = handler(message, backend)
    return asp_response("DATA_RESPONSE", result)
```

### Step 3: Write Tests

Create `tests/test_yourbackend.py`:

```python
import pytest
from asp.backends.yourbackend import YourBackend

class TestYourBackend:
    @pytest.fixture
    def backend(self):
        return YourBackend(config={...})

    def test_list_sheets(self, backend):
        sheets = backend.list_sheets()
        assert isinstance(sheets, list)
```

## Adding New Handlers

### Step 1: Create Handler

Create `asp/handlers/your_handler.py`:

```python
from asp.core.backend import SpreadsheetBackend
from asp.core.registry import register_handler

def handle_your_message(message: dict, backend: SpreadsheetBackend) -> dict:
    """
    Handle YOUR_MESSAGE_TYPE message.

    Args:
        message: ASP message dict
        backend: SpreadsheetBackend instance

    Returns:
        Result dictionary
    """
    payload = message.get("payload", {})

    # Validate
    if "required_field" not in payload:
        raise ValueError("Missing required_field")

    # Process
    result = backend.your_method(payload["required_field"])

    return {"result": result}

# Register handler
register_handler("YOUR_MESSAGE_TYPE", handle_your_message)
```

### Step 2: Import in Server

Update `server.py`:

```python
import asp.handlers.your_handler
```

### Step 3: Define Schema

Create `schemas/your_message.schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "required_field": {
      "type": "string",
      "description": "Description of field"
    }
  },
  "required": ["required_field"]
}
```

## Testing

### Running Tests

```bash
# All tests
python -m pytest

# Specific file
python -m pytest tests/test_backends.py

# Specific test
python -m pytest tests/test_backends.py::TestCSVBackend::test_read_range

# With coverage
python -m pytest --cov=asp tests/

# With output
python -m pytest -v
```

### Test Structure

```python
import pytest
from asp.backends.csv_backend import CSVBackend

class TestCSVBackend:
    """Test suite for CSVBackend."""

    @pytest.fixture
    def backend(self):
        """Fixture: create backend instance."""
        return CSVBackend()

    @pytest.fixture
    def sample_data(self):
        """Fixture: sample test data."""
        return ["row1", "row2"]

    def test_initialization(self, backend):
        """Test: backend initializes correctly."""
        assert backend is not None

    def test_list_sheets(self, backend):
        """Test: list_sheets returns list."""
        result = backend.list_sheets()
        assert isinstance(result, list)
```

### Mocking

```python
from unittest.mock import Mock, patch

def test_with_mock():
    mock_backend = Mock()
    mock_backend.list_sheets.return_value = ["Sheet1", "Sheet2"]

    result = mock_backend.list_sheets()
    assert result == ["Sheet1", "Sheet2"]
```

## Debugging

### Print Debugging

```python
import sys

def debug(msg, *args):
    print(f"DEBUG: {msg}", *args, file=sys.stderr)

debug("Variable value:", variable_name)
```

### Using Python Debugger

```python
import pdb

def problematic_function():
    pdb.set_trace()  # Execution pauses here
    # Use: l (list), n (next), c (continue), p (print)
```

### VS Code Debugging

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["asp.server:app", "--reload"],
      "jinja": true
    }
  ]
}
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

Configure in `server.py`:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Performance Tips

1. **Cache sheet lists** if backends don't change frequently
2. **Stream large ranges** instead of loading all data
3. **Lazy-load backends** (create only when needed)
4. **Use indexes** for CSV files with many rows
5. **Profile with cProfile**:
   ```python
   import cProfile
   cProfile.run('your_function()')
   ```

## Documentation Standards

- Docstrings for all public functions
- Type hints for all parameters
- Examples in docstrings for complex functions
- Update README when adding features
- Keep API docs in sync with code

## Release Checklist

- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Tag created

---

Happy coding! 🚀
