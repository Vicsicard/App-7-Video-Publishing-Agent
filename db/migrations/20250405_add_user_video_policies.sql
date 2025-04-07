-- Add user policies for video_schedule table
CREATE POLICY "Users can view their own video schedules"
  ON video_schedule
  FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own video schedules"
  ON video_schedule
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own video schedules"
  ON video_schedule
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own video schedules"
  ON video_schedule
  FOR DELETE
  USING (auth.uid() = user_id);
