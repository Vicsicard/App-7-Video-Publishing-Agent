-- Add RLS policies for transcript_files table
ALTER TABLE public.transcript_files ENABLE ROW LEVEL SECURITY;

-- Service role policies
CREATE POLICY "Service role can select from transcript_files"
  ON transcript_files
  FOR SELECT
  USING (auth.role() = 'service_role');

CREATE POLICY "Service role can insert into transcript_files"
  ON transcript_files
  FOR INSERT
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Service role can update transcript_files"
  ON transcript_files
  FOR UPDATE
  USING (auth.role() = 'service_role');

CREATE POLICY "Service role can delete from transcript_files"
  ON transcript_files
  FOR DELETE
  USING (auth.role() = 'service_role');

-- User policies
CREATE POLICY "Users can view their own transcript files"
  ON transcript_files
  FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own transcript files"
  ON transcript_files
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own transcript files"
  ON transcript_files
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own transcript files"
  ON transcript_files
  FOR DELETE
  USING (auth.uid() = user_id);
