"""
Supabase client configuration and initialization.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError(
        "Missing Supabase credentials. "
        "Please ensure SUPABASE_URL and SUPABASE_KEY are set in .env file"
    )

supabase: Client = create_client(url, key)
