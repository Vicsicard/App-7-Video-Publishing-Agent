-- Drop existing policies
DROP POLICY IF EXISTS "Service role can access all videos" ON video_schedule;
DROP POLICY IF EXISTS "Users can view their own video schedules" ON video_schedule;
DROP POLICY IF EXISTS "Users can create their own video schedules" ON video_schedule;
DROP POLICY IF EXISTS "Users can update their own video schedules" ON video_schedule;
DROP POLICY IF EXISTS "Users can delete their own video schedules" ON video_schedule;

-- Add user_id column if it doesn't exist
ALTER TABLE video_schedule 
ADD COLUMN IF NOT EXISTS user_id uuid REFERENCES auth.users(id);

-- Ensure published column has correct default and is not null
ALTER TABLE video_schedule ALTER COLUMN published SET DEFAULT false;
ALTER TABLE video_schedule ALTER COLUMN published SET NOT NULL;

-- Add unique constraint on video_id
ALTER TABLE video_schedule DROP CONSTRAINT IF EXISTS video_schedule_video_id_key;
ALTER TABLE video_schedule ADD CONSTRAINT video_schedule_video_id_key UNIQUE (video_id);

-- Disable RLS temporarily
ALTER TABLE video_schedule DISABLE ROW LEVEL SECURITY;

-- Create new policies with proper permissions
CREATE POLICY "Service role bypass RLS"
ON video_schedule
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Grant permissions to service role
GRANT ALL ON video_schedule TO service_role;
