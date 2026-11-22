from fastapi import FastAPI, HTTPException

from app.database import get_connection
from app.schemas import Decision, DecisionCreate

app = FastAPI(title="Decision Log")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/decisions", response_model=Decision, status_code=201)
def create_decision(payload: DecisionCreate):
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO decisions (title, context, decision, status) "
            "VALUES (?, ?, ?, ?)",
            (payload.title, payload.context, payload.decision, payload.status),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM decisions WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    finally:
        conn.close()
    return dict(row)


@app.get("/decisions", response_model=list[Decision])
def list_decisions():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM decisions ORDER BY id DESC").fetchall()
    finally:
        conn.close()
    return [dict(row) for row in rows]


@app.get("/decisions/{decision_id}", response_model=Decision)
def get_decision(decision_id: int):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM decisions WHERE id = ?", (decision_id,)
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Decision not found")
    return dict(row)