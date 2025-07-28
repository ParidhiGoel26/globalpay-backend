# globalpay-backend
## Overview

This is the mock API server for the **GlobalPay** digital payment system. Built using **FastAPI**, it simulates Aadhaar based offline e-kyc verification, wallet functionality, and transaction handling.

---
### Clone & Install

```bash
git clone https://github.com/ParidhiGoel26/globalpay-backend.git
cd globalpay-backend
pip install -r requirements.txt
uvicorn main:app
```

Access the api server on http://127.0.0.1:8000/ by default.
http://127.0.0.1:8000/docs for documentation of the implemented

---

## 📦 API Endpoints
### Authentication
| Endpoint | Method | Scope |
| ---- | ---- | ---- |
| `/auth/register` | POST   | - Create a new user with phone number (used as wallet ID) <br> - Stores hashed password <br> - Validates duplicates |
| `/auth/login`    | POST   | - Validates phone/password <br> - Returns a JWT token <br> - Token used to access protected routes|
| `/auth/me`       | GET    | - Returns the logged-in user's data <br> - Manually serialized to avoid pydantic/ORM issues|
| `/auth/kyc`    | POST   | Accepts optional ID proof and a security PIN. On correct PIN (123456), sets KYC as `verified`, creates wallet using phone number as ID. If PIN is incorrect, KYC is marked `pending`. |
| `/auth/verify` | POST   | Verifies OTP (`123456`) and sets `phone_status` to `verified`, then hashes and stores user password. User must exist.|

### Wallet & Transactions
| Endpoint | Method | Scope |
| ---- | ---- | ---- |
| `/wallet/create`       | POST   | - Initializes wallet with `balance = 0` <br> - Uses phone as wallet ID <br> - Links wallet to user|
| `/wallet/balance`      | GET    | - Returns current balance for the authenticated user’s wallet|
| `/wallet/transactions` | GET    | - Lists all transactions done by the user <br> - Filtered via transaction types|
| `/wallet/load`         | POST   | - Adds funds to wallet (simulates bank transfer) <br> - OTP is not required|
| `/wallet/pay`          | POST   | - Transfers money to another wallet <br> - OTP required (`123456`)|
|`/wallet/withdraw `     | POST   | - Deducts the amount from users wallet <br> - OTP required (`123456`)|

### Banks and Biometetrics (Optional)
| Endpoint | Method | Scope |
| ---- | ---- | ---- |
| `/bank/link` | POST   | - Saves user's bank name and masked account number <br> - Linked to user via foreign key |
| `/bank/linked` | GET    | - Returns linked bank details for the authenticated user |
| `/biometric/register` | POST   | - Accepts palm/vein scan placeholder |
