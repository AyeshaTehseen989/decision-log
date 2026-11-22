from fastapi import FastAPI

app = FastAPI(title="Decision Log")


@app.get("/health")
def health():
    return{"status": "ok"}