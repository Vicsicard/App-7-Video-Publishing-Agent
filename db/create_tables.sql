-- First, create the transcript_files table
create table if not exists transcript_files (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Then create the video_schedule table
create table if not exists video_schedule (
    id uuid primary key default gen_random_uuid(),
    video_id uuid references transcript_files(id),
    video_type text check (video_type in ('shortform', 'longform')),
    platform text check (platform in ('youtube', 'instagram', 'facebook', 'website')),
    title text,
    description text,
    tags text[],
    scheduled_at timestamp with time zone,
    published boolean default false,
    publish_url text,
    publish_error text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Enable RLS on video_schedule
alter table video_schedule enable row level security;

-- Create the RLS policy
create policy "Users can manage their own video schedules"
    on video_schedule for all
    using (
        auth.uid() = (
            select user_id 
            from transcript_files
            where transcript_files.id = video_schedule.video_id
        )
    );

-- Create helpful indexes
create index if not exists idx_video_schedule_scheduled 
    on video_schedule(scheduled_at) 
    where not published;

create index if not exists idx_video_schedule_video_id 
    on video_schedule(video_id);

-- Add comments
comment on table video_schedule is 'Stores video publishing schedule and status across different platforms';
comment on column video_schedule.video_type is 'Type of video content: shortform (<60s) or longform';
comment on column video_schedule.platform is 'Target platform for publication: youtube, instagram, facebook, or website';
comment on column video_schedule.scheduled_at is 'Scheduled publication timestamp';
comment on column video_schedule.published is 'Whether the video has been successfully published';
comment on column video_schedule.publish_url is 'URL of the published video on the target platform';
comment on column video_schedule.publish_error is 'Error message if publication failed';
