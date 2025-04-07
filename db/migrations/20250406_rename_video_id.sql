-- Rename video_id to transcript_id
ALTER TABLE video_schedule 
    RENAME COLUMN video_id TO transcript_id;

-- Update indexes
DROP INDEX IF EXISTS idx_video_schedule_video_id;
CREATE INDEX IF NOT EXISTS idx_video_schedule_transcript_id 
    ON video_schedule(transcript_id);

-- Update RLS policy
DROP POLICY IF EXISTS "Service role can access all videos" ON video_schedule;
CREATE POLICY "Service role can access all videos"
    ON video_schedule FOR ALL
    USING (
        (auth.jwt() ->> 'role'::text) = 'service_role'::text
        OR
        auth.uid() = (
            SELECT user_id 
            FROM transcript_files
            WHERE transcript_files.id = video_schedule.transcript_id
        )
    );
