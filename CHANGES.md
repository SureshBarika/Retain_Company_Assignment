# CHANGES.md

## Overview
This document summarizes the key changes made to refactor the legacy Flask-based user management API. The primary goals were to improve code organization, security, maintainability, and adherence to best practices.

---

## 🔧 Major Issues Identified

1. **SQL Injection Vulnerabilities**
   - Unsafe string interpolation was used in SQL queries.
   - ✅ Fixed using parameterized queries via SQLite placeholders (`?`).

2. **Plaintext Password Storage**
   - Passwords were stored without any encryption.
   - ✅ Fixed using `werkzeug.security`'s password hashing (`generate_password_hash`, `check_password_hash`).

3. **Poor Code Structure**
   - All code was bundled in `app.py`, violating separation of concerns.
   - ✅ Split code into logical modules (`routes.py`, `models.py`, `db.py`, `utils.py`).

4. **Unvalidated Input Data**
   - Incoming JSON requests were not validated.
   - ✅ Added basic field presence checks for required parameters.

5. **Unclear and Inconsistent Responses**
   - Responses were plain strings or incomplete JSON.
   - ✅ Fixed to return consistent JSON responses with appropriate HTTP status codes.

6. **Global Database Connection**
   - Shared global SQLite connection across requests (`check_same_thread=False`).
   - ✅ Replaced with request-scoped connection using Flask `g` context.

---

## 🧱 Refactoring Decisions

### ✅ Folder Structure
messy-migration-refactored/
```
├── app/
│ ├── init.py # App factory pattern
│ ├── routes.py # Flask route handlers
│ ├── db.py # DB initialization + connection
│ ├── models.py # DB operations
│ └── utils.py # Password helpers
├── init_db.py
├── app.py # Entrypoint
└── requirements.txt
```


### ✅ Architectural Changes
- Adopted **App Factory Pattern** to support better scalability/testing.
- Abstracted DB layer for better separation of concerns and testability.
- Organized logic into reusable functions.

### ✅ Security & Reliability
- Passwords hashed securely.
- SQL injection eliminated.
- Better validation and error messaging.

### ✅ API Behavior
- All endpoints return JSON.
- Consistent HTTP status codes (e.g. 200, 201, 400, 404, 401).

---

## 🤝 Trade-Offs & Assumptions

- No extensive validation libraries were added to stay within scope.
- Did not implement auth tokens (e.g. JWT) since it was out of scope.
- Retained SQLite for simplicity (not production-grade).
- Assumed email is unique for login; no duplication check for email at creation.

---

## 🕒 If I Had More Time
- Add proper validation using libraries like `marshmallow` or `pydantic`.
- Add unit/integration tests using `pytest` and test client.
- Implement error logging and monitoring.
- Implement pagination for `/users`.
- Add email format validation.
- Migrate to SQLAlchemy for ORM support.
- Add authentication (JWT / sessions).

---

## 🤖 AI Usage Declaration
- Tool: ChatGPT-4o
- Purpose: Code guidance, refactoring strategy, implementation templates

---

✅ All changes maintain the original API contract.
✅ To run:
```bash
pip install -r requirements.txt
python init_db.py
python app.py
```
API available at: http://localhost:5009
