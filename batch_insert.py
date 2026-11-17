import csv, requests, time

URL = "http://177.44.248.56:8000/fifa"
HEADERS = {}  # se ativar autenticação: {"X-API-Key": "sua-chave"}

with open("fifa_player_performance_market_value.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

inicio = 20000
t = time.time()
ok = 0
for i, r in enumerate(rows[:100]):
    r["player_id"] = inicio + i
    resp = requests.post(URL, json=r, headers=HEADERS)
    if resp.status_code == 201:
        ok += 1
    else:
        print("Erro:", resp.status_code, resp.text)
print(f"Inseridos {ok} em {round(time.time() - t, 2)}s")
