import psycopg2
from datetime import datetime, timezone

db = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5433
)
cursor = db.cursor()

dt = datetime.now(timezone.utc)
sql = f"insert into goods values(2, 'test', 'test', 100, 10, 'test', 'test', 100, 100, 100, 100, 100, '{dt}')"
cursor.execute(sql)
db.commit()
