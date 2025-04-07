import os
import httpx
from datetime import datetime, timezone
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Get Supabase config
SUPABASE_URL = "https://aqicztygjpmunfljjuto.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxaWN6dHlnanBtdW5mbGpqdXRvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MzcwNTU4MiwiZXhwIjoyMDU5MjgxNTgyfQ.lIfnbWUDm8yDz1g_gQJNi56rCiGRAunY48rgVAwLID4"

# Set up headers
headers = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Create test data
test_data = {
    "video_id": str(uuid.uuid4()),
    "user_id": str(uuid.uuid4()),
    "platform": "youtube",
    "scheduled_at": datetime.now(timezone.utc).isoformat(),
    "title": "Test Video",
    "description": "Test description",
    "tags": []
}

# Make request
url = f"{SUPABASE_URL}/rest/v1/video_schedule"
response = httpx.post(url, headers=headers, json=test_data)

# Log results
print(f"Status code: {response.status_code}")
print(f"Response headers: {dict(response.headers)}")
print(f"Response body: {response.text}")
