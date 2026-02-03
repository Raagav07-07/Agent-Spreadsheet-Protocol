from fastapi import FastAPI
from asp.core.registry import get_handler
from asp.core.envelope import asp_response
from asp.discover import TOOLS
import asp.handlers.sheet_list
import asp.handlers.read_range

app=FastAPI()
@app.post("/asp")
async def asp_endpoint(message: dict):
    message_type = message.get("type")
    handler = get_handler(message_type)
    if not handler:
        return asp_response("ERROR", {
            "code": "UNKNOWN_TYPE",
            "message": f"No handler for {message_type}"
        })
    result = handler(message)
    return asp_response("DATA_RESPONSE", result)

@app.get("/asp/discover")
async def asp_discover():
    return asp_response("DISCOVER_RESPONSE", {
        "tools": TOOLS
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

