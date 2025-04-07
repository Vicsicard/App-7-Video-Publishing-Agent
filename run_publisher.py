#!/usr/bin/env python3
"""
Video Publisher Job Script
Checks for and processes videos that are scheduled for publishing.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any
sys.path.append(str(Path(__file__).parent))

from lib.supabase.fetch_due_videos import fetch_due_videos
from lib.supabase.video_storage import get_video_file
from lib.utils import generate_publish_manifest, save_and_upload_manifest
from lib.platforms import handle_website_publishing
from lib.supabase.client import supabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_video_file(file_path: str) -> None:
    """Clean up a temporary video file."""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        logger.error(f"Error cleaning up video file: {str(e)}")

def update_video_status(
    schedule_id: str,
    video_id: str,
    success: bool,
    platform_url: str = None,
    manifest: str = None,
    manifest_url: str = None,
    error: str = None,
    user_id: str = None
) -> None:
    """Update video publishing status."""
    try:
        data = {
            "published": success,
            "publish_url": platform_url,
            "publish_manifest": manifest,
            "manifest_url": manifest_url,
            "publish_error": error
        }
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        # Use ID to target the row
        query = supabase.table("video_schedule").update(data).eq("id", schedule_id)
        response = query.execute()
        
        # Log response for debugging
        logger.info(f"Update response: {response.data}")
        
        if not response.data:
            logger.error(f"Failed to update video status: {video_id}")
            return
            
        updated = response.data[0]
        if updated.get('published') != success:  
            logger.error(f"Failed to update published status for video: {video_id}")
            logger.error(f"Updated data: {updated}")
            return
            
        logger.info(f"Updated video status: {video_id} (success={success})")
        
    except Exception as e:
        logger.error(f"Error updating video status: {str(e)}")
        logger.error(f"Error details: {str(e.__dict__)}")

def run_video_publisher():
    """
    Main function to check and process videos scheduled for publishing.
    Fetches due videos and processes them through appropriate platforms.
    """
    logger.info("Starting video publisher job")
    
    try:
        # Fetch videos due for publishing
        due_videos = fetch_due_videos()
        logger.info(f"Found {len(due_videos)} video(s) scheduled for publishing")
        
        # Process each due video
        for video in due_videos:
            video_id = video['video_id']
            schedule_id = video['id']  # Get schedule ID
            platform = video['platform']
            scheduled_at = video['scheduled_at']
            user_id = video.get('user_id')
            
            logger.info(
                f"Processing video {video_id} "
                f"to {platform} "
                f"at {scheduled_at}"
            )
            
            try:
                # Get transcript file info for storage path
                response = supabase.table("transcript_files") \
                    .select("file_path,bucket") \
                    .eq("id", video['video_id']) \
                    .execute()
                    
                if not response.data:
                    update_video_status(
                        schedule_id=schedule_id,
                        video_id=video_id,
                        success=False,
                        error="Video data not found",
                        user_id=user_id
                    )
                    continue
                    
                transcript = response.data[0]
                video['storage_path'] = f"{transcript['bucket']}/{transcript['file_path']}"
                
                # Get video file from Supabase
                file_path = get_video_file(video['video_id'])
                if not file_path:
                    update_video_status(
                        schedule_id=schedule_id,
                        video_id=video_id,
                        success=False,
                        error="Video file not found",
                        user_id=user_id
                    )
                    continue
                
                # Add file path to video data
                video['file_path'] = file_path
                
                # Handle platform-specific uploads
                result = None
                if video['platform'] == 'youtube':
                    result = upload_to_youtube(video)
                elif video['platform'] == 'meta':
                    result = upload_to_meta(video)
                elif video['platform'] == 'website':
                    result = handle_website_publishing(video)
                else:
                    update_video_status(
                        schedule_id=schedule_id,
                        video_id=video_id,
                        success=False,
                        error=f"Unsupported platform: {video['platform']}",
                        user_id=user_id
                    )
                    continue
                    
                if not result['success']:
                    update_video_status(
                        schedule_id=schedule_id,
                        video_id=video_id,
                        success=False,
                        error=result.get('error', 'Unknown error'),
                        user_id=user_id
                    )
                    continue
                    
                # Generate publish manifest
                manifest_content = generate_publish_manifest(
                    video,
                    result['publish_url'],
                    result.get('embed_code')
                )
                
                # Save manifest locally
                manifest_path, manifest_url = save_and_upload_manifest(
                    video,
                    manifest_content
                )
                
                # Update video status
                update_video_status(
                    schedule_id=schedule_id,
                    video_id=video_id,
                    success=True,
                    platform_url=result['publish_url'],
                    manifest=manifest_content,
                    manifest_url=manifest_url,
                    user_id=user_id
                )
                
            except Exception as e:
                logger.error(f"Error processing video: {str(e)}")
                update_video_status(
                    schedule_id=schedule_id,
                    video_id=video_id,
                    success=False,
                    error=str(e),
                    user_id=user_id
                )
                continue
                
            finally:
                # Clean up temporary video file
                if 'file_path' in video:
                    cleanup_video_file(video['file_path'])
                    
        return True
        
    except Exception as e:
        logger.error(f"Publisher job failed: {str(e)}")
        return False

if __name__ == "__main__":
    run_video_publisher()
