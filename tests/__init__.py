import os, sys
from pathlib import Path

# Change python path to app directory
app_path = str((Path(__file__).parent.parent / 'app').absolute())
sys.path.append(app_path)

from constants import KEY_JWT_SECRET, KEY_POSTGRESQL_HOST, KEY_VONAGE_API_KEY

# Make sure the app runs using an ephemeral db and mock verification service
os.environ[KEY_JWT_SECRET] = 'myTestSecret'
if KEY_POSTGRESQL_HOST in os.environ:
    del os.environ[KEY_POSTGRESQL_HOST]
if KEY_VONAGE_API_KEY in os.environ:
    del os.environ[KEY_VONAGE_API_KEY]
