import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="FIFA API",
    description="API de performance de jogadores FIFA.",
    default_response_class=ORJSONResponse,
)

conn = sqlite3.connect("fifa.db", check_same_thread=False)
conn.row_factory = sqlite3.Row

class Player(BaseModel):
    player_id: int
    player_name: str
    age: int
    nationality: str
    club: str
    position: str
    overall_rating: int
    potential_rating: int
    matches_played: int
    goals: int
    assists: int
    minutes_played: int
    market_value_million_eur: float
    contract_years_left: int
    injury_prone: str
    transfer_risk_level: str

@app.post("/fifa", status_code=201)
def insert_player(p: Player):
    try:
        conn.execute(
            "INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            tuple(p.model_dump().values()),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="player_id já existe")
    return p

@app.get("/fifa/count")
def count():
    n = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    return {"count": n}

@app.get("/fifa")
def get_all():
    return [dict(r) for r in conn.execute("SELECT * FROM players")]

@app.get("/fifa/id/{id}")
def get_by_id(id: int):
    r = conn.execute("SELECT * FROM players WHERE player_id = ?", (id,)).fetchone()
    if not r:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return dict(r)

@app.get("/fifa/nat/{exp}")
def get_by_nat(exp: str):
    rows = conn.execute(
        "SELECT * FROM players WHERE nationality = ? COLLATE NOCASE", (exp,)
    ).fetchall()
    return [dict(r) for r in rows]
