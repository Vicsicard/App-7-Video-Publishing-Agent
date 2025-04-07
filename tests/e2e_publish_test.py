#!/usr/bin/env python3
"""
End-to-end test for video publishing workflow.
"""

import os
import sys
import logging
from datetime import datetime, timedelta, timezone
import tempfile
import uuid
import httpx
from pathlib import Path
import time
sys.path.append(str(Path(__file__).parent.parent))

from lib.supabase.storage_utils import upload_test_video

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Supabase config from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")

def authenticate_service():
    """Authenticate with Supabase using service role key."""
    global api_headers
    api_headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def create_test_user():
    """Create a test user in Supabase."""
    try:
        # Set up service role authentication first
        authenticate_service()
        
        # Generate a unique test user ID
        user_id = str(uuid.uuid4())
        email = f"test_{user_id}@example.com"
        
        # Create test user using auth API
        url = f"{SUPABASE_URL}/auth/v1/admin/users"
        user_data = {
            "email": email,
            "password": "test_password123",
            "email_confirm": True,
            "user_metadata": {"role": "authenticated"}
        }
        
        response = httpx.post(url, headers=api_headers, json=user_data)
        response.raise_for_status()
        user_data = response.json()
        user_id = user_data['id']
        
        logger.info(f"Created test user with ID: {user_id}")
        return user_id
        
    except Exception as e:
        logger.error(f"Error creating test user: {str(e)}")
        return None

def create_test_video_entry(user_id: str):
    """Create a test video entry in the database."""
    try:
        # Create a temporary test video file
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            # Write some dummy video data (just enough to be a valid MP4)
            f.write(b'\x00' * 1024)  # 1KB of zeros
            temp_path = f.name

        # Upload the video
        file_name = 'test_video.mp4'
        storage_path = upload_test_video(user_id, temp_path, file_name)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        # First create transcript file entry
        transcript_id = str(uuid.uuid4())  # Pre-generate ID to use in video_schedule
        transcript_data = {
            'id': transcript_id,
            'user_id': user_id,
            'file_path': f"{user_id}/{file_name}",  # Match the storage path format
            'file_name': file_name,
            'file_type': 'video/mp4',
            'bucket': 'videos'
        }
        
        url = f"{SUPABASE_URL}/rest/v1/transcript_files"
        response = httpx.post(url, headers=api_headers, json=transcript_data)
        response.raise_for_status()
        
        # Create video schedule entry
        schedule_data = {
            "video_id": transcript_id,  # Use transcript_id as video_id
            "platform": "website",
            "scheduled_at": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),  # Schedule it for 1 minute ago
            "user_id": user_id  # Add user_id to the schedule
        }
        
        logger.info(f"Creating video schedule with data: {schedule_data}")
        url = f"{SUPABASE_URL}/rest/v1/video_schedule"
        response = httpx.post(url, headers=api_headers, json=schedule_data)
        
        if response.status_code != 201:
            logger.error(f"Failed to create video schedule. Status: {response.status_code}")
            logger.error(f"Response: {response.text}")
            response.raise_for_status()
            
        return transcript_id  # Return transcript_id since it's used as video_id
        
    except Exception as e:
        logger.error(f"Error creating test video entry: {str(e)}")
        return None

def verify_publishing_result(video_id: str) -> bool:
    """
    Verify that a video was published successfully.
    
    Args:
        video_id: ID of the video to verify
        
    Returns:
        bool: True if verification passed, False otherwise
    """
    try:
        # Add delay to ensure update is reflected
        time.sleep(2)
        
        url = f"{SUPABASE_URL}/rest/v1/video_schedule"
        params = {"video_id": f"eq.{video_id}"}  # Query by video_id field
        response = httpx.get(url, headers=api_headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            logger.error(f"No video found with ID {video_id}")
            return False
            
        video = data[0]
        if not video.get('published', False):  # Use get() with default False
            logger.error(f"Video {video_id} was not marked as published")
            logger.error(f"Video data: {video}")  # Log video data for debugging
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Error verifying publishing result: {str(e)}")
        return False

def run_e2e_test():
    """Run the end-to-end publishing test."""
    logger.info("Starting end-to-end publishing test")
    
    # Create test user
    user_id = create_test_user()
    if not user_id:
        return False
        
    # Create test video entry
    video_id = create_test_video_entry(user_id)
    if not video_id:
        return False
        
    # Wait for publisher to process
    attempts = 0
    max_attempts = 6
    while attempts < max_attempts:
        # Run publisher
        from run_publisher import run_video_publisher
        run_video_publisher()
        
        # Check if video was published
        if verify_publishing_result(video_id):
            return True
            
        time.sleep(10)  # Wait 10 seconds between attempts
        attempts += 1
    
    return verify_publishing_result(video_id)

if __name__ == "__main__":
    success = run_e2e_test()
    if not success:
        logger.error("End-to-end test failed verification")
        sys.exit(1)
    sys.exit(0)
