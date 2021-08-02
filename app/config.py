import os
from dotenv.main import dotenv_values

__config = {
    **dotenv_values('../.env'),
    **os.environ
}

def get(key):
    return __config[key] if key in __config else None
