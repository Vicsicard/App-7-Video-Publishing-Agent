"""
Supabase storage utilities for video file handling.
"""

import os
import tempfile
import requests
from typing import Dict, Any, Optional
from .supabase_client import supabase

def get_video_file(video_id: str) -> Optional[str]:
    """
    Get a video file from Supabase storage using a signed URL.
    Downloads to a temporary file and returns the path.
    
    Args:
        video_id: UUID of the video in transcript_files
        
    Returns:
        str: Path to temporary file containing the video,
             or None if video cannot be retrieved
    """
    try:
        # Get video details from transcript_files
        result = supabase.table("transcript_files") \
            .select("storage_path") \
            .eq("id", video_id) \
            .execute()
            
        if not result.data:
            raise Exception(f"No video found with ID: {video_id}")
            
        storage_path = result.data[0]["storage_path"]
        
        # Get signed URL for the video
        signed_url = supabase.storage \
            .from_("videos") \
            .create_signed_url(storage_path, 3600)  # 1 hour expiry
            
        if not signed_url:
            raise Exception("Failed to create signed URL")
            
        # Download to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        response = requests.get(signed_url, stream=True)
        response.raise_for_status()
        
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                temp_file.write(chunk)
                
        temp_file.close()
        return temp_file.name
        
    except Exception as e:
        raise Exception(f"Failed to get video file: {str(e)}")
        
def cleanup_video_file(file_path: str) -> None:
    """
    Clean up a temporary video file.
    
    Args:
        file_path: Path to the temporary file to delete
    """
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        # Log but don't raise - this is cleanup
        print(f"Warning: Failed to cleanup temp file {file_path}: {str(e)}")
