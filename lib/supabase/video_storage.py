"""
Functions for managing video files in Supabase storage.
"""

import os
import tempfile
import logging
from pathlib import Path
from typing import Optional
import httpx

from .client import supabase, get_supabase_headers

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_video_file(video_id: str) -> Optional[str]:
    """
    Get a video file from Supabase storage and save it to a temporary file.
    
    Args:
        video_id: ID of the video in the transcript_files table
        
    Returns:
        Optional[str]: Path to the temporary file containing the video, or None if retrieval failed
    """
    try:
        # Get file info from transcript_files table
        response = supabase.table("transcript_files") \
            .select("file_path,bucket") \
            .eq("id", video_id) \
            .execute()
            
        if not response.data:
            raise Exception(f"No transcript found with ID: {video_id}")
            
        transcript = response.data[0]
        
        # Get signed URL for file
        url = f"{supabase.url}/storage/v1/object/{transcript['bucket']}/{transcript['file_path']}"
        response = httpx.get(url, headers=get_supabase_headers(include_representation=False))
        response.raise_for_status()
        
        # Save to temporary file
        suffix = Path(transcript['file_path']).suffix
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(response.content)
            return f.name
            
    except Exception as e:
        logger.error(f"Failed to get video file: {str(e)}")
        return None

def cleanup_video_file(file_path: str):
    """
    Clean up a temporary video file.
    
    Args:
        file_path: Path to the temporary file to delete
    """
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        logger.error(f"Failed to clean up video file: {str(e)}")
