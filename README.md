# Cloud Bank Analytics System

A modern, secure banking analytics platform with **dual-mode architecture** supporting both local SQLite and AWS cloud deployment.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![AWS](https://img.shields.io/badge/AWS-DynamoDB%20%7C%20SNS-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Role-Based Dashboards
- **Fraud Analyst**: Real-time transaction monitoring, fraud detection, account freezing
- **Financial Manager**: Custom reports, trend analysis, performance metrics
- **Compliance Officer**: Regulatory monitoring, threshold alerts, audit logs

### Core Capabilities
- ✅ Real-time transaction processing (deposits, withdrawals, transfers)
- ✅ Advanced fraud detection with pattern analysis
- ✅ Interactive data visualizations (Chart.js)
- ✅ Currency conversion support (₹, $, €, £)
- ✅ Light/Dark theme toggle
- ✅ Secure authentication with role-based access control

### Dual-Mode Architecture
- **Local Mode**: SQLite database for development
- **AWS Mode**: DynamoDB + SNS for production cloud deployment
- **Seamless Switching**: Toggle between modes with one environment variable

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- (Optional) AWS account for cloud mode

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "AWS project"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment**
```bash
# Copy the local configuration
cp .env.local .env
```

4. **Run the application**
```bash
python app_aws.py
```

5. **Access the application**
```
http://localhost:5000
```

### Default Test Accounts
| Email | Password | Role |
|-------|----------|------|
| fraud@test.com | test123 | Fraud Analyst |
| finance@test.com | test123 | Financial Manager |
| compliance@test.com | test123 | Compliance Officer |

---

## 📁 Project Structure

```
AWS project/
├── app_aws.py              # Main Flask application
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
│
├── models/                 # Data models
│   ├── user.py            # User authentication
│   ├── account.py         # Bank accounts
│   └── transaction.py     # Transactions
│
├── services/              # Business logic layer
│   ├── database_adapter.py       # Database abstraction
│   ├── notification_adapter.py   # Notification abstraction
│   └── fraud_detection.py        # Fraud detection engine
│
├── routes/                # API endpoints
│   ├── auth.py           # Authentication routes
│   ├── dashboard.py      # Dashboard routes
│   └── api.py            # REST API endpoints
│
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   └── dashboards/
│
├── static/               # Frontend assets
│   ├── css/
│   ├── js/
│   └── images/
│
├── scripts/              # Utility scripts
│   ├── create_dynamodb_tables.py
│   ├── create_sns_topics.py
│   └── init_db.py
│
└── docs/                 # Documentation
    └── AWS_SETUP.md
```

---

## 🔄 Dual-Mode Operation

### Local Mode (Default)
Uses SQLite database for development and testing.

```env
# .env
USE_AWS=false
DATABASE_PATH=database.db
```

### AWS Cloud Mode
Uses DynamoDB and SNS for production deployment.

```env
# .env
USE_AWS=true
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

### Switching Modes
```bash
# Switch to local mode
cp .env.local .env

# Switch to AWS mode
cp .env.aws .env
```

---

## ☁️ AWS Deployment

### Setup AWS Services

1. **Create DynamoDB Tables**
```bash
python scripts/create_dynamodb_tables.py
```
Creates 5 tables: users, accounts, transactions, notifications, audit-log

2. **Create SNS Topics**
```bash
python scripts/create_sns_topics.py
```
Creates topics for fraud alerts, compliance warnings, and system notifications

3. **Configure Environment**
Update `.env.aws` with your AWS credentials and resource ARNs

4. **Activate AWS Mode**
```bash
cp .env.aws .env
python app_aws.py
```

For detailed AWS setup instructions, see [docs/AWS_SETUP.md](docs/AWS_SETUP.md)

---

## 🛡️ Security Features

- **Password Hashing**: Werkzeug SHA-256 with salt
- **Session Management**: Flask-Login with secure cookies
- **Role-Based Access**: Decorator-based authorization
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Template auto-escaping
- **CSRF Protection**: Flask-WTF tokens

---

## 📊 Technology Stack

### Backend
- **Framework**: Flask 2.3+
- **Authentication**: Flask-Login
- **Database**: SQLite / AWS DynamoDB
- **Notifications**: Local / AWS SNS
- **Cloud SDK**: boto3

### Frontend
- **Templates**: Jinja2
- **Styling**: Custom CSS with theme support
- **Charts**: Chart.js
- **Icons**: Font Awesome

### Cloud Services (Optional)
- **Database**: Amazon DynamoDB
- **Notifications**: Amazon SNS
- **Compute**: Amazon EC2 (for deployment)
- **Monitoring**: CloudWatch

---

## 🎨 Features Showcase

### Fraud Detection Dashboard
- Real-time transaction monitoring
- Automatic pattern-based fraud flagging
- One-click account freezing
- Detailed transaction analysis

### Financial Analytics
- Custom date range reports
- Transaction type breakdowns
- Revenue trend analysis
- Account performance metrics

### Compliance Monitoring
- Regulatory threshold tracking
- Automated compliance alerts
- Audit log generation
- Risk assessment tools

---

## 🧪 Testing

### Run Database Adapter Tests
```bash
python test_adapter.py
```

### Manual Testing Checklist
- [ ] User signup and login
- [ ] Account creation
- [ ] Deposit transaction
- [ ] Withdrawal transaction
- [ ] Transfer between accounts
- [ ] Fraud detection flagging
- [ ] Dashboard data visualization
- [ ] Theme switching
- [ ] Currency conversion

---

## 📈 Performance

### Local Mode (SQLite)
- Response Time: < 50ms
- Concurrent Users: 10-20
- Storage: Unlimited (disk-based)

### AWS Mode (DynamoDB)
- Response Time: 50-100ms (network latency)
- Concurrent Users: 1000+ (auto-scaling)
- Storage: Unlimited (cloud-based)
- Cost: ~$1.35/month (low usage)

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `USE_AWS` | Enable AWS mode | `true` / `false` |
| `FLASK_SECRET_KEY` | Session encryption key | Auto-generated |
| `DATABASE_PATH` | SQLite database file | `database.db` |
| `AWS_REGION` | AWS region | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS credentials | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials | `secret...` |

---

## 📝 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /signup` - New user registration
- `POST /logout` - User logout

### Dashboards
- `GET /fraud_dashboard` - Fraud analyst view
- `GET /financial_dashboard` - Financial manager view
- `GET /compliance_dashboard` - Compliance officer view

### REST API
- `POST /api/deposit` - Create deposit
- `POST /api/withdraw` - Create withdrawal
- `POST /api/transfer` - Create transfer
- `POST /api/flag_fraud` - Flag transaction
- `GET /api/report` - Generate custom report

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

For issues and questions:
- Check [docs/AWS_SETUP.md](docs/AWS_SETUP.md) for AWS configuration
- Review application logs for error details
- Check AWS CloudWatch for cloud deployment issues

---

## 🎯 Roadmap

- [x] Dual-mode architecture (SQLite/DynamoDB)
- [x] Role-based dashboards
- [x] Fraud detection system
- [x] AWS integration (DynamoDB + SNS)
- [ ] EC2 deployment automation
- [ ] Advanced ML fraud detection
- [ ] Mobile responsive design
- [ ] API rate limiting
- [ ] Real-time WebSocket updates

---

## 👥 Authors

Built with ❤️ for modern banking analytics

---

## 🙏 Acknowledgments

- Flask framework and community
- Chart.js for beautiful visualizations
- AWS for cloud infrastructure
- All contributors and testers

---

**Note**: This is a demonstration/educational project. For production use, implement additional security measures, compliance checks, and load testing.
