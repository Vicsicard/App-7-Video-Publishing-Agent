-- Add file columns to transcript_files
alter table transcript_files
    add column if not exists file_path text not null,
    add column if not exists file_name text not null,
    add column if not exists file_type text not null check (file_type in ('video', 'audio', 'transcript')),
    add column if not exists bucket text not null;

-- Add comments
comment on column transcript_files.file_path is 'Path to the file within the bucket';
comment on column transcript_files.file_name is 'Original name of the uploaded file';
comment on column transcript_files.file_type is 'Type of file: video, audio, or transcript';
comment on column transcript_files.bucket is 'Storage bucket containing the file';

-- Enable RLS on transcript_files
alter table transcript_files enable row level security;

-- Create RLS policy
create policy "Users can manage their own transcript files"
    on transcript_files for all
    using (auth.uid() = user_id);

-- Create helpful indexes
create index if not exists idx_transcript_files_user_id
    on transcript_files(user_id);

create index if not exists idx_transcript_files_file_type
    on transcript_files(file_type);

-- Create storage buckets if they don't exist
insert into storage.buckets (id, name, public)
values
    ('videos', 'videos', false),
    ('documents', 'documents', true)
on conflict (id) do nothing;

-- Create storage policies for videos bucket
create policy "Users can manage their own videos"
    on storage.objects for all
    using (
        bucket_id = 'videos' and
        auth.uid()::text = (storage.foldername(name))[1]
    );

-- Create storage policies for documents bucket
create policy "Users can manage their own documents"
    on storage.objects for all
    using (
        bucket_id = 'documents' and
        auth.uid()::text = (storage.foldername(name))[1]
    );

-- Create storage policies for public access to documents
create policy "Public can read documents"
    on storage.objects for select
    using (bucket_id = 'documents');

-- Add manifest columns to video_schedule
alter table video_schedule
    add column if not exists publish_manifest text,
    add column if not exists manifest_url text;

-- Add comments
comment on column video_schedule.publish_manifest is 'Markdown-formatted publishing manifest';
comment on column video_schedule.manifest_url is 'Public URL to the published manifest';
