-- Drop existing policies
DROP POLICY IF EXISTS "Allow service role to read unpublished scheduled videos" ON video_schedule;

-- Create new policies with full access for service role
CREATE POLICY "Service role has full access to video_schedule"
  ON video_schedule
  FOR ALL
  TO service_role
  USING (true);
