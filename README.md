# 🏠 Nivasa - Hostel Management System

A Flask-based Hostel Management System with AI-powered complaint classification and a student AI assistant.

## 📌 About the Project

**Nivasa** is a college project designed to simplify and digitize hostel management.

The system provides separate interfaces for **Administrators** and **Students**, allowing hostel-related activities such as room management, student management, complaints, leave requests, fees, notices, and notifications to be managed through a single web application.

It also includes AI features to automatically classify student complaints and provide an AI-based assistant for common hostel-related queries.

---

## ✨ Key Features

### 👨‍💼 Admin Module

- Admin authentication
- Admin dashboard
- Hostel management
- Room management
- Student account creation and management
- Room allocation
- Complaint management
- Leave request management
- Fee management
- Notice creation
- Student notifications
- Complaint category and priority analysis

### 👨‍🎓 Student Module

- Secure student login
- Student dashboard
- Student profile management
- View allocated room
- Submit complaints
- Track complaint status
- Submit leave requests
- Track leave request status
- View hostel fees
- Fee payment simulation
- View notices
- Receive notifications
- AI Assistant

### 🤖 AI Features

#### AI Complaint Classification

Student complaints are automatically analyzed and classified into categories such as:

- Plumbing
- Electrical
- Cleaning
- Internet
- Furniture
- Other

The system also assigns a complaint priority such as:

- High
- Medium
- Low

#### AI Student Assistant

The AI Assistant can help students with common hostel-related information such as:

- Room information
- Fee information
- Complaint status
- Leave request status
- Profile information
- General hostel assistance

---

## 🔐 Security Features

Nivasa includes several security mechanisms:

- Flask-Login authentication
- Password hashing
- Role-based access control
- Student and admin route protection
- CSRF protection
- Secure session cookies
- Student data isolation
- IDOR/access-control protection
- Input validation
- Authentication checks on protected routes

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend programming |
| Flask | Web framework |
| Flask-SQLAlchemy | Database ORM |
| SQLite | Database |
| Flask-Login | Authentication |
| Flask-WTF | CSRF protection |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend interaction |
| Scikit-learn | AI complaint classification |
| TF-IDF | Text feature extraction |
| Logistic Regression | Complaint classification |

---

## 📂 Project Structure

```text
Nivasa-Hostel-Management-System/
│
├── ai/
│   ├── assistant.py
│   └── complaint_classifier.py
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   ├── __init__.py
│   └── extensions.py
│
├── config.py
├── requirements.txt
├── run.py
├── .gitignore
└── README.md
