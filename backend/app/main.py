from fastapi import FastAPI, HTTPException

from app.database import get_connection
from app.schemas import Decision, DecisionCreate, StatusUpdate

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

@app.patch("/decisions/{decision_id}/status", response_model=Decision)
def update_status(decision_id: int, payload: StatusUpdate):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM decisions WHERE id = ?", (decision_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Decision not found")
        if row["status"] == "superseded":
            raise HTTPException(
                status_code=409, detail="A superseded decision cannot change status"
            )
        conn.execute(
            "UPDATE decisions SET status = ? WHERE id = ?",
            (payload.status, decision_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM decisions WHERE id = ?", (decision_id,)
        ).fetchone()
    finally:
        conn.close()
    return dict(row)


@app.post(
    "/decisions/{decision_id}/supersede", response_model=Decision, status_code=201
)
def supersede_decision(decision_id: int, payload: DecisionCreate):
    conn = get_connection()
    try:
        old = conn.execute(
            "SELECT * FROM decisions WHERE id = ?", (decision_id,)
        ).fetchone()
        if old is None:
            raise HTTPException(status_code=404, detail="Decision not found")
        if old["status"] == "superseded":
            raise HTTPException(
                status_code=409, detail="Decision is already superseded"
            )
        cursor = conn.execute(
            "INSERT INTO decisions (title, context, decision, status) "
            "VALUES (?, ?, ?, 'accepted')",
            (payload.title, payload.context, payload.decision),
        )
        new_id = cursor.lastrowid
        conn.execute(
            "UPDATE decisions SET status = 'superseded', superseded_by = ? "
            "WHERE id = ?",
            (new_id, decision_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM decisions WHERE id = ?", (new_id,)
        ).fetchone()
    finally:
        conn.close()
    return dict(row)