#!/usr/bin/env python3
"""
Video Publisher Job Script
Checks for and processes videos that are scheduled for publishing.
"""

import sys
import os
import logging
from datetime import datetime
from pathlib import Path
from lib.supabase.fetch_due_videos import fetch_due_videos
from lib.platforms.youtube_client import upload_to_youtube
from lib.platforms.meta_client import upload_to_meta
from lib.supabase.video_storage import get_video_file, cleanup_video_file
from lib.supabase.supabase_client import supabase
from lib.supabase.supabase_utils import get_public_video_url, parse_storage_path, get_video_embed_code
from lib.utils.manifest_builder import generate_publish_manifest
from lib.supabase.upload_utils import upload_file, get_or_create_bucket
from typing import Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('publisher.log')
    ]
)
logger = logging.getLogger(__name__)

# Create manifests directory if it doesn't exist
MANIFESTS_DIR = Path("manifests")
MANIFESTS_DIR.mkdir(exist_ok=True)

# Ensure documents bucket exists
get_or_create_bucket("documents")

def save_and_upload_manifest(
    video: dict,
    manifest_content: str,
    status: str = "success"
) -> Tuple[str, Optional[str]]:
    """
    Save manifest locally and upload to Supabase.
    
    Args:
        video: Video metadata dictionary
        manifest_content: Manifest content to save
        status: Status tag for the filename (success/error)
        
    Returns:
        tuple: (local_path, remote_url)
    """
    # Save locally first
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    local_path = MANIFESTS_DIR / f"manifest_{video['video_id']}_{timestamp}_{status}.md"
    
    with open(local_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
        
    logger.info(f"Manifest created and saved: {local_path}")
    
    # Upload to Supabase
    try:
        remote_path = f"{video['user_id']}/{video['transcript_id']}/manifest_{video['video_id']}.md"
        remote_url = upload_file(
            local_path=str(local_path),
            bucket="documents",
            remote_path=remote_path,
            file_type="manifest",
            make_public=True
        )
        
        if remote_url:
            logger.info(f"Manifest uploaded to: {remote_url}")
            
        return str(local_path), remote_url
        
    except Exception as e:
        logger.error(f"Failed to upload manifest: {str(e)}")
        return str(local_path), None

def update_video_status(
    video_id: str,
    success: bool,
    video_url: str = None,
    error: str = None,
    manifest: str = None,
    manifest_url: str = None,
    user_id: str = None,
    transcript_id: str = None
) -> None:
    """
    Update the video_schedule record with the publishing result.
    
    Args:
        video_id: ID of the video
        success: Whether the publish was successful
        video_url: URL where the video was published
        error: Error message if publish failed
        manifest: Manifest content
        manifest_url: Public URL of the manifest
        user_id: User ID for manifest path
        transcript_id: Transcript ID for manifest path
    """
    try:
        data = {
            "published": success,
            "publish_error": error
        }
        
        if video_url:
            data["publish_url"] = video_url
            
        if manifest:
            data["publish_manifest"] = manifest
            
        if manifest_url:
            data["manifest_url"] = manifest_url
            
        # Add manifest path if we have all required components
        if success and user_id and transcript_id:
            data["manifest_path"] = f"{user_id}/{transcript_id}/manifest_{video_id}.md"
            
        supabase.table("video_schedule") \
            .update(data) \
            .eq("video_id", video_id) \
            .execute()
            
    except Exception as e:
        logger.error(f"Failed to update video status: {str(e)}")

def save_manifest(video_id: str, manifest_content: str, status: str = "success") -> str:
    """
    Save manifest content to a local file.
    
    Args:
        video_id: ID of the video
        manifest_content: Manifest content to save
        status: Status tag for the filename (success/error)
        
    Returns:
        str: Path to the saved manifest file
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    manifest_path = MANIFESTS_DIR / f"manifest_{video_id}_{timestamp}_{status}.md"
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
        
    logger.info(f"Manifest saved to: {manifest_path}")
    return str(manifest_path)

def handle_website_publishing(video_data: dict) -> dict:
    """
    Handle publishing a video for website embedding.
    
    Args:
        video_data: Dictionary containing video metadata
        
    Returns:
        dict: Result containing success status and URL or error
    """
    try:
        logger.info("Preparing to publish video for personal website...")
        
        # Get bucket and path from storage_path
        storage_path = video_data.get('storage_path')
        if not storage_path:
            raise ValueError("No storage path provided for video")
            
        bucket, file_path = parse_storage_path(storage_path)
        if not bucket or not file_path:
            raise ValueError(f"Invalid storage path: {storage_path}")
        
        # Make the file public (if needed)
        supabase.storage \
            .from_(bucket) \
            .update(file_path, {"public": True})
            
        # Generate the public URL
        public_url = get_public_video_url(bucket, file_path)
        
        # Generate embed code
        embed_code = get_video_embed_code(public_url)
        
        logger.info(f"Generated public URL for website embedding")
        logger.info("Use this HTML code to embed the video:")
        logger.info(f"\n{embed_code}")
        
        return {
            'success': True,
            'platform_url': public_url,
            'embed_code': embed_code
        }
        
    except Exception as e:
        logger.error(f"Website publishing failed: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

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
            logger.info(
                f"Processing: '{video['title']}' "
                f"[{video['video_type']}] "
                f"to {video['platform']} "
                f"at {video['scheduled_at']}"
            )
            
            try:
                # Get video file from Supabase
                file_path = get_video_file(video['video_id'])
                if not file_path:
                    raise Exception("Failed to retrieve video file")
                
                # Add file path to video data
                video['file_path'] = file_path
                
                # Handle platform-specific uploads
                result = None
                
                if video['platform'] == 'youtube':
                    result = upload_to_youtube(video)
                elif video['platform'] in ['facebook', 'instagram']:
                    result = upload_to_meta(video['platform'], video)
                elif video['platform'] == 'website':
                    result = handle_website_publishing(video)
                else:
                    logger.error(f"Unsupported platform: {video['platform']}")
                    continue
                
                if result and result['success']:
                    published_at = datetime.utcnow().isoformat()
                    manifest_content = generate_publish_manifest(
                        transcript_id=video["transcript_id"],
                        platform=video["platform"],
                        publish_url=result["platform_url"],
                        scheduled_at=video["scheduled_at"],
                        published_at=published_at,
                        additional_info={
                            "title": video["title"],
                            "video_type": video["video_type"]
                        }
                    )
                    
                    # Save and upload manifest
                    local_path, remote_url = save_and_upload_manifest(video, manifest_content)
                    
                    logger.info(f"Successfully uploaded to {video['platform']}: {result['platform_url']}")
                    logger.info("\nPublishing Manifest:")
                    logger.info(manifest_content)
                    
                    update_video_status(
                        video['video_id'],
                        True,
                        result['platform_url'],
                        manifest=manifest_content,
                        manifest_url=remote_url,
                        user_id=video.get('user_id'),
                        transcript_id=video.get('transcript_id')
                    )
                else:
                    error = result['error'] if result else "Unknown error"
                    logger.error(f"Failed to upload: {error}")
                    
                    # Generate error manifest
                    error_manifest = generate_publish_manifest(
                        transcript_id=video["transcript_id"],
                        platform=video["platform"],
                        publish_url="N/A",
                        scheduled_at=video["scheduled_at"],
                        published_at=datetime.utcnow().isoformat(),
                        status=f" Error: {error}"
                    )
                    
                    # Save and upload error manifest
                    local_path, remote_url = save_and_upload_manifest(video, error_manifest, "error")
                    
                    update_video_status(
                        video['video_id'],
                        False,
                        error=error,
                        manifest=error_manifest,
                        manifest_url=remote_url,
                        user_id=video.get('user_id'),
                        transcript_id=video.get('transcript_id')
                    )
                    
            except Exception as e:
                logger.error(f"Error processing video: {str(e)}")
                
                # Generate error manifest
                error_manifest = generate_publish_manifest(
                    transcript_id=video["transcript_id"],
                    platform=video["platform"],
                    publish_url="N/A",
                    scheduled_at=video["scheduled_at"],
                    published_at=datetime.utcnow().isoformat(),
                    status=f" Error: {str(e)}"
                )
                
                # Save and upload error manifest
                local_path, remote_url = save_and_upload_manifest(video, error_manifest, "error")
                
                update_video_status(
                    video['video_id'],
                    False,
                    error=str(e),
                    manifest=error_manifest,
                    manifest_url=remote_url,
                    user_id=video.get('user_id'),
                    transcript_id=video.get('transcript_id')
                )
                
            finally:
                # Clean up temporary file
                if 'file_path' in video:
                    cleanup_video_file(video['file_path'])
            
        logger.info("Video publisher job completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error in video publisher job: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_video_publisher()
    sys.exit(0 if success else 1)
