import os

__config = {
    **os.environ
}

def get(key: str) -> str:
    return (__config[key] if key in __config else '').strip()
