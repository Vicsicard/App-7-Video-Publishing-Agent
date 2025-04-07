-- Drop existing policies
DROP POLICY IF EXISTS "Service role has full access to all storage objects" ON storage.objects;
DROP POLICY IF EXISTS "Allow service role access to videos bucket" ON storage.objects;

-- Add specific policies for service role
CREATE POLICY "Allow service role to insert objects"
  ON storage.objects
  FOR INSERT
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Allow service role to select objects"
  ON storage.objects
  FOR SELECT
  USING (auth.role() = 'service_role');
