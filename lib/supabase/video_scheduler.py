"""
Module for scheduling videos for publishing.
"""

from typing import Dict, Any
from datetime import datetime
from .supabase_client import supabase

def schedule_video(
    video_id: str,
    video_type: str,
    platform: str,
    title: str,
    description: str,
    tags: list,
    scheduled_at: datetime
) -> Dict[str, Any]:
    """
    Schedule a video for publishing.

    Args:
        video_id (str): UUID of the video from transcript_files
        video_type (str): Type of video ('shortform' or 'longform')
        platform (str): Target platform ('youtube', 'instagram', 'facebook', 'website')
        title (str): Title of the video
        description (str): Description of the video
        tags (list): List of tags for the video
        scheduled_at (datetime): When to publish the video

    Returns:
        Dict[str, Any]: The created schedule entry

    Raises:
        ValueError: If video_type or platform are invalid
        Exception: If the database operation fails
    """
    # Validate video type
    valid_video_types = ['shortform', 'longform']
    if video_type not in valid_video_types:
        raise ValueError(f"Invalid video_type. Must be one of: {valid_video_types}")

    # Validate platform
    valid_platforms = ['youtube', 'instagram', 'facebook', 'website']
    if platform not in valid_platforms:
        raise ValueError(f"Invalid platform. Must be one of: {valid_platforms}")

    try:
        # Create schedule entry
        response = supabase.table("video_schedule").insert({
            "video_id": video_id,
            "video_type": video_type,
            "platform": platform,
            "title": title,
            "description": description,
            "tags": tags,
            "scheduled_at": scheduled_at.isoformat()
        }).execute()

        if not response.data:
            raise Exception("No data returned from insert operation")
        
        return response.data[0]
    
    except Exception as e:
        raise Exception(f"Failed to schedule video: {str(e)}")
