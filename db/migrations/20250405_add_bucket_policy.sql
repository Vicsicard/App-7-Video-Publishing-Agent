-- Create storage bucket policy for service role
CREATE POLICY "Service role can access all buckets"
  ON storage.buckets
  FOR ALL
  TO service_role
  USING (true);
