"""
Utility functions for working with Supabase storage.
"""

import os
from typing import Optional
from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")

def get_public_video_url(bucket: str, path: str) -> str:
    """
    Generate a public URL for a video stored in Supabase storage.
    
    Args:
        bucket: Storage bucket name (e.g., 'videos')
        path: Path to the video file within the bucket
        
    Returns:
        str: Public URL for direct video access
        
    Example:
        >>> get_public_video_url('videos', 'user123/video1.mp4')
        'https://your-project.supabase.co/storage/v1/object/public/videos/user123/video1.mp4'
    """
    # URL encode the path to handle special characters
    encoded_path = quote(path)
    return f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{encoded_path}"

def get_video_embed_code(video_url: str, width: int = 640, height: int = 360) -> str:
    """
    Generate HTML embed code for a video URL.
    
    Args:
        video_url: Public URL of the video
        width: Video player width in pixels
        height: Video player height in pixels
        
    Returns:
        str: HTML code for embedding the video
        
    Example:
        >>> get_video_embed_code('https://example.com/video.mp4')
        '<video controls width="640" height="360">
             <source src="https://example.com/video.mp4" type="video/mp4">
             Your browser does not support the video tag.
           </video>'
    """
    return f'''<video controls width="{width}" height="{height}">
    <source src="{video_url}" type="video/mp4">
    Your browser does not support the video tag.
</video>'''

def parse_storage_path(storage_path: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parse a storage path into bucket and file path components.
    
    Args:
        storage_path: Full storage path (e.g., 'videos/user123/video1.mp4')
        
    Returns:
        tuple: (bucket_name, file_path) or (None, None) if invalid
    """
    if not storage_path or '/' not in storage_path:
        return None, None
        
    parts = storage_path.split('/', 1)
    if len(parts) != 2:
        return None, None
        
    return parts[0], parts[1]
