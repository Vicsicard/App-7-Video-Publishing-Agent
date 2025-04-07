#!/usr/bin/env python3
"""
Script to check transcript files table.
"""

import os
import sys
import httpx
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

# Get Supabase config from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")

def check_transcript_files():
    """Check transcript files table."""
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Get all transcript files
    url = f"{SUPABASE_URL}/rest/v1/transcript_files"
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    
    print("Transcript files:")
    for file in response.json():
        print(f"ID: {file['id']}")
        print(f"User ID: {file['user_id']}")
        print(f"File path: {file['file_path']}")
        print(f"Bucket: {file['bucket']}")
        print("---")
        
    # Get all video schedules
    url = f"{SUPABASE_URL}/rest/v1/video_schedule"
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    
    print("\nVideo schedules:")
    for video in response.json():
        print(f"ID: {video['id']}")
        print(f"Video ID: {video['video_id']}")
        print(f"Platform: {video['platform']}")
        print(f"Scheduled at: {video['scheduled_at']}")
        print(f"Published: {video['published']}")
        print("---")

if __name__ == "__main__":
    check_transcript_files()
