# Cloud-hosted Banking Data Analytics and Reporting System on AWS

A production-ready, cloud-based banking analytics platform built with Flask and SQLite for local development, designed for seamless AWS migration.

## Features

### Core Functionality
- **Role-Based Access Control**: Three specialized user roles
  - Fraud Analyst: Real-time fraud detection and monitoring
  - Financial Manager: Custom reports and KPI analytics
  - Compliance Officer: Regulatory compliance tracking
  
- **Transaction Management**
  - Deposit, withdrawal, and transfer operations
  - Real-time balance validation
  - Comprehensive transaction history with filtering
  - Export capabilities (CSV)

- **Analytics Dashboards**
  - Real-time suspicious transaction alerts
  - Financial KPIs and trend analysis
  - Compliance monitoring with threshold alerts
  - Custom report generation

### Security
- Password hashing (Werkzeug)
- Session management (Flask-Login)
- Role-based route protection
- Input validation and sanitization

## Technology Stack

### Phase 1 (Current)
- **Backend**: Flask 3.0
- **Database**: SQLite (local file)
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Charts**: Chart.js

### Phase 2-4 (Future)
- AWS DynamoDB (NoSQL database)
- AWS SNS (notifications)
- AWS IAM (security)
- AWS EC2 (hosting)

## Project Structure

```
d:/AWS project/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── database.db                 # SQLite database
├── .env.example               # Environment template
│
├── models/                     # Data models
├── routes/                     # API endpoints
├── services/                   # Business logic
├── decorators/                 # Auth decorators
├── scripts/                    # Utilities
├── static/                     # CSS, JS, images
└── templates/                  # HTML templates
```

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd "d:/AWS project"
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults work for local development)
   ```

5. **Initialize database**
   ```bash
   python models/init_db.py
   ```

6. **Seed test data**
   ```bash
   python scripts/seed_data.py
   ```

## Running the Application

### Development Server
```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000)

### Test Users

The seed script creates three test users:

| Email | Password | Role |
|-------|----------|------|
| fraud@test.com | test123 | Fraud Analyst |
| finance@test.com | test123 | Financial Manager |
| compliance@test.com | test123 | Compliance Officer |

## Usage

### 1. Login
- Navigate to the login page
- Use one of the test accounts
- You'll be redirected to your role-specific dashboard

### 2. Create Transactions
- Navigate to `/transactions/create`
- Choose transaction type (deposit, withdrawal, transfer)
- Enter amount and account details
- Submit to create transaction

### 3. View Transaction History
- Navigate to `/transactions/history`
- Filter by date range, type, or amount
- Search by transaction ID
- Export to CSV

### 4. Dashboard Features

**Fraud Analyst Dashboard**
- View suspicious transactions
- See real-time alerts
- Drill down into transaction details
- Flag or freeze accounts

**Financial Manager Dashboard**
- View KPIs (total transactions, volume)
- Generate custom reports
- Analyze trends with charts
- Export financial data

**Compliance Officer Dashboard**
- Monitor regulatory metrics
- View threshold alerts
- Access complete audit logs
- Initiate corrective actions

## Development

### Database Schema

**Users Table**
- user_id (PK, UUID)
- name
- email (unique)
- password_hash
- role (FRAUD_ANALYST | FINANCIAL_MANAGER | COMPLIANCE_OFFICER)
- created_at

**Accounts Table**
- account_id (PK, UUID)
- user_id (FK)
- balance
- status
- created_at

**Transactions Table**
- transaction_id (PK, UUID)
- account_id (FK)
- transaction_type (deposit | withdrawal | transfer)
- amount
- timestamp
- status
- fraud_flag (boolean)

### Adding New Features

1. Create route in `routes/`
2. Add business logic in `services/`
3. Create HTML template in `templates/`
4. Add styles in `static/css/`
5. Add JavaScript in `static/js/`

## Phase Roadmap

- **Phase 1** ✅ (Current): Local development with SQLite
- **Phase 2**: Add AWS logic (boto3) while still running locally
- **Phase 3**: Migrate to DynamoDB and AWS services
- **Phase 4**: Deploy to EC2 production

## Configuration

### Environment Variables

```env
# Database Mode
DB_MODE=local          # or 'aws' for Phase 3

# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=development  # or 'production'

# Database Path (local mode)
DATABASE_PATH=database.db

# AWS Configuration (Phase 3+)
# AWS_ACCESS_KEY_ID=your-key
# AWS_SECRET_ACCESS_KEY=your-secret
# AWS_REGION=us-east-1
```

## Troubleshooting

### Database Issues
```bash
# Reset database
rm database.db
python models/init_db.py
python scripts/seed_data.py
```

### Port Already in Use
```bash
# Change port in app.py or kill process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill
```

## Security Notes

- **Never commit** the actual `.env` file
- **Change default passwords** in production
- **Use HTTPS** when deploying
- **Set strong SECRET_KEY** in production
- **Enable CORS** protection for production

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

Proprietary - Banking Application

## Support

For issues or questions, contact the development team.

---

**Project**: Cloud-hosted Banking Data Analytics and Reporting System on AWS  
**Version**: 1.0.0 (Phase 1)  
**Last Updated**: January 2026
