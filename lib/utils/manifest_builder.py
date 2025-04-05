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
    transcript_id: str,
    platform: str,
    publish_url: str,
    scheduled_at: str,
    published_at: str,
    status: str = "✅ Success",
    additional_info: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate a markdown-formatted publishing manifest.
    
    Args:
        transcript_id: ID of the transcript/video
        platform: Publishing platform (youtube, facebook, instagram, website)
        publish_url: URL where the content was published
        scheduled_at: When the publish was scheduled (ISO format)
        published_at: When the publish completed (ISO format)
        status: Publishing status (default: "✅ Success")
        additional_info: Optional dictionary of additional information to include
        
    Returns:
        str: Formatted markdown manifest
        
    Example:
        >>> manifest = generate_publish_manifest(
        ...     "vid123",
        ...     "youtube",
        ...     "https://youtu.be/abc123",
        ...     "2025-04-04T18:00:00",
        ...     "2025-04-04T18:01:23",
        ...     additional_info={"views": 0, "likes": 0}
        ... )
    """
    platform_emoji = get_platform_emoji(platform)
    formatted_scheduled = format_datetime(scheduled_at)
    formatted_published = format_datetime(published_at)
    
    manifest = f"""# Publishing Summary {platform_emoji}

**Transcript ID**: {transcript_id}  
**Platform**: {platform.title()}  
**Scheduled At**: {formatted_scheduled}  
**Published At**: {formatted_published}  
**URL**: {publish_url}  
**Status**: {status}"""

    # Add any additional information
    if additional_info:
        manifest += "\n\n## Additional Information\n"
        for key, value in additional_info.items():
            manifest += f"\n**{key.title()}**: {value}"
            
    # Add platform-specific notes
    if platform.lower() == 'website':
        manifest += "\n\n## Embed Code\n```html\n"
        manifest += f'<video controls width="640" height="360">\n'
        manifest += f'    <source src="{publish_url}" type="video/mp4">\n'
        manifest += f'    Your browser does not support the video tag.\n'
        manifest += f'</video>\n```'
    
    return manifest
