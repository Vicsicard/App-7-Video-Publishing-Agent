"""
Utility functions for generating publishing manifests and summaries.
"""

from datetime import datetime
from typing import Optional, Dict, Any

def format_datetime(dt_str: str) -> str:
    """
    Format a datetime string into a human-readable format.
    
    Args:
        dt_str: ISO format datetime string
        
    Returns:
        str: Formatted datetime string
    """
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except (ValueError, TypeError):
        return dt_str

def get_platform_emoji(platform: str) -> str:
    """
    Get an appropriate emoji for the publishing platform.
    
    Args:
        platform: Platform name (youtube, facebook, instagram, website)
        
    Returns:
        str: Platform emoji
    """
    platform_emojis = {
        'youtube': '📺',
        'facebook': '📱',
        'instagram': '📸',
        'website': '🌐',
        'error': '❌'
    }
    return platform_emojis.get(platform.lower(), '📄')

def generate_publish_manifest(
    video: dict,
    publish_url: str,
    embed_code: str = None,
    status: str = "Success"
) -> str:
    """
    Generate a markdown manifest for a published video.
    
    Args:
        video: Video metadata dictionary
        publish_url: URL where video was published
        embed_code: Optional HTML embed code
        status: Status message to include
        
    Returns:
        str: Markdown formatted manifest
    """
    manifest = f"""# Video Publishing Manifest

## Video Details
- Transcript ID: {video['transcript_id']}
- Platform: {video['platform']}
- Scheduled At: {video['scheduled_at']}
- Published At: {datetime.utcnow().isoformat()}

## Publishing Details
- Status: {status}
- Public URL: {publish_url}

## Storage Details
- Storage Path: {video.get('storage_path', 'N/A')}
"""

    if embed_code:
        manifest += f"\n## Embed Code\n```html\n{embed_code}\n```"
        
    return manifest
