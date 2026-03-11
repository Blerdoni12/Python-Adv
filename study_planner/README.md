# Study Planner System

A production-ready study planner built with FastAPI, Streamlit, SQLite, and Pydantic. It includes authentication, study plan management, session tracking, analytics, recommendations, and a resource scraper.

## Project Structure
- `app/` FastAPI backend
- `frontend/` Streamlit UI
- `database/` SQLite database file
- `logs/` application logs

## Setup

```bash
cd study_planner
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Environment
Update `.env` with a strong `JWT_SECRET` before running. Adjust `API_BASE_URL` if the backend runs on a different host or port.

## Run Backend

```bash
cd study_planner
uvicorn app.main:app --reload
```

## Run Frontend

```bash
cd study_planner
streamlit run frontend/streamlit_app.py
```

## API Endpoints (Summary)
- `POST /register`
- `POST /login`
- `GET /plans` `POST /plans` `PUT /plans/{id}` `DELETE /plans/{id}`
- `GET /sessions` `POST /sessions`
- `GET /analytics`
- `GET /recommendations`
- `GET /resources?topic=...`
