-- First check if RLS is enabled
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_class
        WHERE relname = 'video_schedule'
        AND relrowsecurity = true
    ) THEN
        -- Enable RLS if it's not enabled
        ALTER TABLE video_schedule ENABLE ROW LEVEL SECURITY;
    END IF;
END $$;

-- Drop existing policies
DROP POLICY IF EXISTS "Service role bypass RLS" ON video_schedule;
DROP POLICY IF EXISTS "Service role can read all videos" ON video_schedule;
DROP POLICY IF EXISTS "Service role can insert videos" ON video_schedule;
DROP POLICY IF EXISTS "Service role can update videos" ON video_schedule;
DROP POLICY IF EXISTS "Service role can delete videos" ON video_schedule;

-- Create explicit policies for service role
CREATE POLICY "Allow read for service role"
ON video_schedule
FOR SELECT
TO service_role
USING (true);

CREATE POLICY "Allow insert for service role"
ON video_schedule
FOR INSERT
TO service_role
WITH CHECK (true);

CREATE POLICY "Allow update for service role"
ON video_schedule
FOR UPDATE
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Allow delete for service role"
ON video_schedule
FOR DELETE
TO service_role
USING (true);

-- Grant all permissions to service role
GRANT ALL ON video_schedule TO service_role;
