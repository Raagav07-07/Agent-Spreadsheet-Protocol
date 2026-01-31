from asp.core.registry import register_handler
from asp.core.context import backend

@register_handler("SHEET_LIST")
def sheet_list_handler(message):
    sheets = backend.list_sheets()
    return {"sheets": sheets}