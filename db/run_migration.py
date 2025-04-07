#!/usr/bin/env python3

import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.supabase.supabase_client import supabase

def run_migration(migration_file):
    """Run a SQL migration file against Supabase."""
    with open(migration_file, 'r') as f:
        sql = f.read()
        
    # Execute the SQL using the exec_sql RPC function
    response = supabase.rpc("exec_sql", {"query": sql})
    print(f"Migration {migration_file} executed successfully")

if len(sys.argv) < 2:
    print("Usage: python run_migration.py <migration_file>")
    sys.exit(1)

migration_file = sys.argv[1]
run_migration(migration_file)
