# ⚙️ NoteVault Backend — FastAPI REST API

A production-ready, modular REST API built with **FastAPI**, **MongoDB**, and **JWT Authentication**, following clean architecture principles and API best practices.

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py         # Environment-based settings (pydantic-settings)
│   │   └── security.py       # JWT token creation & bcrypt password hashing
│   ├── database/
│   │   └── mongodb.py        # Motor async MongoDB client
│   ├── models/
│   │   ├── user.py           # User DB model
│   │   └── note.py           # Note DB model
│   ├── schemas/
│   │   ├── user.py           # Pydantic schemas for User requests/responses
│   │   └── note.py           # Pydantic schemas for Note requests/responses
│   ├── services/
│   │   ├── user_service.py   # User business logic (create, authenticate)
│   │   └── note_service.py   # Note business logic (CRUD)
│   ├── routes/
│   │   ├── auth.py           # /api/v1/auth/* endpoints
│   │   └── notes.py          # /api/v1/notes/* endpoints
│   ├── utils/
│   │   └── dependencies.py   # get_current_user dependency guard
│   └── main.py               # FastAPI app entry point, CORS, lifespan
├── .env                      # Environment variables (not committed to git)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- MongoDB (local `mongod` or [MongoDB Atlas](https://cloud.mongodb.com/))

### 1. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
MONGO_URL=mongodb://localhost:27017
# OR for MongoDB Atlas:
# MONGO_URL=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/

DB_NAME=notes_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload
```

Server starts at: **http://127.0.0.1:8000**

---

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Reference

### 🔐 Authentication — `/api/v1/auth`

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| `POST` | `/register` | `{username, email, password}` | Register new user |
| `POST` | `/login` | `{username, password}` | Login, returns access + refresh tokens |
| `POST` | `/refresh` | `{refresh_token}` | Get a new access token |

**Login Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### 📋 Notes — `/api/v1/notes` *(JWT Required)*

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| `GET` | `/` | Auth | Get all notes (admin sees all users' notes) |
| `POST` | `/` | Auth | Create a note |
| `PUT` | `/{note_id}` | Owner | Update a note |
| `DELETE` | `/{note_id}` | Owner / Admin | Delete a note |

**Create Note Body:**
```json
{
  "title": "My Note Title",
  "content": "Note content here"
}
```

**Note Response:**
```json
{
  "_id": "65f...",
  "title": "My Note Title",
  "content": "Note content here",
  "owner_id": "65e...",
  "created_at": "2026-03-14T10:30:00"
}
```

---

## 🔐 Authentication Flow

```
Client                       Server
  |                             |
  |-- POST /auth/register ----> |  Hash password (bcrypt), store user
  |<-- 201 Created ------------ |
  |                             |
  |-- POST /auth/login -------> |  Verify password, issue JWT pair
  |<-- {access_token, ...} ---- |
  |                             |
  |-- GET /notes/ ------------>  |  Bearer token validated via dependency
  |   Authorization: Bearer ... |
  |<-- [notes array] ---------- |
```

---

## 👥 Role-Based Access

| Role | Permissions |
|------|------------|
| `user` | CRUD on **own** notes only |
| `admin` | Read/Delete **all** notes from all users |

Set role manually in MongoDB or create an admin endpoint.

---

## 🧰 Tech Stack & Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `motor` | Async MongoDB driver |
| `pymongo` | MongoDB utilities |
| `python-jose[cryptography]` | JWT encoding/decoding |
| `bcrypt` | Password hashing |
| `pydantic` + `pydantic-settings` | Schema validation & config |
| `python-multipart` | Form data support |
| `email-validator` | Email field validation |
| `python-dotenv` | `.env` file loading |

---

## 🗄️ Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "username": "string (unique)",
  "email": "string (unique)",
  "hashed_password": "string",
  "role": "user | admin",
  "created_at": "datetime"
}
```

### Notes Collection
```json
{
  "_id": "ObjectId",
  "title": "string",
  "content": "string",
  "owner_id": "string (ref: Users._id)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

---

## 📌 Scalability Considerations

- **Async First**: All database operations use `motor` (async), enabling thousands of concurrent requests
- **Modular Services**: Each domain (auth, notes) is isolated into its own service — easy to extract as a microservice
- **Config-Driven**: All environment values loaded via `pydantic-settings`, ready for Docker/Kubernetes environments
- **Stateless Auth**: JWT-based auth scales horizontally — any server can validate tokens
- **Redis Caching** *(optional)*: Add a Redis layer in `note_service.py` to cache popular notes queries