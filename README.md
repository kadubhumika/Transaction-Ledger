# 🚀 Tranasaction Ledger

RBI Ledger is a full-stack digital banking simulation platform built with FastAPI, PostgreSQL, Redis, and WebSockets. The system supports secure OTP-based authentication, multi-bank account management, real-time money transfers, scheduled payments, live notifications, PDF statement generation, and spending analytics.

## ✨ Features

* 🔐 OTP-based Email Authentication using Brevo SMTP
* 🏦 Multi-Bank Account Management (SBI, HDFC, ICICI, etc.)
* 💸 Real-Time Money Transfers Between Accounts
* 📡 Live WebSocket Notifications
* ⏰ Scheduled Future Payments with Background Scheduler
* 📄 PDF Bank Statement Generation
* 📊 Spending Analytics Dashboard
* 👤 User Profile Management
* ⚡ Redis Caching for Faster Performance
* 🔑 JWT Authentication & Authorization

## 🛠 Tech Stack

* **Backend:** FastAPI, Python, Uvicorn
* **Database:** PostgreSQL (Neon)
* **Caching:** Redis
* **ORM:** SQLAlchemy
* **Authentication:** JWT + OTP Verification
* **Notifications:** WebSockets
* **Email Service:** Brevo SMTP
* **PDF Generation:** ReportLab
* **Frontend:** HTML, CSS, JavaScript

## ⚙️ Local Setup

### Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
python -m http.server 5500
```

### Docker (Optional)

```bash
docker-compose up --build -d
```

## 📌 Highlights

* Implemented secure OTP-based login workflow
* Added real-time transaction notifications using WebSockets
* Integrated Redis caching for performance optimization
* Automated scheduled payments with background job processing
* Generated downloadable PDF account statements
* Built analytics APIs for expense tracking and spending insights

  <img width="700" height="700" alt="image" src="https://github.com/user-attachments/assets/4c7ad04a-bd13-4598-b88f-dccf1f0376a0" />

## 👩‍💻 Developer

**Bhumika Kadu**

---

### 🌐 Live Demo - https://transaction-ledger-frontend.onrender.com 
## 🛠️ Tech Stack & Infrastructure Architecture

*   **Backend Framework:** FastAPI (Asynchronous Python Web Services)
*   **Primary Database:** PostgreSQL hosted on **Neon DB** (Serverless Data Layer with connection pooling)
*   **Hosting Platform:** **Render** (Cloud Web Service running asynchronous Uvicorn workers)
*   **Caching & OTP Management:** **Redis Cache** (5-minute expiration lifecycles for security tokens)
*   **Real-time Notifications:** HTML5 WebSockets (Instant state updates across login/payment sessions)
*   **Automated Communication:** **Brevo Web REST API v3** (Transactional OTP delivery over HTTP to bypass cloud port blocks)
