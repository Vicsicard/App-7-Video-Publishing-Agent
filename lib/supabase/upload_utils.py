"""
Utilities for uploading files to Supabase storage.
"""

import os
from pathlib import Path
from typing import Optional, List
from .supabase_client import supabase

def get_or_create_bucket(bucket: str) -> None:
    """
    Get a bucket if it exists, create if it doesn't.
    Handles RLS policies gracefully.
    
    Args:
        bucket: Bucket name to check/create
    """
    try:
        # Try to get bucket info first
        buckets = supabase.storage.list_buckets()
        bucket_exists = any(b['name'] == bucket for b in buckets)
        
        if not bucket_exists:
            # If bucket doesn't exist, try to create it
            try:
                supabase.storage.create_bucket(
                    bucket,
                    options={'public': True}  # Make bucket public by default
                )
            except Exception as create_error:
                # If creation fails due to permissions, try to use existing bucket
                if 'Unauthorized' in str(create_error):
                    # Just verify we can access the bucket
                    supabase.storage.from_(bucket).list()
                else:
                    raise create_error
                    
    except Exception as e:
        if 'Unauthorized' in str(e):
            # If we can't list buckets due to permissions, try to use the bucket directly
            try:
                # Verify we can access the bucket
                supabase.storage.from_(bucket).list()
            except Exception as access_error:
                raise Exception(f"Cannot access bucket '{bucket}': {str(access_error)}")
        else:
            raise Exception(f"Failed to ensure bucket exists: {str(e)}")

def upload_file(
    local_path: str,
    bucket: str,
    remote_path: str,
    file_type: str,
    make_public: bool = False
) -> Optional[str]:
    """
    Upload a file to Supabase storage.
    
    Args:
        local_path: Path to local file
        bucket: Storage bucket name
        remote_path: Path within bucket
        file_type: Type of file (e.g., 'video', 'manifest', 'thumbnail')
        make_public: Whether to make the file publicly accessible
        
    Returns:
        str: Public URL if make_public=True, None otherwise
        
    Raises:
        Exception: If upload fails
    """
    try:
        # Ensure local file exists
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")
            
        # Ensure remote path has no leading slash
        remote_path = remote_path.lstrip('/')
        
        # Read file content
        with open(local_path, 'rb') as f:
            file_content = f.read()
            
        # Get content type
        content_type = "text/markdown" if file_type == "manifest" else "application/octet-stream"
            
        # Upload to Supabase
        try:
            result = supabase.storage \
                .from_(bucket) \
                .upload(
                    path=remote_path,
                    file=file_content,
                    file_options={"content-type": content_type}
                )
                
        except Exception as upload_error:
            # If file exists, try to update it
            if "already exists" in str(upload_error):
                result = supabase.storage \
                    .from_(bucket) \
                    .update(
                        path=remote_path,
                        file=file_content,
                        file_options={"content-type": content_type}
                    )
            else:
                raise upload_error
            
        # Make public if requested
        if make_public:
            try:
                supabase.storage \
                    .from_(bucket) \
                    .update(remote_path, {"public": True})
            except Exception as public_error:
                # If we can't make it public, but it's in a public bucket, it might still work
                pass
                
            # Generate public URL
            return f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/{bucket}/{remote_path}"
            
        return None
        
    except Exception as e:
        raise Exception(f"Failed to upload {file_type}: {str(e)}")

def list_bucket_contents(bucket: str, prefix: str = "") -> List[dict]:
    """
    List contents of a bucket with optional prefix filter.
    
    Args:
        bucket: Bucket name to list
        prefix: Optional path prefix to filter by
        
    Returns:
        list: List of file information dictionaries
    """
    try:
        return supabase.storage.from_(bucket).list(prefix)
    except Exception as e:
        raise Exception(f"Failed to list bucket contents: {str(e)}")

def delete_file(bucket: str, path: str) -> None:
    """
    Delete a file from storage.
    
    Args:
        bucket: Bucket name
        path: Path to file within bucket
    """
    try:
        supabase.storage.from_(bucket).remove([path])
    except Exception as e:
        raise Exception(f"Failed to delete file: {str(e)}")
