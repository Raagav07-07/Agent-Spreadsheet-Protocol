from asp.core.registry import register_handler
from asp.core.context import backend

@register_handler("READ_RANGE")
def read_range_handler(message):
    payload = message.get("payload", {})
    sheet = payload.get("sheet")
    cell_range = payload.get("range")

    rows = backend.read_range(sheet, cell_range)
    return {"rows": rows}
