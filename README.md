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
