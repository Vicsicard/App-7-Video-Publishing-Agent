"""
Supabase client configuration.
"""

import os
import httpx
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")

def get_supabase_headers(*, include_representation: bool = True) -> Dict[str, str]:
    """Get headers for Supabase requests with service role authentication."""
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    if include_representation:
        headers["Prefer"] = "return=representation"
    return headers

class SupabaseClient:
    """Simple Supabase client for database operations."""
    
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        
    def table(self, name: str) -> 'TableQuery':
        """Create a query for the given table."""
        return TableQuery(self, name)

class TableQuery:
    """Query builder for Supabase tables."""
    
    def __init__(self, client: SupabaseClient, table: str):
        self.client = client
        self.table = table
        self.query_params: Dict[str, Any] = {}
        self.select_cols = "*"
        self.filters = {}
        
    def select(self, columns: str) -> 'TableQuery':
        """Select specific columns."""
        self.select_cols = columns
        return self
        
    def eq(self, column: str, value: Any) -> 'TableQuery':
        """Add equals filter."""
        self.filters[column] = value
        self.query_params[column] = f"eq.{value}"
        return self
        
    def lte(self, column: str, value: Any) -> 'TableQuery':
        """Add less than or equal filter."""
        self.query_params[column] = f"lte.{value}"
        return self
        
    def order(self, column: str, order: str = "asc") -> 'TableQuery':
        """Add order by clause."""
        self.query_params["order"] = f"{column}.{order}"
        return self
        
    def update(self, data: Dict[str, Any]) -> 'TableQuery':
        """Set update data."""
        self.update_data = data
        return self
        
    def execute(self) -> Any:
        """Execute the query."""
        url = f"{self.client.url}/rest/v1/{self.table}"
        
        # Handle SELECT queries
        if not hasattr(self, 'update_data'):
            try:
                response = httpx.get(
                    url, 
                    headers=get_supabase_headers(include_representation=False), 
                    params=self.query_params
                )
                response.raise_for_status()
                return type('Response', (), {'data': response.json()})
            except httpx.HTTPError as e:
                logger.error(f"Failed to execute SELECT query: {str(e)}")
                logger.error(f"Response text: {e.response.text if hasattr(e, 'response') else 'No response'}")
                raise
            
        # Handle UPDATE queries
        else:
            # Convert query params to filter string
            filter_params = {}
            for column, value in self.filters.items():
                filter_params[column] = f"eq.{value}"
            
            try:
                # Use PATCH for update
                response = httpx.patch(
                    url,
                    headers=get_supabase_headers(),
                    params=filter_params,
                    json=self.update_data
                )
                response.raise_for_status()
                
                data = response.json()
                if not data:
                    logger.error(f"Update succeeded but returned no data. This may indicate a policy issue.")
                    logger.error(f"Update params: {filter_params}")
                    logger.error(f"Update data: {self.update_data}")
                
                return type('Response', (), {'data': data})
                
            except httpx.HTTPError as e:
                logger.error(f"Failed to execute UPDATE query: {str(e)}")
                logger.error(f"Response text: {e.response.text if hasattr(e, 'response') else 'No response'}")
                logger.error(f"Update params: {filter_params}")
                logger.error(f"Update data: {self.update_data}")
                raise
            
# Create global client instance
supabase = SupabaseClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
