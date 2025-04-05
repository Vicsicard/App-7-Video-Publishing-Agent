"""
Meta Graph API client for publishing to Facebook and Instagram.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
FB_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
IG_USER_ID = os.getenv("INSTAGRAM_USER_ID")

def upload_facebook_video(video_path, title, description):
    """
    Upload a video to Facebook.
    
    Args:
        video_path: Path to the video file
        title: Video title
        description: Video description
        
    Returns:
        str: URL of the uploaded video
        
    Raises:
        Exception: If upload fails
    """
    with open(video_path, "rb") as f:
        files = {"file": f}
        params = {
            "title": title,
            "description": description,
            "access_token": META_ACCESS_TOKEN
        }
        response = requests.post(
            f"https://graph-video.facebook.com/v18.0/{FB_PAGE_ID}/videos",
            files=files,
            data=params
        )
    result = response.json()
    if "id" not in result:
        raise Exception(result.get("error", "Unknown error"))
    return f"https://www.facebook.com/{FB_PAGE_ID}/videos/{result['id']}"

def upload_instagram_reel(video_path, caption):
    """
    Upload a video as an Instagram Reel.
    
    Args:
        video_path: Path to the video file
        caption: Video caption (combines title and description)
        
    Returns:
        str: URL of the uploaded reel
        
    Raises:
        Exception: If upload or publish fails
    """
    # Step 1: Upload media
    files = {"video": open(video_path, "rb")}
    params = {
        "media_type": "VIDEO",
        "caption": caption,
        "access_token": META_ACCESS_TOKEN
    }
    response = requests.post(
        f"https://graph-video.facebook.com/v18.0/{IG_USER_ID}/media",
        files=files,
        data=params
    )
    result = response.json()
    if "id" not in result:
        raise Exception(result.get("error", "Upload step failed"))
    container_id = result["id"]

    # Step 2: Publish media
    publish_response = requests.post(
        f"https://graph.facebook.com/v18.0/{IG_USER_ID}/media_publish",
        data={"creation_id": container_id, "access_token": META_ACCESS_TOKEN}
    )
    publish_result = publish_response.json()
    if "id" not in publish_result:
        raise Exception(publish_result.get("error", "Publish step failed"))

    return f"https://www.instagram.com/reel/{publish_result['id']}"

def upload_to_meta(platform: str, video_data: dict) -> dict:
    """
    Upload a video to either Facebook or Instagram.
    
    Args:
        platform: Either 'facebook' or 'instagram'
        video_data: Dictionary containing video metadata and file path
        
    Returns:
        dict: Upload result with success status and video URL or error
    """
    try:
        if platform == 'facebook':
            video_url = upload_facebook_video(
                video_data['file_path'],
                video_data['title'],
                video_data['description']
            )
        elif platform == 'instagram':
            caption = f"{video_data['title']}\n\n{video_data['description']}"
            video_url = upload_instagram_reel(
                video_data['file_path'],
                caption
            )
        else:
            raise ValueError(f"Unsupported platform: {platform}")
            
        return {
            'success': True,
            'platform_url': video_url
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
