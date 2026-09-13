# 🏦 SecureBank — Banking Management System

> **A professional banking management system built with Python Flask, MySQL (XAMPP), HTML, CSS, and JavaScript.**

<div align="center">

### 🔐 Secure • Reliable • Modular • Database-Driven

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![XAMPP](https://img.shields.io/badge/XAMPP-Local_Server-FB7A24?style=for-the-badge&logo=xampp&logoColor=white)](https://www.apachefriends.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)

</div>

---

## 📌 Project Overview

**SecureBank** is a full-stack banking management system developed using the **Python Flask framework**, **MySQL database**, and a responsive **HTML/CSS frontend**.

The project is designed to simulate the core workflow of a modern banking application, including customer registration, account management, authentication, transactions, profile management, branch management, and administrative operations.

The system follows a structured client-server architecture where:

```text
┌─────────────────────────────────────────────────────────┐
│                    👤 USER / ADMIN                      │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  🌐 HTML + CSS + JS                     │
│                   Frontend Interface                    │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    🐍 FLASK                             │
│              Application / Business Logic               │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  🗄️ MYSQL DATABASE                      │
│                    via XAMPP                            │
└─────────────────────────────────────────────────────────┘
✨ Key Features
👤 Customer Features
🔐 Secure user registration
🔑 User login/logout
🔒 Password management
🔄 Change password functionality
👤 Customer profile
🖼️ Profile image upload
🏦 Bank account creation
💰 Account balance management
💳 Multiple account types
🧾 Transaction history
🔎 Transaction reference tracking
📅 Transaction date/time tracking
📄 Transaction pagination
📊 Dashboard statistics
🏢 Branch selection
🔔 Flash-based notifications
🛡️ Session-based authentication
🏦 Banking Architecture

The system separates customer identity from banking accounts.

A customer can have a unique CIF (Customer Information File) and multiple banking accounts.

                    👤 CUSTOMER
                         │
                         ▼
                    🆔 CIF NUMBER
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
          💰 SAVINGS   💳 CURRENT   🏦 OTHER
           ACCOUNT      ACCOUNT     ACCOUNT
             │           │           │
             ▼           ▼           ▼
        Account No.  Account No.  Account No.

This structure allows one customer identity to be associated with multiple banking products.

👨‍💼 Admin Features

The administrative panel provides centralized control over the banking system.

Admin Dashboard
📊 Total branches
👥 Total customers
🏦 Total accounts
💰 Total bank balance
📋 Account management
🔎 Customer/account information
🏢 Branch information
🔐 Admin authentication
🚫 Account blocking/unblocking
📈 Banking statistics
👤 Customer/account relationship visibility
Account Status Management

Administrators can control account status:

ACTIVE
  │
  ├──► BLOCKED
  │
  └──► ACTIVE
🗄️ Database Structure

The project uses MySQL through XAMPP.

Major database entities include:

users
  │
  ├──────────────► user_cif
  │                    │
  │                    ▼
  │                 CIF Number
  │
  └──────────────► accounts
                       │
                       ├── account_number
                       ├── account_type
                       ├── balance
                       ├── status
                       ├── branch_id
                       └── cif_id
                              │
                              ▼
                           user_cif

branchs
  │
  └──────────────► accounts

transactions
  │
  └──────────────► accounts
🧩 Main Database Tables
Table	Purpose
users	Stores customer information
user_cif	Stores unique CIF information
accounts	Stores customer bank accounts
branchs	Stores bank branch information
transactions	Stores account transaction history
admin / Admin data	Stores administrator authentication data

The exact table structure can be extended as the project grows.

🛠️ Technology Stack
Backend
Python
   │
   └── Flask
        ├── Routing
        ├── Sessions
        ├── Authentication
        ├── Form Processing
        ├── File Upload
        ├── Database Operations
        └── Business Logic
Frontend
HTML5
  │
  ├── Forms
  ├── Tables
  ├── Dashboard
  ├── Navigation
  └── User Interface

CSS3
  │
  ├── Responsive Design
  ├── Animations
  ├── Cards
  ├── Tables
  └── Authentication UI

JavaScript
  │
  ├── UI interactions
  ├── Validation
  └── Dynamic behavior
Database
XAMPP
  │
  └── MySQL / MariaDB
          │
          ├── Users
          ├── Accounts
          ├── CIF
          ├── Branches
          └── Transactions
📁 Project Structure
SecureBank_project/
│
├── .venv/
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── login.css
│   │   ├── dashboard.css
│   │   └── admin.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── uploads/
│       └── profile_images/
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── change_password.html
│   ├── transactions.html
│   │
│   └── admin/
│       ├── login.html
│       └── dashboard.html
│
├── app.py
├── database.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

Folder names may differ depending on the current implementation.

⚙️ Application Workflow
Registration
User
 │
 ▼
Registration Form
 │
 ├── Full Name
 ├── Father's Name
 ├── Email
 ├── Phone
 ├── Password
 ├── Profile Image
 ├── Account Type
 └── Branch
 │
 ▼
Validation
 │
 ▼
Duplicate Customer Check
 │
 ▼
Create User
 │
 ▼
Generate / Assign CIF
 │
 ▼
Create Bank Account
 │
 ▼
Save Data in MySQL
 │
 ▼
Registration Complete
🔐 Authentication Flow
              ┌───────────────┐
              │     LOGIN     │
              └───────┬───────┘
                      │
                      ▼
              Validate Credentials
                      │
              ┌───────┴───────┐
              │               │
            FAIL             SUCCESS
              │               │
              ▼               ▼
          Error Message    Create Session
                              │
                              ▼
                         Dashboard
💳 Transaction System

Transactions are associated with customer accounts.

Example:

Account
   │
   ├── Deposit
   ├── Withdrawal
   ├── Transfer
   └── Other Transaction
          │
          ▼
     transactions
          │
          ├── transaction type
          ├── amount
          ├── reference
          ├── description
          └── created_at

Transaction history supports:

Transaction type
Amount
Reference number
Description
Date/time
Pagination
Account-based filtering
📄 Transaction Pagination

The transaction interface supports configurable pagination.

Items Per Page

[ 5 ] [ 10 ] [ 20 ] [ 50 ]

          ↓

┌─────────────────────────────┐
│ Transaction Records         │
├─────────────────────────────┤
│ Transaction 1               │
│ Transaction 2               │
│ Transaction 3               │
│ ...                         │
└─────────────────────────────┘

       ◀ Previous  1  2  3  Next ▶
🏢 Branch Management

Each banking account can be associated with a bank branch.

Example:

Branch
 │
 ├── Branch Name
 ├── IFSC Code
 └── Branch ID
        │
        ▼
     Account

This allows the system to maintain a relationship between:

Customer → CIF → Account → Branch
🛡️ Security Considerations

Security is an important part of the application architecture.

The project includes or is designed to support:

🔐 Session-based authentication
🔑 Password validation
🔒 Protected routes
🛡️ Admin authorization
🧹 Input validation
🗄️ Parameterized SQL queries
🚫 Duplicate account/customer checks
📁 Controlled file uploads
🔑 Environment-based configuration
🧾 Transaction auditing
⏱️ Session timeout
🚪 Secure logout
🚫 Unauthorized route protection
Important Production Improvements

For real-world deployment, additionally implement:

Password Hashing
       +
CSRF Protection
       +
Secure Cookies
       +
HTTPS
       +
Rate Limiting
       +
Input Sanitization
       +
Strong Authorization
       +
Database Backups
       +
Audit Logging
       +
Secrets Management

This project is an educational/software engineering project and should not be used to process real customer banking information without a professional security, compliance, and infrastructure review.

🧪 Local Development Environment
Requirements

Install:

Python 3.x
Flask
MySQL / MariaDB
XAMPP
HTML5
CSS3
JavaScript
VS Code
Git
🚀 Installation
1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd SecureBank_project
2️⃣ Create Virtual Environment
Windows
python -m venv .venv

Activate:

.venv\Scripts\Activate.ps1

If PowerShell blocks activation:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

Then:

.venv\Scripts\Activate.ps1
📦 3️⃣ Install Dependencies
pip install -r requirements.txt

Or install Flask and MySQL connector manually:

pip install flask mysql-connector-python
🗄️ 4️⃣ Configure XAMPP

Open XAMPP Control Panel.

Start:

Apache   → Start
MySQL    → Start

Open phpMyAdmin:

http://localhost/phpmyadmin

Create the project database.

Example:

CREATE DATABASE securebank;

Then select the database:

USE securebank;

Import or execute the project's database schema.

🔧 5️⃣ Configure Database Connection

Example:

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "securebank"
}

For better security, use environment variables:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=securebank
SECRET_KEY=change-this-value
▶️ 6️⃣ Run the Application
python app.py

The Flask development server will normally be available at:

http://127.0.0.1:5000/

Open the address in your browser.

🔑 Example Application Routes
/
├── /login
├── /register
├── /logout
├── /dashboard
├── /profile
├── /change-password
├── /transactions
│
└── /admin
    ├── /dashboard
    ├── /login
    ├── /logout
    └── /account/<account_id>/toggle

Routes may change as development continues.

🎨 UI / UX

The project focuses on a modern banking dashboard experience.

UI Characteristics
┌─────────────────────────────────────────────────┐
│ 🏦 SecureBank                    👤 User       │
├─────────────────────────────────────────────────┤
│                                                 │
│  💰 Balance        🏦 Accounts     📊 Activity │
│                                                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  Recent Transactions                            │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │ Type │ Amount │ Reference │ Date          │  │
│  ├───────────────────────────────────────────┤  │
│  │ Deposit │ ₹... │ ...      │ ...           │  │
│  │ Withdraw│ ₹... │ ...      │ ...           │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
📊 System Architecture
                         SECUREBANK
                             │
             ┌───────────────┴───────────────┐
             │                               │
         CUSTOMER                          ADMIN
             │                               │
             ▼                               ▼
       Authentication                  Authentication
             │                               │
             ▼                               ▼
         Dashboard                     Admin Dashboard
             │                               │
       ┌─────┼─────┐                   ┌─────┼─────┐
       │     │     │                   │     │     │
       ▼     ▼     ▼                   ▼     ▼     ▼
    Profile Account Transactions    Users Accounts Branches
       │     │     │                   │     │     │
       └─────┴─────┴──────────┬────────┴─────┴─────┘
                              │
                              ▼
                         Flask Backend
                              │
                              ▼
                        MySQL Database
                              │
                              ▼
                            XAMPP
🧠 Development Concepts Demonstrated

This project demonstrates practical software engineering concepts including:

Python programming
Flask web development
MVC-style application organization
HTTP routing
GET/POST requests
HTML forms
Jinja2 templates
Sessions
Authentication
Authorization
CRUD operations
MySQL relational database design
SQL joins
Foreign-key relationships
Pagination
File uploads
Form validation
Error handling
Flash messages
Admin dashboards
Git/GitHub workflow
🔄 CRUD Operations

The application follows the standard CRUD model:

CREATE
  │
  ├── Register Customer
  ├── Create Account
  └── Create Transaction

READ
  │
  ├── Dashboard
  ├── Profile
  ├── Accounts
  └── Transactions

UPDATE
  │
  ├── Profile
  ├── Password
  └── Account Status

DELETE
  │
  └── Controlled administrative operations
🧪 Testing Checklist

Before pushing changes to GitHub:

☐ Registration works
☐ Duplicate email validation works
☐ Login works
☐ Logout works
☐ Session protection works
☐ Dashboard loads correctly
☐ Profile loads correctly
☐ Image upload works
☐ Password change works
☐ Account creation works
☐ Transaction history works
☐ Pagination works
☐ Admin login works
☐ Admin dashboard works
☐ Account blocking works
☐ Database connection works
☐ Invalid routes are handled
☐ SQL queries use parameters
☐ Sensitive configuration is excluded from Git
🌿 Git Workflow

Recommended development workflow:

git status
git add .
git commit -m "Add banking management system features"
git push origin main

For feature development:

main
 │
 ├── feature/authentication
 ├── feature/accounts
 ├── feature/transactions
 ├── feature/admin
 └── feature/ui
🚫 .gitignore

Never commit sensitive or unnecessary files.

Example:

# Virtual Environment
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]

# Environment variables
.env

# IDE
.vscode/
.idea/

# Database
*.sql
*.sqlite
*.db

# Logs
*.log

# Uploaded files
static/uploads/

# OS
.DS_Store
Thumbs.db

If your repository intentionally contains a safe database schema, keep a sanitized schema file such as database/schema.sql rather than committing private customer data.

📈 Future Development Roadmap
Phase 1 — Core Banking
[x] User Registration
[x] User Login
[x] User Dashboard
[x] Account Management
[x] Transaction History
[x] Admin Dashboard
Phase 2 — Advanced Banking
[ ] Fund Transfer
[ ] Beneficiary Management
[ ] Scheduled Transfers
[ ] Transaction Search
[ ] Account Statements
[ ] PDF Statements
[ ] Email Notifications
[ ] OTP Verification
Phase 3 — Security
[ ] CSRF Protection
[ ] Strong Password Hashing
[ ] Login Rate Limiting
[ ] Two-Factor Authentication
[ ] Device/Login History
[ ] Security Audit Logs
[ ] Advanced Role-Based Access Control
Phase 4 — Production Architecture
[ ] PostgreSQL
[ ] Redis
[ ] Background Workers
[ ] Docker
[ ] Nginx
[ ] HTTPS
[ ] CI/CD
[ ] Automated Testing
[ ] Monitoring
[ ] Backup & Recovery
🏗️ Possible Production Architecture

For a future production-grade version:

                         INTERNET
                            │
                            ▼
                         HTTPS
                            │
                            ▼
                          NGINX
                            │
                            ▼
                     Gunicorn / WSGI
                            │
                            ▼
                     Python Backend
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
        PostgreSQL                     Redis
        Primary DB                 Cache / Session
              │                           │
              └─────────────┬─────────────┘
                            │
                            ▼
                    Background Workers
                            │
                            ▼
                  Notifications / Jobs
💡 Why This Project?

SecureBank was designed to provide practical experience with the architecture behind database-driven financial applications.

The project focuses on:

Frontend
   +
Backend
   +
Database
   +
Authentication
   +
Authorization
   +
Business Logic
   +
Security
   +
Administration

Rather than being only a UI project, it demonstrates how different software components communicate to build a complete web application.

👨‍💻 Learning Outcomes

By developing this project, you can gain practical experience in:

🐍 Python
🌐 Flask
🗄️ MySQL
🎨 HTML/CSS
⚡ JavaScript
🔐 Authentication
🛡️ Web Security
📊 Database Design
🔗 SQL Relationships
🧩 Backend Architecture
📁 File Handling
🔄 CRUD
📄 Pagination
👨‍💼 Admin Systems
🌿 Git & GitHub
📌 Project Status
╔══════════════════════════════════════╗
║          SECUREBANK STATUS           ║
╠══════════════════════════════════════╣
║ Backend        : 🟢 Flask            ║
║ Database       : 🟢 MySQL            ║
║ Server         : 🟢 XAMPP            ║
║ Frontend       : 🟢 HTML/CSS         ║
║ Authentication : 🟢 Implemented      ║
║ Admin Panel    : 🟢 Implemented      ║
║ Transactions   : 🟢 Implemented      ║
║ Development    : 🟡 Ongoing          ║
╚══════════════════════════════════════╝
⚠️ Disclaimer

SecureBank is a software development and educational project.

It is not intended to operate as a real financial institution or process real banking credentials, payment information, or customer financial data.

Before deploying a banking application to production, professional security testing, compliance validation, encryption, infrastructure hardening, auditing, monitoring, disaster recovery, and regulatory requirements must be addressed.

📜 License

This project is intended for educational and development purposes.

You may add an appropriate open-source license such as:

MIT License

or another license that matches your intended distribution model.

⭐ Support the Project

If this project helped you learn Flask, MySQL, or full-stack development:

⭐ Star the repository
🍴 Fork the repository
🐛 Report issues
💡 Suggest improvements
🔧 Submit pull requests
<div align="center">
🏦 SecureBank
Building a structured banking system with Python, Flask & MySQL.
Code → Database → Security → Banking → Innovation

Made with 🐍 Python + 🌐 Flask + 🗄️ MySQL + 🎨 HTML/CSS

</div> ```
