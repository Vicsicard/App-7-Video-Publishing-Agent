-- Initialize video_schedule table and security policies
-- This table manages the scheduling and tracking of video publications across platforms

-- Create the video_schedule table
create table if not exists video_schedule (
  id uuid primary key default gen_random_uuid(),
  video_id uuid references transcript_files(id),
  video_type text, -- 'shortform' or 'longform'
  platform text,   -- 'youtube', 'instagram', 'facebook', 'website'
  title text,
  description text,
  tags text[],
  scheduled_at timestamp,
  published boolean default false,
  publish_url text,
  publish_error text,
  created_at timestamp default now()
);

-- Add constraints for video_type and platform
ALTER TABLE video_schedule
  ADD CONSTRAINT valid_video_type 
  CHECK (video_type IN ('shortform', 'longform'));

ALTER TABLE video_schedule
  ADD CONSTRAINT valid_platform 
  CHECK (platform IN ('youtube', 'instagram', 'facebook', 'website'));

-- Enable Row Level Security
alter table video_schedule enable row level security;

-- Create policy for user access
create policy "Allow users to manage their own video schedule"
  on video_schedule
  for all
  using (
    auth.uid() = (
      select user_id from transcript_files
      where transcript_files.id = video_schedule.video_id
    )
  );

-- Create indexes for common queries
CREATE INDEX idx_video_schedule_scheduled 
  ON video_schedule(scheduled_at) 
  WHERE NOT published;

CREATE INDEX idx_video_schedule_video_id 
  ON video_schedule(video_id);

-- Add helpful comments
COMMENT ON TABLE video_schedule IS 'Stores video publishing schedule and status across different platforms';
COMMENT ON COLUMN video_schedule.video_type IS 'Type of video content: shortform (<60s) or longform';
COMMENT ON COLUMN video_schedule.platform IS 'Target platform for publication: youtube, instagram, facebook, or website';
COMMENT ON COLUMN video_schedule.scheduled_at IS 'Scheduled publication timestamp';
COMMENT ON COLUMN video_schedule.published IS 'Whether the video has been successfully published';
COMMENT ON COLUMN video_schedule.publish_url IS 'URL of the published video on the target platform';
COMMENT ON COLUMN video_schedule.publish_error IS 'Error message if publication failed';
