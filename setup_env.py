"""
Helper script to set up environment variables.
"""
import os
import shutil
from pathlib import Path

# Define source and target paths
source_env = Path("docs/.env")
target_env = Path(".env")

# Read existing content
with open(source_env, "r") as f:
    content = f.read()

# Update environment variable names
content = content.replace("SUPABASE_ANON_KEY", "SUPABASE_SERVICE_KEY")

# Write to root directory
with open(target_env, "w") as f:
    f.write(content)

print("Environment file created in project root.")
print("IMPORTANT: Please add SUPABASE_SERVICE_ROLE_KEY to the .env file if needed")
