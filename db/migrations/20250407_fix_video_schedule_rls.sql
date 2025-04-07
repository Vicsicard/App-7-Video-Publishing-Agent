-- Enable RLS on video_schedule
ALTER TABLE video_schedule ENABLE ROW LEVEL SECURITY;

-- Drop existing service role policy
DROP POLICY IF EXISTS "Service role bypass RLS" ON video_schedule;

-- Create new service role policies with explicit permissions
CREATE POLICY "Service role can read all videos"
ON video_schedule
FOR SELECT
TO service_role
USING (true);

CREATE POLICY "Service role can insert videos"
ON video_schedule
FOR INSERT
TO service_role
WITH CHECK (true);

CREATE POLICY "Service role can update videos"
ON video_schedule
FOR UPDATE
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Service role can delete videos"
ON video_schedule
FOR DELETE
TO service_role
USING (true);

-- Add user policies
CREATE POLICY "Users can view their own video schedules"
ON video_schedule
FOR SELECT
TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "Users can create their own video schedules"
ON video_schedule
FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update their own video schedules"
ON video_schedule
FOR UPDATE
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete their own video schedules"
ON video_schedule
FOR DELETE
TO authenticated
USING (user_id = auth.uid());
