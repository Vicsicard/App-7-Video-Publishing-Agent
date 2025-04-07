$env:SUPABASE_URL="https://aqicztygjpmunfljjuto.supabase.co"
$env:SUPABASE_SERVICE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxaWN6dHlnanBtdW5mbGpqdXRvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MzcwNTU4MiwiZXhwIjoyMDU5MjgxNTgyfQ.lIfnbWUDm8yDz1g_gQJNi56rCiGRAunY48rgVAwLID4"

# Function to run SQL file against Supabase
function Invoke-SqlMigration {
    param (
        [string]$FilePath
    )
    $sql = Get-Content $FilePath -Raw
    # Escape any special characters in SQL
    $sql = $sql.Replace('"', '\"').Replace("`n", "\n").Replace("`r", "")
    $body = @{
        "query" = $sql
    } | ConvertTo-Json -Compress

    $headers = @{
        "apikey" = $env:SUPABASE_SERVICE_KEY
        "Authorization" = "Bearer $env:SUPABASE_SERVICE_KEY"
        "Content-Type" = "application/json"
        "Prefer" = "return=minimal"
    }

    Write-Host "Running migration: $FilePath"
    try {
        $response = Invoke-RestMethod -Uri "$env:SUPABASE_URL/rest/v1/rpc/exec_sql" -Method Post -Headers $headers -Body $body
        Write-Host "Migration successful"
    } catch {
        Write-Host "Migration failed: $_"
        Write-Host "Request body: $body"
        throw
    }
}

# Run migrations in order
$migrations = @(
    "20250406_create_transcript_files.sql",
    "20250405_fix_transcript_files.sql",
    "20250405_recreate_video_schedule.sql",
    "20250405_add_transcript_files_policies.sql",
    "20250405_add_user_video_policies.sql",
    "20250406_fix_video_schedule_updates.sql",
    "20250407_fix_video_schedule_constraint.sql",
    "20250407_fix_video_schedule_rls.sql",
    "20250407_fix_video_schedule_service_role.sql"
)

foreach ($migration in $migrations) {
    Invoke-SqlMigration "db/migrations/$migration"
}
