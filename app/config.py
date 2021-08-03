import os

__config = {
    **os.environ
}

def get(key):
    return __config[key] if key in __config else None
