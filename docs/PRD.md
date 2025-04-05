 App 7: Video Publishing Agent – PRD
App Name:
Video Publishing Agent (App 7 of the Self Cast System)

Purpose:
Automate the scheduling and publishing of finalized video content to supported platforms (YouTube, Instagram, Facebook, and optionally the Web) based on type (longform or shortform) and scheduled time.

🧩 Key Features
1. Platform-Aware Scheduling
Detect video type: shortform vs longform

Support publishing to:

YouTube

Instagram Reels

Facebook Reels

Website (embed or CDN-hosted)

2. Scheduled Execution
Poll the database for videos where:

sql
Copy
Edit
published = false AND scheduled_at <= now()
Publish eligible videos at scheduled time

3. Metadata Handling
Title, description, tags stored in the database

Apply proper formatting per platform

Optionally auto-generate tags from transcript later

4. Upload Logic Per Platform
YouTube: YouTube Data API v3

Schedule via publishAt

Support Shorts if duration < 60s

Instagram & Facebook: Meta Graph API

Reels support

Requires business account setup

Website:

Embed via YouTube or display via Supabase signed link

5. Status Tracking & Logging
Track success or failure for each platform

Save:

published = true

publish_url

publish_error

Log attempts to aid troubleshooting

🗃️ Database Schema
video_schedule
sql
Copy
Edit
create table video_schedule (
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
🔁 Workflow
User approves a video in App 5

App 6 (or UI) allows user to schedule publish time + target platforms

App 7 runs periodically (cron or job trigger):

Scans video_schedule for due items

Fetches video from Supabase via signed URL

Publishes using platform API

Updates status

🔐 Security
All uploads must use signed URLs from Supabase

OAuth2 or long-lived tokens stored securely for platform API access

🧪 Testing
Include test cases for:

Signed URL expiration

Missing metadata

Platform-specific failures (e.g., bad token, invalid format)

Success logging

🧰 Implementation Stack
Layer	Tool or Lib
Language	Python
Job runner	Cron, Celery, or FastAPI w/ schedule endpoint
APIs	YouTube Data API, Meta Graph API
Storage	Supabase
DB tracking	Supabase Postgres
Secrets	.env, not in repo
✅ Success Criteria
Videos are successfully posted to correct platforms at scheduled times

Publish status and URL are stored and retrievable

Platform-specific constraints (e.g., Shorts, Reels) are handled correctly

Logging provides clear diagnostics

