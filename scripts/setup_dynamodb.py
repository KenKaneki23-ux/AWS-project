"""
Setup script for DynamoDB tables
Run this script to create all required tables in AWS
"""

import sys
import os

# Add parent directory to path so we can import from models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.init_db import init_db

if __name__ == '__main__':
    print("\n🚀 Starting DynamoDB Setup...\n")
    
    try:
        init_db()
        print("\n✅ Setup complete! You can now run the application.\n")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
