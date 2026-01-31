TOOLS = [
    {
        "id": "SHEET_LIST",
        "name": "List Sheets",
        "description": "Returns all available sheet names",
        "input_schema": {},
        "permission": "read"
    },
    {
        "id": "READ_RANGE",
        "name": "Read Range",
        "description": "Read a specific cell range from a sheet",
        "input_schema": {
  "title": "READ_RANGE Payload",
  "type": "object",
  "required": ["sheet", "range"],
  "properties": {
    "sheet": { "type": "string" },
    "range": { "type": "string", "example": "A1:D100" }
  }
},
        "permission": "read"
    }
]
