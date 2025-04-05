"""
YouTube API client for video publishing.
Uses secure credential-based authentication with refresh token.
"""

import os
from typing import Dict, Any
import logging
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

def get_youtube_credentials() -> Credentials:
    """
    Create YouTube API credentials using environment variables.
    Uses refresh token for secure, headless authentication.
    """
    return Credentials(
        None,  # No access token needed, will be refreshed
        refresh_token=os.getenv('YOUTUBE_REFRESH_TOKEN'),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv('YOUTUBE_CLIENT_ID'),
        client_secret=os.getenv('YOUTUBE_CLIENT_SECRET')
    )

def upload_to_youtube(video_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Upload a video to YouTube using secure credential-based authentication.
    
    Args:
        video_data (Dict[str, Any]): Video metadata including:
            - title: Video title
            - description: Video description
            - tags: List of tags
            - file_path: Path to video file
            - scheduled_at: Optional timestamp for scheduled publishing
            
    Returns:
        Dict[str, Any]: Upload result with:
            - success: bool
            - video_id: str (if successful)
            - error: str (if failed)
    """
    try:
        # Get credentials and build service
        credentials = get_youtube_credentials()
        youtube = build('youtube', 'v3', credentials=credentials)
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': video_data['title'],
                'description': video_data['description'],
                'tags': video_data.get('tags', []),
                'categoryId': '22'  # People & Blogs category
            },
            'status': {
                'privacyStatus': 'private',  # Start as private
                'selfDeclaredMadeForKids': False
            }
        }
        
        # If scheduled_at is provided, set publishAt
        if 'scheduled_at' in video_data:
            scheduled_time = datetime.fromisoformat(video_data['scheduled_at'])
            body['status']['publishAt'] = scheduled_time.isoformat() + 'Z'
        
        # Create MediaFileUpload object
        media = MediaFileUpload(
            video_data['file_path'],
            mimetype='video/*',
            resumable=True
        )
        
        # Execute the upload
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = request.execute()
        
        return {
            'success': True,
            'video_id': response['id']
        }
        
    except Exception as e:
        logger.error(f"YouTube upload failed: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
