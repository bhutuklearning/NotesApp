# 🎨 NoteVault Frontend — React.js Application

A modern, premium-designed React.js frontend for the NoteVault Notes CRUD application. Features JWT authentication, protected routing, and a polished glassmorphism UI.

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   └── axios.js          # Axios instance with JWT interceptor
│   ├── components/
│   │   ├── NoteForm.jsx       # Create / Edit note form
│   │   └── ProtectedRoute.jsx # JWT-guarded route wrapper
│   ├── context/
│   │   └── AuthContext.jsx    # Global authentication state (React Context)
│   ├── pages/
│   │   ├── Login.jsx          # Login page
│   │   ├── Register.jsx       # Registration page
│   │   ├── Dashboard.jsx      # Main notes dashboard
│   │   ├── Auth.css           # Shared auth page styles
│   │   └── Dashboard.css      # Dashboard styles
│   ├── App.jsx                # Router & route definitions
│   └── main.jsx               # React app entry point
├── .env                       # Environment variables
├── index.html
├── vite.config.js
└── package.json
```

---

## 🚀 Getting Started

### Prerequisites
- **Node.js 18+** and **npm**
- Backend server running at `http://localhost:8000` (see [backend/README.md](../backend/README.md))

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Start the Dev Server
```bash
npm run dev
```

App starts at: **http://localhost:5173**

---

## 🌐 Pages & Routes

| Route | Component | Access | Description |
|-------|-----------|--------|-------------|
| `/login` | `Login.jsx` | Public | User login form |
| `/register` | `Register.jsx` | Public | New user registration |
| `/` | `Dashboard.jsx` | 🔒 Protected | Notes CRUD dashboard |

Unauthenticated users are automatically redirected to `/login` by `ProtectedRoute`.

---

## 🔐 Authentication Flow

1. User registers via `/register` → redirected to `/login`
2. User logs in via `/login` → receives JWT access + refresh tokens
3. Tokens are stored in `localStorage`
4. `AuthContext` decodes the token and stores `user` state globally
5. Axios interceptor attaches `Authorization: Bearer <token>` to every request
6. `ProtectedRoute` checks for valid user session before rendering pages
7. On logout, tokens are cleared and user is redirected to `/login`

---

## 🎨 Design System

The UI follows a **glassmorphism dark theme** with animated gradients:

- **Background**: Animated multi-stop gradient (`#0f0c29` → `#302b63` → `#24243e`)
- **Cards**: Frosted glass effect using `backdrop-filter: blur(16px)` with subtle borders
- **Accent Colors**: Orange-to-pink gradient (`#8A2387` → `#E94057` → `#F27121`)
- **Typography**: `Inter` / System UI sans-serif
- **Animations**: Slide-up on mount, shake on error, gradient loop

---

## 🧩 Key Components

### `AuthContext`
Provides global `user`, `login()`, `register()`, and `logout()` functions to all components via React Context API. Reads JWT from `localStorage` on load.

### `api/axios.js`
Pre-configured Axios instance with:
- `baseURL` set from `VITE_API_URL`
- Request interceptor that automatically injects the JWT bearer token

### `ProtectedRoute`
HOC wrapper that checks if a user is authenticated. Redirects unauthenticated users to `/login`.

### `NoteForm`
Dual-purpose form that handles both creating new notes and editing existing ones, driven by the `currentNote` prop.

---

## 🧰 Tech Stack

| Package | Purpose |
|---------|---------|
| `react` + `react-dom` | UI library |
| `vite` | Build tool & dev server |
| `react-router-dom` | Client-side routing |
| `axios` | HTTP client with interceptors |
| `jwt-decode` | Decode JWT for user info |

---

## 📜 Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server with HMR |
| `npm run build` | Build for production (outputs to `dist/`) |
| `npm run preview` | Preview the production build |
| `npm run lint` | Run ESLint |
