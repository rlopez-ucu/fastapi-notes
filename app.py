from fastapi import FastAPI
from pathlib import Path

app = FastAPI(title="Notes API")

DATA_DIR = Path("/data")
NOTES_FILE = DATA_DIR / "notes.txt"


@app.on_event("startup")
def ensure_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_FILE.touch(exist_ok=True)


@app.get("/")
def root():
    return {"message": "The API is up and running"}


@app.get("/add/{note}")
def add_note(note: str):
    with NOTES_FILE.open("a", encoding="utf-8") as f:
        f.write(note + "\n")
    return {"message": "Note added", "note": note}


@app.get("/list")
def list_notes():
    with NOTES_FILE.open("r", encoding="utf-8") as f:
        notes = [line.strip() for line in f if line.strip()]
    return {"count": len(notes), "notes": notes}