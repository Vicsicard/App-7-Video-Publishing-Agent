# Video Publishing Agent

A robust video publishing automation system that handles scheduling and publishing of video content across multiple platforms.

## Features

### Core Publishing
- ✅ Multi-platform video publishing (YouTube, Meta, Website)
- ✅ Scheduled publishing with configurable dates
- ✅ Automatic video file handling and cleanup
- ✅ Platform-specific metadata support
- ✅ Error handling and retry mechanisms

### Publishing Manifests
- ✅ Automatic manifest generation for all publishes
- ✅ Markdown-formatted summaries
- ✅ Local and cloud storage (Supabase)
- ✅ Success and error status tracking
- ✅ Platform-specific embed codes
- ✅ Detailed metadata including:
  - Transcript ID
  - Platform
  - Scheduled/Published times
  - URLs
  - Status

### Storage & Database
- ✅ Supabase integration for:
  - Video storage
  - Publishing schedules
  - Manifest storage
  - Status tracking
- ✅ Row Level Security (RLS)
- ✅ Public/Private file handling

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
META_ACCESS_TOKEN=your_meta_access_token
```

4. Initialize the database:
```bash
python db/setup_database.py
```

## Usage

### Running the Publisher
```bash
python run_publisher.py
```

This will:
1. Check for videos due for publishing
2. Process each video through its target platform
3. Generate and store publishing manifests
4. Update status in the database

### Manifest Structure
Manifests are stored in two locations:

1. Local: `manifests/manifest_<video_id>_<timestamp>_<status>.md`
2. Supabase: `documents/{user_id}/{transcript_id}/manifest_{video_id}.md`

Each manifest includes:
- Publishing summary
- Platform details
- Timing information
- URLs and embed codes
- Status and any errors

## Database Schema

### video_schedule
- id (uuid, primary key)
- video_id (uuid, references transcript_files)
- platform (text)
- scheduled_at (timestamp)
- published (boolean)
- publish_url (text)
- publish_error (text)
- manifest_path (text)
- manifest_url (text)
- publish_manifest (text)

## Debugging Notes

### Video Upload Issues
Common issues and solutions for video upload problems:

1. Authentication Errors
- Check that SUPABASE_SERVICE_ROLE_KEY is properly set
- Verify RLS policies are correctly configured
- Use service role authentication for storage operations

2. Status Update Issues
- Ensure video_schedule table has correct RLS policies
- Check that service role has necessary permissions
- Verify update queries include correct filters

### Recent Updates (2025-04-07)

1. Improved Authentication
- Centralized header configuration with `get_supabase_headers()`
- Consistent service role key usage across all requests
- Added option to include/exclude `return=representation` header

2. Enhanced Error Handling
- Added comprehensive error logging for database operations
- Improved policy-related issue detection
- Better error messages with request context
- Added logging for silent failures

3. Code Improvements
- Centralized Supabase header management
- Removed redundant header configurations
- Updated video storage to use centralized auth
- Enhanced cleanup function error handling

## Known Issues

None currently. All tests passing as of 2025-04-07.

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
