-- Drop existing policies
DROP POLICY IF EXISTS "Users can manage their own video schedules" ON video_schedule;
DROP POLICY IF EXISTS "Service role can access all videos" ON video_schedule;
DROP POLICY IF EXISTS "Allow service role to read unpublished scheduled videos" ON video_schedule;

-- Create new policies
CREATE POLICY "Allow service role to read unpublished scheduled videos"
  ON video_schedule
  FOR SELECT
  USING (true);

CREATE POLICY "Users can manage their own video schedules"
  ON video_schedule 
  FOR ALL
  USING (
    auth.uid() = (
      SELECT user_id 
      FROM transcript_files
      WHERE transcript_files.id = video_schedule.video_id
    )
  );
