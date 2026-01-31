from uuid import uuid4
from datetime import datetime

def asp_response(msg_type, payload):
    return {
        "asp_version":"1.0",
        "message_id":str(uuid4()),
        "sender":"spreadsheet",
        "type":msg_type,
        "timestamp":datetime.utcnow().isoformat(),
        "payload":payload
    }