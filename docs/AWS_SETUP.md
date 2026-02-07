# AWS Setup Guide

This guide will help you set up AWS services for the Cloud Banking Analytics application.

## Prerequisites

1. **AWS Account**: Create one at [aws.amazon.com](https://aws.amazon.com)
2. **AWS CLI**: Install and configure (optional but recommended)
3. **Python boto3**: Already installed via `requirements.txt`

---

## Step 1: Create IAM User

1. Go to AWS Console → IAM → Users → Add User
2. User name: `cloudbank-developer

`
3. Access type: **Programmatic access**
4. Attach policies:
   - `AmazonDynamoDBFullAccess`
   - `AmazonSNSFullAccess`
   - `CloudWatchFullAccess`
5. **Save the Access Key ID and Secret Access Key**

---

## Step 2: Configure Credentials

Add your AWS credentials to `.env.aws`:

```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA_YOUR_ACCESS_KEY_HERE
AWS_SECRET_ACCESS_KEY=your_secret_access_key_here
```

Or configure AWS CLI:
```bash
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key
# Default region: us-east-1
# Default output format: json
```

---

## Step 3: Create DynamoDB Tables

Run the table creation script:

```bash
python scripts/create_dynamodb_tables.py
```

This creates 5 tables:
- `cloudbank-users`
- `cloudbank-accounts`
- `cloudbank-transactions`
- `cloudbank-notifications`
- `cloudbank-audit-log`

**Cost**: ~$1.25/month for low usage (Free tier: 25GB storage, 200M requests)

---

## Step 4: Create SNS Topics

Run the SNS topic creation script:

```bash
python scripts/create_sns_topics.py
```

This creates 3 topics:
- `cloudbank-fraud-alerts`
- `cloudbank-compliance-warnings`
- `cloudbank-system-alerts`

**Important**: Confirm email subscriptions sent to your inbox!

**Cost**: ~$0.50/month for 1,000 emails (Free tier: 1,000 emails)

---

## Step 5: Update .env.aws

Copy the SNS topic ARNs from the script output to `.env.aws`:

```env
SNS_FRAUD_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:cloudbank-fraud-alerts
SNS_COMPLIANCE_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:cloudbank-compliance-warnings
SNS_SYSTEM_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:cloudbank-system-alerts
```

---

## Step 6: Migrate Data (Optional)

If you have existing SQLite data:

```bash
python scripts/migrate_sqlite_to_dynamodb.py
```

This will copy all data from `database.db` to DynamoDB tables.

---

## Step 7: Switch to AWS Mode

```bash
# Copy AWS config to active .env
cp .env.aws .env

# Or manually set USE_AWS=true in .env
USE_AWS=true
```

---

## Step 8: Test Application

Start the application:

```bash
python app_aws.py
```

Test all features:
- ✅ Login/signup
- ✅ Create transactions
- ✅ Flag fraud (should trigger SNS notification)
- ✅ View dashboards

---

## Troubleshooting

### Issue: "Unable to locate credentials"
**Solution**: Make sure AWS credentials are in `.env.aws` or configured via `aws configure`

### Issue: "Table already exists"
**Solution**: Tables are already created. Skip table creation step.

### Issue: "Access Denied"
**Solution**: Check IAM user has required permissions (DynamoDB, SNS)

### Issue: "Region not found"
**Solution**: Verify `AWS_REGION` in `.env.aws` is correct

---

## Cost Summary

| Service | Usage | Monthly Cost | Free Tier |
|---------|-------|--------------|-----------|
| DynamoDB | 1GB, 1M requests | $1.25 | 25GB, 200M requests (12 months) |
| SNS | 1,000 emails | $0.10 | 1,000 emails (forever) |
| CloudWatch | Basic monitoring | $0.00 | 10 metrics (forever) |
| **Total** | | **~$1.35/month** | **Free for 12 months!** |

---

## Switch Back to Local Mode

```bash
# Copy local config
cp .env.local .env

# Or set USE_AWS=false
USE_AWS=false
```

Application will work with SQLite again!

---

## Next Steps

After AWS is working:
1. Deploy to EC2 (see `deployment/` folder)
2. Set up CloudWatch alarms
3. Configure auto-scaling (if needed)

---

## Support

For issues, check:
- AWS Console → CloudWatch → Logs
- Application logs
- AWS Service Health Dashboard
