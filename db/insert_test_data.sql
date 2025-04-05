-- Insert a test video into transcript_files
insert into transcript_files (id, user_id)
values (
    '00000000-0000-0000-0000-000000000000',
    auth.uid()  -- This will use the current authenticated user's ID
);
