# EC2 Deployment with IAM Roles

## Overview

This application supports **IAM roles** for EC2 deployment, eliminating the need for hardcoded credentials.

---

## Setup Steps

### 1. Create IAM Role for EC2

**Required Permissions:**
- `dynamodb:PutItem`
- `dynamodb:GetItem`
- `dynamodb:Query`
- `dynamodb:Scan`
- `dynamodb:UpdateItem`
- `dynamodb:DeleteItem`
- `dynamodb:CreateTable`
- `dynamodb:DescribeTable`
- `dynamodb:ListTables`

**Create Role:**
1. Go to AWS Console → IAM → Roles
2. Click "Create role"
3. Select "AWS service" → "EC2"
4. Attach policy: `AmazonDynamoDBFullAccess` (or create custom policy with above permissions)
5. Name: `banking-app-ec2-role`
6. Create role

### 2. Launch EC2 Instance with Role

1. Go to EC2 → Launch Instance
2. Select Amazon Linux 2023 AMI
3. **Important**: Under "Advanced details" → "IAM instance profile" → Select `banking-app-ec2-role`
4. Configure security groups (allow port 5000 for Flask)
5. Launch instance

### 3. Deploy Application on EC2

SSH into instance:
```bash
ssh -i your-key.pem ec2-user@your-ec2-ip
```

Install dependencies:
```bash
sudo yum update -y
sudo yum install python3-pip git -y
```

Clone and setup:
```bash
git clone <your-repo>
cd "AWS project"
pip3 install -r requirements.txt
```

Configure environment (no credentials needed!):
```bash
# .env file
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Table names
DYNAMODB_USERS_TABLE=users
DYNAMODB_ACCOUNTS_TABLE=accounts
DYNAMODB_TRANSACTIONS_TABLE=transactions
```

Create tables (if not already created):
```bash
python3 scripts/setup_dynamodb.py
```

Run application:
```bash
python3 app_aws.py
```

---

## How It Works

### Local Development (with credentials)
```python
# boto3 uses explicit credentials from .env
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='AKIA...',
    aws_secret_access_key='...'
)
```

### EC2 with IAM Role (no credentials needed)
```python
# boto3 automatically uses instance role credentials
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1'
    # No credentials needed!
)
```

The code automatically detects which mode to use:
- If `AWS_ACCESS_KEY_ID` is set → use explicit credentials
- If empty → use IAM role (EC2 instance profile)

---

## Benefits of IAM Roles

✅ **No hardcoded credentials** - More secure
✅ **Automatic rotation** - AWS manages credential lifecycle
✅ **No .env secrets** - Can commit .env safely (without credentials)
✅ **AWS best practice** - Recommended by AWS

---

## Testing IAM Role Locally

You can't test IAM roles on your local machine directly, but you can:

1. **Use AWS CLI profiles** (if configured)
2. **Use explicit credentials** in `.env` for development
3. **Test on actual EC2** instance

---

## Troubleshooting

### Error: "Unable to locate credentials"

**On EC2:** Check that IAM role is attached
```bash
# Verify role is attached
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

**Locally:** Add credentials to `.env`

### Error: "Access Denied"

Check IAM role has DynamoDB permissions:
- Go to IAM → Roles → banking-app-ec2-role
- Verify DynamoDB permissions attached

---

## Production Checklist

- [ ] IAM role created with minimal required permissions
- [ ] EC2 instance launched with IAM role attached
- [ ] Security groups configured (port 5000 or 80)
- [ ] DynamoDB tables created
- [ ] Application tested on EC2
- [ ] `.env` file has no hardcoded credentials
