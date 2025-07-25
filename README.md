# globalpay-backend
# Overview

This is the mock API server for the **GlobalPay** digital payment system. Built using **Node.js + Express**, it simulates Aadhaar-based biometric verification, wallet functionality, transaction handling, and offline sync.

---

## 🚀 Features

- 🔐 Biometric (Aadhaar) verification
- 💳 Wallet balance and transaction history
- ✅ Simulated payment flow
- 📡 Offline sync simulation
- 🌐 CORS-enabled for frontend communication
- 🧪 Fully mock-driven, no real database

---

## 🛠️ Tech Stack

- **Node.js** with **Express.js**
- JSON-based mock data
- CORS enabled for frontend
- Modular routes and controllers

---

## 📁 Folder Structure
```
globalpay-backend/
├── server.js # Entry point
├── routes/
│ ├── biometric.js
│ ├── wallet.js
│ └── payment.js
├── controllers/
│ ├── biometricController.js
│ ├── walletController.js
│ └── paymentController.js
├── data/
│ └── mockData.js # Simulated data (balance, txns)
├── middleware/
│ └── logger.js # Optional request logger
├── .gitignore
├── package.json
└── README.md

```

---

## 📦 API Endpoints

| Method | Endpoint                     | Description                          |
|--------|------------------------------|--------------------------------------|
| POST   | `/api/verify-biometric`      | Simulate Aadhaar/biometric check     |
| GET    | `/api/wallet/balance`        | Get mock wallet balance              |
| GET    | `/api/wallet/history`        | Fetch recent transactions            |
| POST   | `/api/payment`               | Simulate payment request             |
| POST   | `/api/sync-wallet`           | Offline data sync trigger            |

---

## 🧪 Getting Started

### 1. Clone & Install

```bash
git clone https://github.com/your-username/globalpay-backend.git
cd globalpay-backend
npm install
npm run dev
```
By default, the API runs at:
👉 http://localhost:5000

### 🌐 CORS Notice

CORS is enabled by default to allow communication with the frontend (globalpay-ui on port 3000).

### 👥 Contributors
Satvik Raj

## 📄 License
All rights reserved by Sentienta QualityAI. This project is part of an internal research initiative. Do not redistribute without permission.
