-- Drop existing policies
DROP POLICY IF EXISTS "Allow service role access to videos bucket" ON storage.objects;

-- Create a more permissive policy for service role
CREATE POLICY "Service role has full access to all storage objects"
  ON storage.objects
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');
