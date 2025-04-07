"""
Functions for fetching videos scheduled for publishing.
"""

import os
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from .client import supabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_due_videos() -> List[Dict[str, Any]]:
    """
    Fetch videos that are due for publishing.
    
    Returns:
        List[Dict[str, Any]]: List of video dictionaries
    """
    try:
        # Get current time in UTC
        now = datetime.now(timezone.utc).isoformat()
        
        # Query for videos that are:
        # 1. Not yet published
        # 2. Scheduled time is in the past
        response = supabase.table("video_schedule") \
            .select("*") \
            .eq("published", False) \
            .lte("scheduled_at", now) \
            .execute()
            
        videos = response.data
        logger.info(f"Found {len(videos)} videos due for publishing")
        
        return videos
        
    except Exception as e:
        logger.error(f"Error fetching due videos: {str(e)}")
        return []
