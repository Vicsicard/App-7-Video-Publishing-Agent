"""
Video publishing manifest utilities.
"""

import os
import json
import logging
from typing import Dict, Any, Tuple, Optional
from datetime import datetime, timezone
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_publish_manifest(
    video: Dict[str, Any],
    publish_url: str,
    embed_code: Optional[str] = None,
    status: str = "success"
) -> str:
    """
    Generate a JSON manifest for a published video.
    
    Args:
        video: Dictionary containing video information
        publish_url: URL where the video was published
        embed_code: Optional HTML code to embed the video
        status: Publishing status, defaults to "success"
        
    Returns:
        str: JSON string containing the manifest
    """
    try:
        manifest = {
            "video_id": video.get("video_id") or video.get("transcript_id"),
            "platform": video["platform"],
            "status": status,
            "publish_url": publish_url,
            "published_at": datetime.now(timezone.utc).isoformat(),
            "storage_path": video.get("storage_path", "")
        }
        
        if embed_code:
            manifest["embed_code"] = embed_code
            
        return json.dumps(manifest, indent=2)
        
    except Exception as e:
        logger.error(f"Error generating manifest: {str(e)}")
        return json.dumps({
            "status": "error",
            "error": str(e)
        }, indent=2)

def save_and_upload_manifest(
    video: Dict[str, Any],
    manifest_content: str,
    status: str = "success"
) -> Tuple[str, Optional[str]]:
    """
    Save a manifest file locally and optionally upload to storage.
    
    Args:
        video: Dictionary containing video information
        manifest_content: JSON string containing manifest content
        status: Publishing status, defaults to "success"
        
    Returns:
        Tuple[str, Optional[str]]: Local manifest path and optional URL
    """
    try:
        # Create manifests directory if it doesn't exist
        manifest_dir = Path("manifests")
        manifest_dir.mkdir(exist_ok=True)
        
        # Generate manifest filename
        video_id = video.get("video_id") or video.get("transcript_id")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"{video_id}_{timestamp}_{status}.json"
        
        # Save manifest locally
        manifest_path = manifest_dir / filename
        with open(manifest_path, "w") as f:
            f.write(manifest_content)
            
        logger.info(f"Saved manifest to {manifest_path}")
        
        # For now, just return the local path
        # In the future, we can add storage upload functionality
        return str(manifest_path), None
        
    except Exception as e:
        logger.error(f"Error saving manifest: {str(e)}")
        return "", None
