# Quick Start Guide

Get up and running with Agent Spreadsheet Protocol in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Agent-Spreadsheet-Protocol.git
cd Agent-Spreadsheet-Protocol
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If `requirements.txt` doesn't exist, install manually:
```bash
pip install fastapi uvicorn pandas narwhals
```

## Running the Server

From the project root:

```bash
python -m asp.server
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

The server is now running and ready to accept ASP messages!

## Testing the API

### Option 1: Using cURL

Open a new terminal and try these commands:

**Discover available tools:**
```bash
curl http://localhost:8000/asp/discover
```

**List sheets:**
```bash
curl -X POST http://localhost:8000/asp \
  -H "Content-Type: application/json" \
  -d '{"type": "SHEET_LIST", "payload": {}}'
```

**Read a range:**
```bash
curl -X POST http://localhost:8000/asp \
  -H "Content-Type: application/json" \
  -d '{
    "type": "READ_RANGE",
    "payload": {
      "sheet": "sales",
      "range": "A1:D10"
    }
  }'
```

### Option 2: Using Python

Create a file `test_asp.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Discover tools
response = requests.get(f"{BASE_URL}/asp/discover")
print("Available Tools:")
print(json.dumps(response.json(), indent=2))

# List sheets
message = {"type": "SHEET_LIST", "payload": {}}
response = requests.post(f"{BASE_URL}/asp", json=message)
print("\nAvailable Sheets:")
print(json.dumps(response.json(), indent=2))

# Read range
message = {
    "type": "READ_RANGE",
    "payload": {
        "sheet": "sales",
        "range": "A1:D10"
    }
}
response = requests.post(f"{BASE_URL}/asp", json=message)
print("\nData Read:")
print(json.dumps(response.json(), indent=2))
```

Run it:
```bash
python test_asp.py
```

### Option 3: Interactive API Docs

Open your browser to:
```
http://localhost:8000/docs
```

This shows an interactive Swagger UI where you can test the API directly.

## Understanding the Response

A successful response looks like:

```json
{
  "status": "DATA_RESPONSE",
  "data": {
    "sheets": ["sales"]
  }
}
```

- `status` – Response type (`DATA_RESPONSE`, `ERROR`, etc.)
- `data` – The actual response data

An error response:

```json
{
  "status": "ERROR",
  "data": {
    "code": "SHEET_NOT_FOUND",
    "message": "Sheet 'sales' does not exist"
  }
}
```

## Sample Data

The project includes sample data in `asp/data/sales.csv`. The server uses this for testing.

**Sample sheet name:** `sales`
**Available columns:** Check by running READ_RANGE

## Next Steps

1. **Read the Specification**
   - See `specification.md` for complete protocol details

2. **Explore the API**
   - See `API.md` for all available endpoints and message types

3. **Understand the Architecture**
   - See `DEVELOPMENT.md` for architectural details

4. **Contribute**
   - See `CONTRIBUTING.md` to contribute to the project

## Common Issues

### "ModuleNotFoundError: No module named 'asp'"

**Solution:** Make sure you're running from the project root:
```bash
# Correct
cd Agent-Spreadsheet-Protocol
python -m asp.server

# Wrong
cd Agent-Spreadsheet-Protocol/asp
python server.py
```

### "Address already in use"

**Solution:** The port 8000 is already in use. Either:
- Kill the process using port 8000
- Or modify the port in `server.py`:
  ```python
  if __name__ == "__main__":
      import uvicorn
      uvicorn.run(app, host="127.0.0.1", port=8001)  # Changed to 8001
  ```

### Virtual environment not activating

**Make sure to activate it:**

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

## Project Structure Overview

```
Agent-Spreadsheet-Protocol/
├── asp/
│   ├── server.py           ← Start here: Main FastAPI server
│   ├── core/              ← Core protocol logic
│   ├── backends/          ← Spreadsheet implementations
│   ├── handlers/          ← Message type handlers
│   └── data/              ← Sample data
├── tests/                 ← Test files
├── schemas/               ← JSON schemas
├── README.md              ← Full project overview
├── API.md                 ← API reference
├── specification.md       ← Protocol specification
├── DEVELOPMENT.md         ← Development guide
└── CONTRIBUTING.md        ← How to contribute
```

## Making Your First Request

Here's a complete example in Python:

```python
import requests

# Configuration
BASE_URL = "http://localhost:8000"

# Create a message
message = {
    "type": "READ_RANGE",
    "payload": {
        "sheet": "sales",
        "range": "A1:C5"
    }
}

# Send request
response = requests.post(f"{BASE_URL}/asp", json=message)

# Handle response
if response.status_code == 200:
    data = response.json()
    if data["status"] == "DATA_RESPONSE":
        print("Success! Data:", data["data"])
    else:
        print("Error:", data["data"])
else:
    print(f"HTTP Error: {response.status_code}")
```

## Performance Considerations

- Reading large ranges (>100,000 rows) may take time
- Currently, entire ranges are loaded into memory
- Streaming large datasets is planned for future versions

## Stopping the Server

Press `Ctrl+C` in the terminal running the server.

## Getting Help

- 📖 [Full Documentation](README.md)
- 🔧 [API Reference](API.md)
- 📋 [Specification](specification.md)
- 🚀 [Development Guide](DEVELOPMENT.md)
- 🤝 [Contributing Guide](CONTRIBUTING.md)
- 🐛 [Report Issues](../../issues)

---

**You're all set!** 🎉 

Start making requests to `http://localhost:8000/asp` and explore the ASP protocol.
