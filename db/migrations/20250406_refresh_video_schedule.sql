-- Refresh the video_schedule table to force schema cache update
ALTER TABLE video_schedule ALTER COLUMN description SET DATA TYPE text;
