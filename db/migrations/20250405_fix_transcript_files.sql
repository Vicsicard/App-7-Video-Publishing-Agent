-- Drop the transcript_id column from transcript_files if it exists
alter table transcript_files
    drop column if exists transcript_id;

-- Update video_schedule to reference transcript_files.id
do $$
begin
    if exists (
        select 1
        from information_schema.columns
        where table_name = 'video_schedule'
        and column_name = 'video_id'
    ) then
        alter table video_schedule
            rename column video_id to transcript_id;
    end if;
end $$;
