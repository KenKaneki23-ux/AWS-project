#!/bin/bash

# EC2 Database Initialization Script
# Run this on your EC2 instance to create the database tables

echo "======================================"
echo "Database Initialization Script"
echo "======================================"

# Navigate to project directory
cd /home/ec2-user/AWS-project || cd /home/ubuntu/AWS-project || cd ~/AWS-project

# Check if we're in the right directory
if [ ! -f "app_aws.py" ]; then
    echo "Error: Cannot find app_aws.py"
    echo "Please navigate to your project directory first"
    exit 1
fi

echo "✓ Found project directory"

# Initialize the database
echo ""
echo "Initializing database..."
python3 scripts/init_db.py

if [ $? -eq 0 ]; then
    echo "✓ Database tables created successfully"
else
    echo "✗ Database initialization failed"
    exit 1
fi

# Seed test data (optional)
echo ""
echo "Do you want to add test data? (y/n)"
read -r answer
if [ "$answer" = "y" ]; then
    python3 scripts/seed_data.py
    echo "✓ Test data added"
fi

echo ""
echo "======================================"
echo "✓ Database setup complete!"
echo "======================================"
echo ""
echo "Your application is ready to use."
echo "Access it at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5000"
