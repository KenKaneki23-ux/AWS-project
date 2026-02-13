# DynamoDB Setup Guide

## Quick Start

### 1. Configure AWS Credentials

Edit your `.env` file and add your AWS credentials:

```env
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
```

### 2. Run the Setup Script

```bash
python scripts/setup_dynamodb.py
```

This will automatically create all required DynamoDB tables:
- `cloudbank-users`
- `cloudbank-accounts`
- `cloudbank-transactions`
- `cloudbank-notifications`

### 3. Start the Application

```bash
python app_aws.py
```

---

## What Gets Created

### Users Table
- **Partition Key**: `user_id` (String)
- **GSI**: `email-index` on `email` field
- **Capacity**: 5 RCU / 5 WCU

### Accounts Table
- **Partition Key**: `account_id` (String)
- **GSI**: `user-accounts-index` on `user_id` field
- **Capacity**: 5 RCU / 5 WCU

### Transactions Table
- **Partition Key**: `transaction_id` (String)
- **GSI**: `account-transactions-index` on `account_id` + `timestamp`
- **Capacity**: 5 RCU / 5 WCU

### Notifications Table
- **Partition Key**: `notification_id` (String)
- **GSI**: `user-notifications-index` on `user_id` field
- **Capacity**: 5 RCU / 5 WCU

---

## Troubleshooting

### Error: "Unable to locate credentials"

Make sure your `.env` file has valid AWS credentials:
```env
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
```

### Error: "Table already exists"

This is normal! The script checks for existing tables and only creates missing ones.

### Error: "Access Denied"

Your AWS IAM user needs the following permissions:
- `dynamodb:CreateTable`
- `dynamodb:DescribeTable`
- `dynamodb:ListTables`

---

## Manual Table Creation (AWS Console)

If you prefer to create tables manually:

1. Go to AWS Console → DynamoDB → Tables → Create table
2. For each table, use the schema shown above
3. Enable the Global Secondary Indexes as specified

---

## Cost Estimate

With provisioned capacity (5 RCU / 5 WCU per table):
- **4 tables** × **$0.00065/hour** = ~**$1.87/month**

For development, you can use AWS Free Tier which includes:
- 25 GB storage
- 25 RCU + 25 WCU (enough for all 4 tables)

---

## Next Steps

After setup is complete:
1. ✅ Tables are created in DynamoDB
2. ✅ Application can connect to database
3. 🔄 Run the application: `python app_aws.py`
4. 🔄 Create test users and data through the UI
