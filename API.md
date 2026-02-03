# ASP API Documentation

Complete reference for the Agent Spreadsheet Protocol HTTP API.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. This is planned for future releases.

## Response Format

All responses follow the ASP envelope format:

```json
{
  "status": "RESPONSE_TYPE",
  "data": {}
}
```

**Response Types:**

- `DATA_RESPONSE` – Successful data operation
- `DISCOVER_RESPONSE` – Tool/capability discovery
- `ERROR` – Error occurred

## Endpoints

### 1. Discover Tools

Retrieve available tools and message types the server supports.

**Request**

```http
GET /asp/discover
```

**Response (200 OK)**

```json
{
  "status": "DISCOVER_RESPONSE",
  "data": {
    "tools": [
      {
        "name": "list_sheets",
        "description": "List all available sheets",
        "message_type": "SHEET_LIST",
        "input_schema": { ... }
      },
      {
        "name": "read_range",
        "description": "Read a range of cells from a sheet",
        "message_type": "READ_RANGE",
        "input_schema": { ... }
      }
    ]
  }
}
```

**cURL Example**

```bash
curl -X GET http://localhost:8000/asp/discover
```

---

### 2. Send ASP Message

Send a message to be processed by the appropriate handler.

**Request**

```http
POST /asp
Content-Type: application/json

{
  "type": "MESSAGE_TYPE",
  "payload": { ... }
}
```

**Response (200 OK)**

```json
{
  "status": "DATA_RESPONSE",
  "data": { ... }
}
```

**Response (400 Bad Request)**

```json
{
  "status": "ERROR",
  "data": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid message format"
  }
}
```

**Response (404 Not Found)**

```json
{
  "status": "ERROR",
  "data": {
    "code": "UNKNOWN_TYPE",
    "message": "No handler for MESSAGE_TYPE"
  }
}
```

---

## Message Types

### SHEET_LIST

List all available sheets in the connected backend.

**Request**

```json
{
  "type": "SHEET_LIST",
  "payload": {}
}
```

**Response**

```json
{
  "status": "DATA_RESPONSE",
  "data": {
    "sheets": ["Sales", "Inventory", "Employees"]
  }
}
```

**cURL Example**

```bash
curl -X POST http://localhost:8000/asp \
  -H "Content-Type: application/json" \
  -d '{
    "type": "SHEET_LIST",
    "payload": {}
  }'
```

---

### READ_RANGE

Read a range of cells from a specific sheet.

**Request**

```json
{
  "type": "READ_RANGE",
  "payload": {
    "sheet": "Sales",
    "range": "A1:D100"
  }
}
```

**Request Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| sheet | string | Yes | Name of the sheet to read from |
| range | string | Yes | Range in format "A1:D100" |

**Response**

```json
{
  "status": "DATA_RESPONSE",
  "data": {
    "rows": [
      { "A": "Product", "B": "Quantity", "C": "Price", "D": "Total" },
      { "A": "Widget", "B": 10, "C": 29.99, "D": 299.9 },
      { "A": "Gadget", "B": 5, "C": 49.99, "D": 249.95 }
    ],
    "range": "A1:D3"
  }
}
```

**cURL Example**

```bash
curl -X POST http://localhost:8000/asp \
  -H "Content-Type: application/json" \
  -d '{
    "type": "READ_RANGE",
    "payload": {
      "sheet": "Sales",
      "range": "A1:D100"
    }
  }'
```

**Error Cases**

```json
{
  "status": "ERROR",
  "data": {
    "code": "SHEET_NOT_FOUND",
    "message": "Sheet 'Sales' does not exist"
  }
}
```

```json
{
  "status": "ERROR",
  "data": {
    "code": "INVALID_RANGE",
    "message": "Invalid range format: A1:D100"
  }
}
```

---

## Planned Message Types

### WRITE_RANGE

Write data to a range of cells.

```json
{
  "type": "WRITE_RANGE",
  "payload": {
    "sheet": "Sales",
    "range": "E1:E100",
    "values": [[100], [200], [300]]
  }
}
```

---

### ACTION_PROPOSE

Propose an action for human approval before execution.

```json
{
  "type": "ACTION_PROPOSE",
  "payload": {
    "action": "WRITE_RANGE",
    "sheet": "Sales",
    "range": "E1:E100",
    "values": [...],
    "rationale": "Calculating totals based on quantity × price"
  }
}
```

---

### ACTION_EXECUTE

Execute a previously approved action.

```json
{
  "type": "ACTION_EXECUTE",
  "payload": {
    "action_id": "uuid",
    "approval_id": "uuid"
  }
}
```

---

### SHEET_SCHEMA

Get column definitions and data types for a sheet.

```json
{
  "type": "SHEET_SCHEMA",
  "payload": {
    "sheet": "Sales"
  }
}
```

Response:

```json
{
  "status": "DATA_RESPONSE",
  "data": {
    "columns": [
      {
        "name": "Product",
        "index": 0,
        "type": "string"
      },
      {
        "name": "Quantity",
        "index": 1,
        "type": "number"
      }
    ]
  }
}
```

---

## HTTP Status Codes

| Code | Meaning                          |
| ---- | -------------------------------- |
| 200  | Success                          |
| 400  | Bad Request (validation error)   |
| 404  | Not Found (unknown message type) |
| 500  | Internal Server Error            |

## Error Response Format

All errors follow this format:

```json
{
  "status": "ERROR",
  "data": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {} // Optional additional details
  }
}
```

**Common Error Codes:**

- `UNKNOWN_TYPE` – Message type not recognized
- `VALIDATION_ERROR` – Invalid message format
- `SHEET_NOT_FOUND` – Referenced sheet doesn't exist
- `INVALID_RANGE` – Invalid cell range format
- `BACKEND_ERROR` – Error from spreadsheet backend
- `INTERNAL_ERROR` – Unexpected server error

---

## Rate Limiting

Rate limiting is not currently implemented but is planned for future releases.

---

## CORS

CORS is currently enabled for all origins. This will be configurable in production.

---

## Example: Complete Workflow

```bash
# 1. Discover available tools
curl -X GET http://localhost:8000/asp/discover

# 2. List sheets
curl -X POST http://localhost:8000/asp \
  -H "Content-Type: application/json" \
  -d '{"type": "SHEET_LIST", "payload": {}}'

# 3. Read data
curl -X POST http://localhost:8000/asp \
  -H "Content-Type: application/json" \
  -d '{
    "type": "READ_RANGE",
    "payload": {
      "sheet": "Sales",
      "range": "A1:D10"
    }
  }'
```

---

## Swagger/OpenAPI

Interactive API documentation is available at:

```
http://localhost:8000/docs
```

Alternative docs (ReDoc):

```
http://localhost:8000/redoc
```

---

## WebSocket Support

WebSocket support is planned for future releases to enable real-time updates and streaming responses.

---

## Versioning

Current API Version: **1.0**

API version is specified in the message envelope (if applicable) and will be maintained for backward compatibility.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for API changes across versions.

---

## Support

For issues or questions about the API:

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](../../issues)
- 📧 Contact: [your-email@example.com]
