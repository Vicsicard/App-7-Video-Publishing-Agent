-- Drop the existing RLS policy
DROP POLICY IF EXISTS "Users can manage their own video schedules" ON video_schedule;

-- Create a new policy that allows the service role to access all rows
CREATE POLICY "Service role can access all videos"
    ON video_schedule FOR ALL
    USING (
        (auth.jwt() ->> 'role'::text) = 'service_role'::text
        OR
        auth.uid() = (
            SELECT user_id 
            FROM transcript_files
            WHERE transcript_files.id = video_schedule.video_id
        )
    );
