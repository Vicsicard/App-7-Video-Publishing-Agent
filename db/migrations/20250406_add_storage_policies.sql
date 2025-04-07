-- Add storage policies for documents bucket
DO $$
BEGIN
    -- Create policy for service role access
    EXECUTE format(
        'CREATE POLICY "Service role can access all storage objects" ON storage.objects FOR ALL TO authenticated USING (auth.role() = ''service_role'')'
    );
    
    -- Create policy for public read access to documents
    EXECUTE format(
        'CREATE POLICY "Public can read documents" ON storage.objects FOR SELECT USING (bucket_id = ''documents'')'
    );
END $$;
