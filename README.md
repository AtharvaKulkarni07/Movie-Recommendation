# 🎬 CineMatch - Movie Recommendation System

A full-stack movie recommendation web application powered by **FastAPI** (using a Markov Chain / transition-probability recommendation engine on the TMDB 5000 dataset) and **React (Vite)** with **The Movie Database (TMDB) API** for real-time movie posters, backdrops, ratings, and details.

---

## 📁 Project Structure

```text
Movie-Recommendation/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── data_loader.py    # Loads & preprocesses TMDB 5000 dataset
│   │   ├── recommender.py    # Markov Chain recommendation engine
│   │   └── main.py           # FastAPI endpoints & CORS
│   ├── data/
│   │   └── tmdb_5000_movies.csv
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/       # MovieCard, SearchBar, etc.
│   │   ├── services/
│   │   │   ├── api.js        # FastAPI client
│   │   │   └── tmdb.js       # TMDB API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env.example          # Sample environment variables
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🔑 Where & How to Add the TMDB API Key

The TMDB API is consumed directly by the **frontend** ([`frontend/src/services/tmdb.js`](file:///d:/Movie-Recommendation/frontend/src/services/tmdb.js)) using Bearer Token authorization.

### 1. Get your TMDB API Token
1. Create a free account at [themoviedb.org](https://www.themoviedb.org/).
2. Navigate to **Settings** > [**API**](https://www.themoviedb.org/settings/api).
3. Request an API key (developer / personal use).
4. Copy the **API Read Access Token (v4 auth)** (this is a long alphanumeric JWT token, distinct from the short v3 API key).

### 2. Configure in Frontend
1. In the `frontend/` folder, create a `.env` file (you can copy [`.env.example`](file:///d:/Movie-Recommendation/frontend/.env.example)):
   ```bash
   cd frontend
   cp .env.example .env
   ```
2. Open `frontend/.env` and paste your token:
   ```env
   VITE_TMDB_READ_ACCESS_TOKEN=your_actual_tmdb_read_access_token_here
   VITE_API_BASE_URL=http://127.0.0.1:8000
   ```
3. Restart the Vite development server if it was already running so Vite loads the new environment variables.

---

## 🚀 Setup & Execution Guide

### 1. Backend Setup (FastAPI)

1. Open a terminal and navigate to `backend`:
   ```bash
   cd backend
   ```
2. (Recommended) Create and activate a virtual environment:
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
5. Verify the backend is running by opening:
   - API Welcome: `http://127.0.0.1:8000/`
   - Interactive Swagger Docs: `http://127.0.0.1:8000/docs`

---

### 2. Frontend Setup (React + Vite)

1. Open a second terminal and navigate to `frontend`:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Ensure `.env` is created with your `VITE_TMDB_READ_ACCESS_TOKEN`.
4. Start the Vite development server:
   ```bash
   npm run dev
   ```
5. Open your browser at `http://localhost:5173`.

---

## 🛠️ Tech Stack & Remaining Steps

| Component | Technologies |
|---|---|
| **Frontend** | React, Vite, Lucide Icons, Vanilla CSS |
| **Backend** | FastAPI, Uvicorn, Pandas |
| **Data & Algorithm** | TMDB 5000 Movies Dataset, Markov Chain Genre/Feature Transitions |
| **External APIs** | TMDB REST API v3/v4 (Posters, Backdrops, Movie Details) |

### Remaining Things / Next Steps Checklist
- [x] Create `frontend/.env.example` template.
- [x] Create root [`README.md`](file:///d:/Movie-Recommendation/README.md) with complete setup instructions.
- [ ] Create `frontend/.env` and paste your TMDB Read Access Token.
- [ ] Run both the FastAPI backend (`uvicorn app.main:app --reload`) and React frontend (`npm run dev`).
