"""
Module for fetching videos that are due for publishing from the video_schedule table.
"""

from typing import List, Dict, Any
from datetime import datetime
from .supabase_client import supabase

def fetch_due_videos() -> List[Dict[str, Any]]:
    """
    Fetch all unpublished videos that are due for publishing (scheduled_at <= current time).
    
    Returns:
        List[Dict[str, Any]]: List of video schedule entries that are due for publishing.
        Each entry contains all columns from the video_schedule table.
        
    Raises:
        Exception: If the Supabase query fails
    """
    # Use UTC time for consistency across different timezones
    now = datetime.utcnow().isoformat()

    try:
        response = supabase.table("video_schedule") \
            .select("*") \
            .eq("published", False) \
            .lte("scheduled_at", now) \
            .order("scheduled_at") \
            .execute()

        # The response data is directly in the response object
        return response.data
    
    except Exception as e:
        raise Exception(f"Failed to fetch due videos: {str(e)}")
