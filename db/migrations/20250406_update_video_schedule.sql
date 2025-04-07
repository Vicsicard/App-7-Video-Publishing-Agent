-- Add user_id column to video_schedule
ALTER TABLE video_schedule 
ADD COLUMN IF NOT EXISTS user_id uuid REFERENCES auth.users(id);

-- Update existing policies
DROP POLICY IF EXISTS "Users can view their own video schedules" ON video_schedule;
DROP POLICY IF EXISTS "Users can create their own video schedules" ON video_schedule;
DROP POLICY IF EXISTS "Users can update their own video schedules" ON video_schedule;
DROP POLICY IF EXISTS "Users can delete their own video schedules" ON video_schedule;
DROP POLICY IF EXISTS "Service role can access all videos" ON video_schedule;

-- Create new policies
CREATE POLICY "Service role can access all videos"
    ON video_schedule FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY "Users can view their own video schedules"
    ON video_schedule FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own video schedules"
    ON video_schedule FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own video schedules"
    ON video_schedule FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own video schedules"
    ON video_schedule FOR DELETE
    USING (auth.uid() = user_id);
