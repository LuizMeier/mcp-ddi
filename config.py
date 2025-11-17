"""Configuration module for DDI API connection parameters."""
import os
from dotenv import load_dotenv

load_dotenv()

WAPI_URL = os.getenv("WAPI_URL")
WAPI_USER = os.getenv("WAPI_USER")
WAPI_PASS = os.getenv("WAPI_PASS")

WAPI_VERIFY_SSL = os.getenv("WAPI_VERIFY_SSL", "True").lower() in ("true", "1", "yes")

if not all([WAPI_URL, WAPI_USER, WAPI_PASS]):
    raise ValueError("Missing one or more required environment variables.")
