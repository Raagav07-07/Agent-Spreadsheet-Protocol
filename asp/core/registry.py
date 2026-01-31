HANDLERS = {}

def register_handler(message_type):
    def decorator(func):
        HANDLERS[message_type] = func
        return func
    return decorator
def get_handler(message_type):
    return HANDLERS.get(message_type)
