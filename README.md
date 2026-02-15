# 🏦 Bank of Mahishmathi

A **Django-based banking web application** designed with **real-world banking rules**, strong security practices, and a **modern user experience**.

> **Bank of Mahishmathi** represents trust, security, and digital banking innovation.

---

## 🚀 Features

### 🔐 Authentication & Security
- User registration and login
- Session-based authentication
- Strong password rules
- Login attempt protection
- CSRF protection
- Role-based access (Admin / User)

---

### 💰 Banking Operations
- Account creation with **minimum initial deposit of ₹100**
- Deposit money
- Withdraw money
- Transfer money (same bank)
- Transaction validation & safety checks
- Account status handling (Active / Disabled)

---

### 📊 User Dashboard
- Current balance overview
- Recent transaction history
- Transaction type indicators (Deposit / Withdraw / Transfer)
- Clean and responsive UI

---

### 🎬 User Experience (UX)
- Opening animation with branding
- Professional landing / About page
- Smooth page transitions
- Animated popup messages for:
  - Login / Logout
  - Deposit / Withdraw / Transfer success
  - Validation and error messages
- Clear user feedback for every action

---

### 🛡️ Admin Panel
- Django Admin integration
- Secure admin access (staff/superuser only)
- User and transaction management

---

## 🧰 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (development)
- **Authentication:** Django Sessions
- **Styling:** Custom CSS
- **Version Control:** Git & GitHub

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/bank-of-mahishmathi.git
cd bank-of-mahishmathi
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run Migrations
python manage.py migrate
5️⃣ Create Superuser
python manage.py createsuperuser
6️⃣ Start Development Server
python manage.py runserver
Open in browser:
http://127.0.0.1:8000/


http://127.0.0.1:8000/
