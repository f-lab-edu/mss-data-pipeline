from dotenv import load_dotenv
import os

import psycopg2


load_dotenv()
db = psycopg2.connect(
    host=os.environ.get("dw_host"),
    dbname=os.environ.get("dw_dbname"),
    user=os.environ.get("dw_user"),
    password=os.environ.get("dw_password"),
    port=os.environ.get("dw_port"),
)
cursor = db.cursor()


def select_data(sql):
    try:
        print(sql)
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(e, sql)


def manipulate_data(sql):
    try:
        print(sql)
        if isinstance(sql, list):
            for query in sql:
                cursor.execute(query)
        else:
            cursor.execute(sql)
    except Exception as e:
        print(e, sql)
    finally:
        db.commit()
