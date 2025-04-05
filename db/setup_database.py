#!/usr/bin/env python3
"""
Database setup script for the Video Publishing Agent.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from lib.supabase.supabase_client import supabase

def run_sql_direct(sql: str) -> None:
    """
    Run SQL directly using REST API.
    
    Args:
        sql: SQL to execute
    """
    try:
        # Execute SQL directly using REST API
        result = supabase.postgrest.schema('public').rpc('exec_sql', {'query': sql}).execute()
        return True
    except Exception as e:
        raise

def setup_database() -> None:
    """Set up the database schema and initial data."""
    try:
        # Get the directory containing this script
        db_dir = Path(__file__).parent
        
        # Run the main schema creation
        print("Creating tables...")
        with open(db_dir / "create_tables.sql", 'r') as f:
            run_sql_direct(f.read())
        
        # Run all migrations in order
        migrations_dir = db_dir / "migrations"
        if migrations_dir.exists():
            print("Running migrations...")
            for migration_file in sorted(migrations_dir.glob("*.sql")):
                print(f"Applying {migration_file.name}...")
                with open(migration_file, 'r') as f:
                    run_sql_direct(f.read())
                
        print("Database setup complete!")
        
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        raise

if __name__ == "__main__":
    setup_database()
