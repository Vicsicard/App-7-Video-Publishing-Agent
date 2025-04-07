-- Set default value for published column
ALTER TABLE video_schedule ALTER COLUMN published SET DEFAULT false;

-- Backfill existing null values
UPDATE video_schedule SET published = false WHERE published IS NULL;
