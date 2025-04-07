-- Drop existing table and policy
DROP POLICY IF EXISTS "Users can manage their own video schedules" ON video_schedule;
DROP TABLE IF EXISTS video_schedule;

-- Recreate video_schedule table
CREATE TABLE video_schedule (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id uuid REFERENCES transcript_files(id),
    platform text CHECK (platform IN ('youtube', 'instagram', 'facebook', 'website')),
    title text,
    description text,
    tags text[],
    scheduled_at timestamp with time zone,
    published boolean DEFAULT false,
    publish_url text,
    publish_error text,
    created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS
ALTER TABLE video_schedule ENABLE ROW LEVEL SECURITY;

-- Create RLS policy that allows service role to access all rows
CREATE POLICY "Service role can access all videos"
    ON video_schedule FOR ALL
    USING (
        (auth.jwt() ->> 'role'::text) = 'service_role'::text
        OR
        auth.uid() = (
            SELECT user_id 
            FROM transcript_files
            WHERE transcript_files.id = video_schedule.video_id
        )
    );

-- Create helpful indexes
CREATE INDEX IF NOT EXISTS idx_video_schedule_scheduled 
    ON video_schedule(scheduled_at) 
    WHERE NOT published;

CREATE INDEX IF NOT EXISTS idx_video_schedule_video_id 
    ON video_schedule(video_id);
