-- Create transcript_files table
CREATE TABLE IF NOT EXISTS public.transcript_files (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid REFERENCES auth.users(id),
    file_path text NOT NULL,
    file_name text NOT NULL,
    file_type text NOT NULL,
    bucket text NOT NULL,
    created_at timestamptz DEFAULT NOW()
);
