"""
Utility functions for storing publishing manifests.
"""

import os
from datetime import datetime
from typing import Dict, Any, Tuple

def save_and_upload_manifest(
    video: Dict[str, Any],
    manifest_content: str,
    status: str = "success"
) -> Tuple[str, str]:
    """
    Save a manifest file locally and upload to storage.
    
    Args:
        video: Video metadata dictionary
        manifest_content: Manifest content to save
        status: Status to include in filename
        
    Returns:
        Tuple[str, str]: (Local manifest path, Manifest URL)
    """
    try:
        # Create manifests directory if it doesn't exist
        manifests_dir = os.path.join(os.path.dirname(__file__), "..", "..", "manifests")
        os.makedirs(manifests_dir, exist_ok=True)
        
        # Generate manifest filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"manifest_{video['id']}_{timestamp}_{status}.md"
        manifest_path = os.path.join(manifests_dir, filename)
        
        # Save manifest locally
        with open(manifest_path, "w") as f:
            f.write(manifest_content)
            
        # For now, just return local path
        # TODO: Upload to storage later
        manifest_url = f"file://{manifest_path}"
        
        return manifest_path, manifest_url
        
    except Exception as e:
        raise Exception(f"Failed to save manifest: {str(e)}")
