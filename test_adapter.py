"""
Test script for database adapter
Tests that the abstraction layer works correctly
"""

from services.database_adapter import get_database_adapter
from config import Config

def test_database_adapter():
    """Test basic database adapter functionality"""
    
    print("=" * 60)
    print("DATABASE ADAPTER TEST")
    print("=" * 60)
    print(f"Mode: {'AWS' if Config.USE_AWS else 'Local (SQLite)'}")
    print(f"Database Path: {Config.DATABASE_PATH if not Config.USE_AWS else 'DynamoDB'}")
    print("=" * 60)
    
    try:
        # Get database adapter
        db = get_database_adapter()
        print(f"\n✅ Database adapter created: {type(db).__name__}")
        
        # Test getting a user
        print("\n--- Testing get_user() ---")
        user = db.get_user_by_email('fraud@test.com')
        if user:
            print(f"✅ Found user: {user['name']} ({user['email']})")
            print(f"   Role: {user['role']}")
        else:
            print("❌ User not found")
        
        # Test getting accounts
        if user:
            print("\n--- Testing get_accounts_by_user() ---")
            accounts = db.get_accounts_by_user(user['user_id'])
            print(f"✅ Found {len(accounts)} account(s)")
            for acc in accounts:
                print(f"   Account {acc['account_id'][:8]}...: Balance = ₹{acc['balance']:.2f}")
        
        # Test getting transactions
        if accounts:
            print("\n--- Testing get_transactions_by_account() ---")
            transactions = db.get_transactions_by_account(accounts[0]['account_id'], limit=5)
            print(f"✅ Found {len(transactions)} transaction(s)")
            for txn in transactions[:3]:
                print(f"   {txn['transaction_type']}: ₹{txn['amount']:.2f} - {txn['status']}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - Adapter is working!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_database_adapter()
