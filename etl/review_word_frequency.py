from dotenv import load_dotenv
from os import getenv

import psycopg2
from psycopg2.extras import execute_values

from pyspark.sql.functions import explode, split, count

from etl.create_sparksess import start_spark


def extract_data(spark, table_name):
    load_dotenv()
    df = (
        spark.read.format("jdbc")
        .option(
            "url",
            f"jdbc:postgresql://{getenv('dw_host')}/{getenv('dw_dbname')}",
        )
        .option("driver", "org.postgresql.Driver")
        .option("query", f"select * from {table_name}")
        .option("user", f"{getenv('dw_user')}")
        .option("password", f"{getenv('dw_password')}")
        .load()
    )

    return df


def transform_data(df):
    words = df.select(
        "goods_id", explode(split("content", "\\s+")).alias("word")
    ).filter("word is not null and content is not null")
    word_counts = words.groupBy("goods_id", "word").agg(count("*").alias("word_count"))

    return word_counts


def load_data(rows):
    load_dotenv()
    conn = psycopg2.connect(
        host=getenv("dw_host"),
        dbname=getenv("dw_dbname"),
        user=getenv("dw_user"),
        password=getenv("dw_password"),
        port=getenv("dw_port"),
    )

    try:
        cursor = conn.cursor()
        sql = """
                INSERT INTO review_word_frequency (goods_id, word, count)
                VALUES %s
                ON CONFLICT (goods_id, word) 
                DO UPDATE SET 
                    count = EXCLUDED.count + review_word_frequency.count;
                """
        batch_size = 100
        batch = []

        for row in rows:
            batch.append((row.goods_id, row.word, row.word_count))
            if len(batch) >= batch_size:
                execute_values(cursor, sql, batch)
                conn.commit()
                batch = []

        if batch:
            execute_values(cursor, sql, batch)
            conn.commit()

    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def main():
    spark = start_spark()
    review = extract_data(spark, "review")

    df = transform_data(review)
    df.foreachPartition(load_data)


if __name__ == "__main__":
    main()
