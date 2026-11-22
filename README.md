# Decision Log

A small web app for recording team decisions in writing: what was decided, why,
and what replaced it later. Decisions are never deleted, only superseded, so
the history stays readable.

Built with Python (FastAPI, SQLite) and React (Vite).

## Run it locally

Backend (terminal 1):

    cd backend
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    uvicorn app.main:app --reload

Frontend (terminal 2):

    cd frontend
    npm install
    npm run dev

Open http://localhost:5173. API docs are at http://127.0.0.1:8000/docs.

## Run the tests

    cd backend
    python -m pytest

## API

| Method | Path | What it does |
|---|---|---|
| GET | /health | Check the API is alive |
| GET | /decisions | List decisions, newest first |
| POST | /decisions | Create a decision |
| GET | /decisions/{id} | Get one decision |
| PATCH | /decisions/{id}/status | Switch between proposed and accepted |
| POST | /decisions/{id}/supersede | Replace a decision with a new one |

## How it is organised

- `backend/app/main.py`: endpoints and the rules (404, 409)
- `backend/app/schemas.py`: input and output validation
- `backend/app/database.py`: SQLite connection and table
- `backend/tests`: tests for every endpoint
- `frontend/src`: React components and one API file
- `docs/decisions`: why I made the main choices

## What I would do next

- Search and filtering
- Database migrations instead of creating the table on connect
- Authentication