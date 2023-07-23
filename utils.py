import os
from dotenv import load_dotenv

# Load env value with `key` from .env
def get_env(key):
    try:
        # Load environment variables from .env file
        load_dotenv()

        return os.getenv(key)
    except Exception as e:
        raise e
