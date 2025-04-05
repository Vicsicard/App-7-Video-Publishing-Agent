"""
Test script to schedule a video for publishing.
"""
from datetime import datetime, timedelta
from lib.supabase.video_scheduler import schedule_video

def create_test_schedule():
    # Schedule a video for immediate publishing
    now = datetime.utcnow()
    try:
        result = schedule_video(
            video_id="00000000-0000-0000-0000-000000000000",  # This should be a valid video_id from transcript_files
            video_type="shortform",
            platform="youtube",
            title="Test Video Upload",
            description="This is a test video for the publishing agent",
            tags=["test", "demo"],
            scheduled_at=now - timedelta(minutes=1)  # Schedule it for 1 minute ago
        )
        print(f"Successfully scheduled video: {result}")
        return True
    except Exception as e:
        print(f"Error scheduling video: {str(e)}")
        return False

if __name__ == "__main__":
    create_test_schedule()
