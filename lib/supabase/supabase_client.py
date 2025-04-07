"""
Supabase client configuration and initialization.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client with service role key for background jobs
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_SERVICE_KEY")  # Use service role key for background jobs

if not url or not key:
    raise ValueError(
        "Missing Supabase credentials. "
        "Please ensure SUPABASE_URL and SUPABASE_SERVICE_KEY are set in .env file"
    )

# Create client with service role key - this allows us to bypass RLS
supabase: Client = create_client(url, key)
