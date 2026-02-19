"""
Database Adapter Factory
Routes all database calls to the SQLite adapter for local development
"""

from services.sqlite_adapter import SQLiteAdapter


def get_database_adapter():
    """
    Get the database adapter instance
    
    Returns:
        SQLiteAdapter: Local SQLite database adapter
    """
    return SQLiteAdapter()
