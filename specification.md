# Agent Spreadsheet Protocol

## Problem  

Today AI agents spread spreadsheets via ad-hoc api. Every app writes custom glue codes.  
There is no standard way to, 
- Read ranges
- Understand sheet semantics
- write back safely
- Audit actions
- Track AI-made changes

ASP solves this by defining a standard conversation between AI Agent and Spreadsheet System (Excel, Google sheets, CSV engine etc..).  

## Roles

Role A - Agent  
- LLM/AI Agent
- Requests data
- Perfrom Analysis
- Proposes or executes actions  

Role B - Spreadsheet Host  
- Google sheets
- Excel  
- CSV Engine  
- Airtable-like systems

ASP is platform agnostic.  

## Design principles  

ASP follows 5 principles:

1. Declarative – Agent says what it wants, not how
2. Safe by default – Writes can be proposed before execution
3. Auditable – Every action is loggable
4. Stateless messages – Each message is self-contained
5. Extensible – New message types can be added

## ASP Message template  

```
{
  "asp_version": "1.0",
  "message_id": "uuid",
  "sender": "agent | spreadsheet",
  "type": "MESSAGE_TYPE",
  "timestamp": "ISO-8601",
  "payload": {}
}
```

## Core message types

1. Read/Understand 
- SHEET_LIST -- List all sheets  
- SHEET_SCHEMA -- Understand column meanings  
- READ_RANGE -- Read specific cells
- SHEET_SUMMARY -- High-level understanding of data

2. Write/Modify  
- WRITE_RANGE -- Direct write
- FORMULA_INSERT -- Insert formulas  
- STRUCTURE_CHANGE -- Add/remove rows, columns, sheets  

3. Intelligence  
- ANOMALY_DETECT -- Detect outliers  
- TREND_ANALYSIS -- Detect trends  
- INSIGHT_REPORT -- Human-readable summary  

4. Safety/Control  
- ACTION_PROPOSE -- Suggest a change 
- ACTION_APPROVE -- Human or system approval  
- ACTION_EXECUTE -- Perform approved change  
- AUDIT_LOG -- Record AI activity  

## Example : Simple ASP Conversation  
 - Step 1 : Agent asks for data  
 ```
 {
  "asp_version": "1.0",
  "message_id": "123",
  "sender": "agent",
  "type": "READ_RANGE",
  "timestamp": "2026-01-28T10:00:00Z",
  "payload": {
    "sheet": "Sales",
    "range": "A1:D100"
  }
}
```

- Step 2 : Spreadsheet responds  
```
{
  "asp_version": "1.0",
  "message_id": "124",
  "sender": "spreadsheet",
  "type": "READ_RANGE_RESULT",
  "timestamp": "2026-01-28T10:00:01Z",
  "payload": {
    "rows": [
      ["Date", "Product", "Units", "Revenue"],
      ["2026-01-01", "Shoes", 20, 4000]
    ]
  }
}
```

- Step 3 : Agent proposes a write  
```
{
  "asp_version": "1.0",
  "message_id": "125",
  "sender": "agent",
  "type": "ACTION_PROPOSE",
  "timestamp": "2026-01-28T10:00:05Z",
  "payload": {
    "action": "WRITE_RANGE",
    "details": {
      "sheet": "Sales",
      "range": "E1",
      "value": "Revenue per Unit"
    }
  }
}
```

## State flow  

DISCOVER → READ → ANALYZE → PROPOSE → APPROVE → EXECUTE → LOG

