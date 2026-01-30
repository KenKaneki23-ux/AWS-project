"""
Seed database with test data
Creates sample users, accounts, and transactions for testing
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from models.account import Account
from models.transaction import Transaction
import random
from datetime import datetime, timedelta

def seed_data():
    """Populate database with test data"""
    
    print("🌱 Seeding database with test data...")
    
    # Create test users (one for each role)
    print("\n👥 Creating users...")
    
    fraud_analyst = User.create(
        name="Sarah Johnson",
        email="fraud@test.com",
        password="test123",
        role="FRAUD_ANALYST"
    )
    print(f"✅ Created Fraud Analyst: {fraud_analyst.email}")
    
    financial_manager = User.create(
        name="John Martinez",
        email="finance@test.com",
        password="test123",
        role="FINANCIAL_MANAGER"
    )
    print(f"✅ Created Financial Manager: {financial_manager.email}")
    
    compliance_officer = User.create(
        name="Lisa Chen",
        email="compliance@test.com",
        password="test123",
        role="COMPLIANCE_OFFICER"
    )
    print(f"✅ Created Compliance Officer: {compliance_officer.email}")
    
    # Create regular test users
    users = [fraud_analyst, financial_manager, compliance_officer]
    
    for i in range(1, 8):
        user = User.create(
            name=f"Test User {i}",
            email=f"user{i}@test.com",
            password="test123",
            role=random.choice(["FRAUD_ANALYST", "FINANCIAL_MANAGER", "COMPLIANCE_OFFICER"])
        )
        users.append(user)
        print(f"✅ Created User: {user.email}")
    
    # Create accounts for users
    print("\n💳 Creating accounts...")
    accounts = []
    
    for user in users:
        # Create 1-2 accounts per user with random initial balances
        num_accounts = random.randint(1, 2)
        for _ in range(num_accounts):
            initial_balance = round(random.uniform(1000, 50000), 2)
            account = Account.create(user.user_id, initial_balance)
            accounts.append(account)
            print(f"✅ Created account {account.account_id[:8]}... for {user.name} with balance ${initial_balance:,.2f}")
    
    # Create sample transactions
    print("\n💰 Creating transactions...")
    transaction_count = 0
    
    # Create deposits
    for _ in range(15):
        account = random.choice(accounts)
        amount = round(random.uniform(100, 5000), 2)
        try:
            Transaction.create_deposit(
                account.account_id,
                amount,
                description=f"Deposit - {random.choice(['Salary', 'Bonus', 'Refund', 'Payment received'])}"
            )
            transaction_count += 1
        except Exception as e:
            print(f"❌ Deposit failed: {e}")
    
    print(f"✅ Created {transaction_count} deposit transactions")
    
    # Create withdrawals
    withdrawal_count = 0
    for _ in range(12):
        account = random.choice(accounts)
        # Ensure withdrawal doesn't exceed balance
        max_withdrawal = account.balance * 0.3  # Max 30% of balance
        if max_withdrawal > 50:
            amount = round(random.uniform(50, max_withdrawal), 2)
            try:
                Transaction.create_withdrawal(
                    account.account_id,
                    amount,
                    description=f"Withdrawal - {random.choice(['ATM', 'Bill payment', 'Cash withdrawal', 'Purchase'])}"
                )
                withdrawal_count += 1
            except Exception as e:
                pass  # Skip if insufficient balance
    
    print(f"✅ Created {withdrawal_count} withdrawal transactions")
    
    # Create transfers
    transfer_count = 0
    for _ in range(10):
        if len(accounts) < 2:
            break
        
        from_account = random.choice(accounts)
        to_account = random.choice([a for a in accounts if a.account_id != from_account.account_id])
        
        max_transfer = from_account.balance * 0.2  # Max 20% of balance
        if max_transfer > 100:
            amount = round(random.uniform(100, max_transfer), 2)
            try:
                Transaction.create_transfer(
                    from_account.account_id,
                    to_account.account_id,
                    amount,
                    description=f"Transfer - {random.choice(['Payment', 'Gift', 'Loan repayment', 'Shared expense'])}"
                )
                transfer_count += 1
            except Exception as e:
                pass
    
    print(f"✅ Created {transfer_count} transfer transactions")
    
    # Flag some transactions as suspicious (for fraud analyst dashboard)
    print("\n🚨 Flagging suspicious transactions...")
    all_transactions = Transaction.get_all(limit=50)
    flagged_count = 0
    
    # Flag large transactions as suspicious
    for txn in all_transactions:
        if txn.amount > 10000 and random.random() < 0.3:  # 30% chance to flag large transactions
            txn.flag_fraud()
            flagged_count += 1
    
    print(f"✅ Flagged {flagged_count} suspicious transactions")
    
    # Summary
    print("\n" + "="*60)
    print("🎉 Database seeding completed!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"  • Users created: {len(users)}")
    print(f"  • Accounts created: {len(accounts)}")
    print(f"  • Total transactions: {transaction_count + withdrawal_count + transfer_count}")
    print(f"  • Flagged transactions: {flagged_count}")
    
    print(f"\n🔑 Test Login Credentials:")
    print(f"  • Fraud Analyst:      fraud@test.com / test123")
    print(f"  • Financial Manager:  finance@test.com / test123")
    print(f"  • Compliance Officer: compliance@test.com / test123")
    print(f"  • Regular Users:      user1@test.com to user7@test.com / test123")
    
    print(f"\n✨ Next step: Run 'python app.py' to start the application")

if __name__ == '__main__':
    seed_data()
