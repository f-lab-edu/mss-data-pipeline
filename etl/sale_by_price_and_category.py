from dotenv import load_dotenv
from os import getenv

import psycopg2
from psycopg2.extras import execute_values

from pyspark.ml.feature import Bucketizer
from pyspark.sql.functions import col

from create_sparksess import start_spark


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
    bucketizer = Bucketizer(
        splits=[x for x in range(0, 1000001, 10000)] + [float("inf")],
        inputCol="sale_price",
        outputCol="price_range",
    )

    df_with_bins = bucketizer.transform(df)
    df_with_bins = df_with_bins.withColumn(
        "price_range", col("price_range").cast("int")
    )
    sales_by_price_and_category = df_with_bins.drop("sale_price")

    return sales_by_price_and_category


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
            INSERT INTO sales_by_price_and_category (goods_id, category, sales, price_range)
            VALUES %s
            ON CONFLICT (goods_id, price_range) 
            DO UPDATE SET 
                category = EXCLUDED.category,
                sales = EXCLUDED.sales;
            """
        batch_size = 100
        batch = []

        for row in rows:
            batch.append((row.goods_id, row.category, row.sales, row.price_range))
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
    immut = extract_data(spark, "immutable_goods_info")
    mut = extract_data(spark, "mutable_goods_info")
    immut_trimmed = immut.select("goods_id", "category", "regular_price")
    mut_trimmed = mut.select(
        "goods_id", "sales_in_recent_year", "sale_price", "created_at"
    ).dropna(subset=["sales_in_recent_year"])

    goods_joined = (
        immut_trimmed.join(
            mut_trimmed, immut_trimmed["goods_id"] == mut_trimmed["goods_id"], "left"
        )
        .select(
            mut_trimmed["goods_id"],
            "category",
            "sale_price",
            col("sales_in_recent_year").alias("sales"),
        )
        .dropna(subset=["sales"])
    )

    df = transform_data(goods_joined)
    distinct_df = df.drop_duplicates(["goods_id", "price_range"])
    distinct_df.foreachPartition(load_data)


if __name__ == "__main__":
    main()
