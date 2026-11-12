import pandas as pd
import redis
df = pd.read_excel("data_УК.xlsx")
df["Выдано предписаний"] = pd.to_numeric(df["Выдано предписаний"], errors="coerce").fillna(0)
df["Сумма штрафа (тыс. руб.)"] = pd.to_numeric(df["Сумма штрафа (тыс. руб.)"], errors="coerce").fillna(0)
df = df[df["Выдано предписаний"] > 10]
print("Строк после фильтра:", len(df))
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
for _, row in df.iterrows():
    key = "org:" + str(row["Год"]) + ":" + str(row["Наименование управляющей организации, жилищного объединения"])
    r.hset(key, mapping={
        "Выдано предписаний": int(row["Выдано предписаний"]),
        "Сумма штрафа": float(row["Сумма штрафа (тыс. руб.)"]),
    })
  print("Всего ключей в Redis:", r.dbsize())
keys = r.keys("org:*")
print("\nПример:")
for k in keys[:5]:
    print(k, "->", r.hgetall(k))
