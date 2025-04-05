-- Add manifest columns to video_schedule table
alter table video_schedule 
    add column if not exists manifest_path text,
    add column if not exists manifest_url text,
    add column if not exists publish_manifest text;

-- Add comments
comment on column video_schedule.manifest_path is 'Storage path to the manifest file in Supabase storage';
comment on column video_schedule.manifest_url is 'Public URL to access the manifest file';
comment on column video_schedule.publish_manifest is 'Manifest content in markdown format';
