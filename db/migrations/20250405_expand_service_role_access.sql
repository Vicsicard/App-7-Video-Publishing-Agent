-- Drop existing policies
DROP POLICY IF EXISTS "Allow service role to read unpublished scheduled videos" ON video_schedule;

-- Create new policies with expanded access for service role
CREATE POLICY "Service role can select from video_schedule"
  ON video_schedule
  FOR SELECT
  USING (auth.role() = 'service_role');

CREATE POLICY "Service role can insert into video_schedule"
  ON video_schedule
  FOR INSERT
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Service role can update video_schedule"
  ON video_schedule
  FOR UPDATE
  USING (auth.role() = 'service_role');

CREATE POLICY "Service role can delete from video_schedule"
  ON video_schedule
  FOR DELETE
  USING (auth.role() = 'service_role');
