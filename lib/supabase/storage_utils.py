"""
Storage utilities for uploading files to Supabase.
"""

import os
import httpx
from typing import Optional

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")

def get_or_create_bucket(bucket_name: str) -> None:
    """
    Get or create a storage bucket.
    
    Args:
        bucket_name: Name of the bucket to get or create
    """
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    
    # Check if bucket exists
    url = f"{SUPABASE_URL}/storage/v1/bucket/{bucket_name}"
    response = httpx.get(url, headers=headers)
    
    if response.status_code == 404:
        # Create bucket
        url = f"{SUPABASE_URL}/storage/v1/bucket"
        data = {
            "name": bucket_name,
            "public": True,  # Make bucket public
            "file_size_limit": 52428800  # 50MB limit
        }
        response = httpx.post(url, headers=headers, json=data)
        response.raise_for_status()

def upload_test_video(user_id: str, file_path: str, file_name: str) -> str:
    """
    Upload a video file to Supabase storage.
    
    Args:
        user_id: User ID to use in storage path
        file_path: Path to local video file
        file_name: Name to use for uploaded file
        
    Returns:
        str: Storage path where file was uploaded
    """
    # Ensure videos bucket exists
    get_or_create_bucket("videos")
    
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    }
    
    storage_path = f"{user_id}/{file_name}"
    url = f"{SUPABASE_URL}/storage/v1/object/videos/{storage_path}"
    
    with open(file_path, "rb") as f:
        files = {"file": (file_name, f, "video/mp4")}
        response = httpx.post(url, headers=headers, files=files)
        response.raise_for_status()
    
    return storage_path
