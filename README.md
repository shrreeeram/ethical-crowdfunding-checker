# 🛡 Ethical Crowdfunding Checker

A full-stack Flask application that detects potentially fraudulent crowdfunding campaigns using automated trust scoring and secure admin moderation.

---

## 🚀 Project Overview

Ethical Crowdfunding Checker is a verification system that evaluates campaign legitimacy using rule-based fraud detection. Each campaign is assigned a Trust Score and reviewed by an authenticated admin before approval.

This project demonstrates authentication, MongoDB cloud integration, fraud logic implementation, and production-ready deployment practices.

---

## 🧠 Features

- Secure Admin Login (Flask-Login + Bcrypt)
- MongoDB Atlas Cloud Database
- Trust Score Calculation (0–100)
- Suspicious Keyword Detection
- High Amount Fraud Detection
- Admin Dashboard with:
  - Total Campaigns
  - Approved / Rejected / Pending Count
  - Average Trust Score
- Search by Name
- Status Filter
- Approve / Reject System
- Azure Deployment Ready

---

## 🏗 Tech Stack

Backend: Flask (Python)  
Database: MongoDB Atlas  
Authentication: Flask-Login  
Security: Flask-Bcrypt  
Deployment: Microsoft Azure  
Frontend: HTML  

---

## 📂 Project Structure

ethical-checker/
│
├── app.py  
├── requirements.txt  
├── templates/  
│   ├── index.html  
│   ├── login.html  
│   └── admin.html  
└── static/  

---

## ⚙️ Installation

1. Clone Repository  
git clone https://github.com/YOUR_USERNAME/ethical-checker.git  

2. Create Virtual Environment  
python -m venv venv  
venv\Scripts\activate  

3. Install Dependencies  
pip install -r requirements.txt  

4. Set Environment Variables  
SECRET_KEY=your_secret_key  
MONGO_URI=your_mongodb_connection_string  

5. Run Application  
python app.py  

Visit: http://127.0.0.1:5000/

---

## 🔎 How It Works

1. User submits a crowdfunding campaign.
2. System calculates Trust Score using rule-based fraud logic.
3. Campaign is stored in MongoDB Atlas.
4. Admin logs in securely.
5. Admin approves or rejects campaign manually.

---

## 🎯 Learning Outcomes

- Flask authentication & session handling
- MongoDB Atlas integration
- Cloud-ready application architecture
- Secure password hashing
- Production deployment practices

---

## 👨‍💻 Author

Pruthviraj Patil  
BCA Student | Aspiring Full-Stack & Cloud Developer
