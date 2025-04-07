-- Create videos bucket if it doesn't exist
INSERT INTO storage.buckets (id, name, public) 
VALUES ('videos', 'videos', true)
ON CONFLICT (id) DO NOTHING;

-- Create policy for videos bucket
CREATE POLICY "Allow service role access to videos bucket"
  ON storage.objects
  FOR ALL
  USING (bucket_id = 'videos' AND auth.role() = 'service_role')
  WITH CHECK (bucket_id = 'videos' AND auth.role() = 'service_role');
