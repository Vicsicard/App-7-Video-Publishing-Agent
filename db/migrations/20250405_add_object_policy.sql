-- Create storage object policy for service role
CREATE POLICY "Service role can access all objects"
  ON storage.objects
  FOR ALL
  TO service_role
  USING (true);
