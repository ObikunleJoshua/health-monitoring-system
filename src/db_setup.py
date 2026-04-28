import sqlite3

conn = sqlite3.connect("health_monitoring.db")
cursor = conn.cursor()

with open("sql/schema.sql", "r") as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()

print("Database created successfully.")