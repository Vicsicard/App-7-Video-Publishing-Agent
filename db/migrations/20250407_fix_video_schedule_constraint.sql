-- Drop existing unique constraint
ALTER TABLE video_schedule DROP CONSTRAINT IF EXISTS video_schedule_video_id_key;

-- Add composite unique constraint for video_id and user_id
ALTER TABLE video_schedule ADD CONSTRAINT video_schedule_video_id_user_id_key UNIQUE (video_id, user_id);
