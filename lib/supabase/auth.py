"""
Supabase authentication utilities.
"""

import os
from .supabase_client import supabase

def authenticate_service():
    """
    Authenticate with Supabase using service role credentials.
    """
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not service_role_key:
        raise ValueError(
            "Missing SUPABASE_SERVICE_ROLE_KEY. "
            "Please ensure it is set in .env file"
        )
    
    # For service role auth, we need to use a special header
    supabase.postgrest.auth(service_role_key)
