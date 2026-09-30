import sqlite3
import pandas as pd

conn = sqlite3.connect("business_data.db")
for name in pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)["name"]:
    print(f"--- {name} ---")
    print(pd.read_sql(f"SELECT * FROM {name} LIMIT 5", conn))
conn.close()