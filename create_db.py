import csv, sqlite3, os

DB = "fifa.db"
CSV = "fifa_player_performance_market_value.csv"

if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
conn.execute("""
CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT,
    age INTEGER,
    nationality TEXT,
    club TEXT,
    position TEXT,
    overall_rating INTEGER,
    potential_rating INTEGER,
    matches_played INTEGER,
    goals INTEGER,
    assists INTEGER,
    minutes_played INTEGER,
    market_value_million_eur REAL,
    contract_years_left INTEGER,
    injury_prone TEXT,
    transfer_risk_level TEXT
)""")

with open(CSV, newline="", encoding="utf-8") as f:
    rows = [tuple(r.values()) for r in csv.DictReader(f)]

conn.executemany("INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
conn.execute("CREATE INDEX idx_nat ON players(nationality COLLATE NOCASE)")
conn.commit()
print("Inseridos:", conn.execute("SELECT COUNT(*) FROM players").fetchone()[0])
conn.close()
