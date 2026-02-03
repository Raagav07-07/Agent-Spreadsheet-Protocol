# Agent Spreadsheet Protocol (ASP)

A standard, declarative protocol for AI agents to safely interact with spreadsheet systems.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Agent Spreadsheet Protocol (ASP) solves the fragmentation problem where AI agents use ad-hoc APIs to interact with spreadsheets. ASP provides a **unified, platform-agnostic standard** for:

- ✅ Reading data ranges from spreadsheets
- ✅ Understanding spreadsheet semantics
- ✅ Safely writing data with approval workflows
- ✅ Auditing AI-driven changes
- ✅ Detecting anomalies and trends

### Why ASP?

Today, every AI integration writes custom glue code. ASP provides a **declarative, stateless message protocol** that works across Excel, Google Sheets, CSV engines, and other spreadsheet systems.

## Key Features

- **Declarative** – Agents specify what they want, not how to do it
- **Safe by Default** – Write operations can be proposed before execution
- **Auditable** – Every action is loggable and traceable
- **Stateless** – Each message is self-contained
- **Extensible** – New message types can be added without breaking compatibility
- **Platform Agnostic** – Works with any spreadsheet system

## Quick Start

### Installation

```bash
git clone https://github.com/yourusername/Agent-Spreadsheet-Protocol.git
cd Agent-Spreadsheet-Protocol
pip install -r requirements.txt
```

### Running the Server

```bash
# From the project root
python -m asp.server
```

The ASP server will start on `http://127.0.0.1:8001`

### Example: Reading a Sheet

```bash
curl -X GET http://127.0.0.1:8000/asp/discover
```

Response:

```json
{
  "status": "DISCOVER_RESPONSE",
  "data": {
    "tools": [...]
  }
}
```

## Architecture

```
Agent-Spreadsheet-Protocol/
├── asp/
│   ├── server.py           # FastAPI server
│   ├── core/              # Core protocol logic
│   │   ├── backend.py     # Abstract spreadsheet backend
│   │   ├── envelope.py    # Message envelope handling
│   │   ├── registry.py    # Handler registry
│   │   └── context.py     # Request context
│   ├── backends/          # Spreadsheet implementations
│   │   └── csv_backend.py # CSV file backend
│   ├── handlers/          # Message type handlers
│   │   ├── sheet_list.py  # SHEET_LIST handler
│   │   └── read_range.py  # READ_RANGE handler
│   └── data/              # Sample data
├── schemas/               # JSON schemas for validation
├── specification.md       # Full protocol specification
├── CONTRIBUTING.md        # Contribution guidelines
└── README.md              # This file
```

## Core Message Types

### Read/Query Operations

- `SHEET_LIST` – List all available sheets
- `SHEET_SCHEMA` – Get column definitions and types
- `READ_RANGE` – Read specific cell ranges
- `SHEET_SUMMARY` – High-level data overview

### Write Operations

- `WRITE_RANGE` – Direct cell writes (requires approval)
- `FORMULA_INSERT` – Insert formulas
- `STRUCTURE_CHANGE` – Modify sheet structure

### Intelligence Operations

- `ANOMALY_DETECT` – Identify outliers
- `TREND_ANALYSIS` – Detect patterns
- `INSIGHT_REPORT` – Generate summaries

### Safety/Control

- `ACTION_PROPOSE` – Suggest a write operation
- `ACTION_APPROVE` – Approve an action
- `ACTION_EXECUTE` – Execute an approved action
- `AUDIT_LOG` – Record and retrieve activity

## Message Format

All ASP messages follow this envelope structure:

```json
{
  "asp_version": "1.0",
  "message_id": "uuid",
  "sender": "agent | spreadsheet",
  "type": "MESSAGE_TYPE",
  "timestamp": "2026-01-28T10:00:00Z",
  "payload": {}
}
```

## Example Usage

### 1. Get Available Sheets

```json
{
  "type": "SHEET_LIST",
  "payload": {}
}
```

### 2. Read a Data Range

```json
{
  "type": "READ_RANGE",
  "payload": {
    "sheet": "Sales",
    "range": "A1:D100"
  }
}
```

### 3. Propose a Write Operation

```json
{
  "type": "ACTION_PROPOSE",
  "payload": {
    "action": "WRITE_RANGE",
    "sheet": "Sales",
    "range": "E1:E100",
    "values": [...]
  }
}
```

## API Endpoints

| Method | Endpoint        | Description                           |
| ------ | --------------- | ------------------------------------- |
| GET    | `/asp/discover` | Get available tools and message types |
| POST   | `/asp`          | Send ASP message to handler           |
| GET    | `/docs`         | Swagger API documentation             |

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code style guidelines
- How to submit issues and PRs
- Development setup
- Testing requirements

## Using with AI Agents

ASP includes a built-in agent powered by Google ADK that can interact with your spreadsheets:

### Setup

1. Set up environment variables:

   ```bash
   cp asp/spreadsheet_agent/.env.example asp/spreadsheet_agent/.env
   # Edit with your Gemini API key
   ```

2. Start the ASP server:

   ```bash
   python -m asp.server
   ```

3. Launch the agent (in a separate terminal):

   ```bash
   adk web asp/spreadsheet_agent
   ```

4. Open your browser to `http://127.0.0.1:8080` and start chatting with the agent!

### How the Agent Works

The agent uses three tools to safely interact with your spreadsheets:

- **Discover** – Queries what tools are available
- **List Sheets** – Shows all available sheets
- **Read Range** – Fetches data from specific cell ranges

The agent intelligently discovers available tools before using them and focuses only on tools needed to answer your questions.

## Supported Backends

- **CSV** – Local CSV files
- **Google Sheets** – Via Google Sheets API (coming soon)
- **Excel** – Via pywin32/openpyxl (coming soon)
- **Airtable** – Via Airtable API (coming soon)

## Specification

For detailed protocol specification, message types, and examples, see [specification.md](specification.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Complete message type implementations
- [ ] Add Google Sheets backend
- [ ] Add Excel backend
- [ ] Web UI for monitoring
- [ ] Python SDK for agents
- [ ] JavaScript/Node.js SDK
- [ ] Go implementation

## Support

- 📖 [Full Specification](specification.md)
- 🐛 [Report Issues](../../issues)
- 💬 [Discussions](../../discussions)

## Authors

- Created as a standardization effort for AI-spreadsheet interactions
