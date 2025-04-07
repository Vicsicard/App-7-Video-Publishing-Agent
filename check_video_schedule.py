#!/usr/bin/env python3
"""
Script to check the video_schedule table directly.
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timezone

sys.path.append(str(Path(__file__).parent))
from lib.supabase.supabase_client import supabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_video_schedule():
    """Check the video_schedule table directly."""
    try:
        # Get all videos from the table
        response = supabase.table("video_schedule").select("*").execute()
        
        logger.info(f"Total videos in table: {len(response.data)}")
        logger.info(f"All videos: {response.data}")
        
        # Get unpublished videos
        now = datetime.now(timezone.utc).isoformat()
        response = supabase.table("video_schedule") \
            .select("*") \
            .eq("published", False) \
            .lte("scheduled_at", now) \
            .execute()
            
        logger.info(f"Unpublished videos due before {now}: {len(response.data)}")
        logger.info(f"Due videos: {response.data}")
        
        return True
    except Exception as e:
        logger.error(f"Error checking video_schedule: {str(e)}")
        return False

if __name__ == "__main__":
    check_video_schedule()
