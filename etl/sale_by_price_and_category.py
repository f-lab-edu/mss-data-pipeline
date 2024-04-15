from dotenv import load_dotenv
from os import getenv

from pyspark.ml.feature import Bucketizer
from pyspark.sql.functions import col, date_trunc

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

    return df_with_bins


def load_data(df):
    load_dotenv()
    df.write.format("jdbc").option(
        "url", f"jdbc:postgresql://{getenv('dw_host')}/{getenv('dw_dbname')}"
    ).option("driver", "org.postgresql.Driver").option(
        "dbtable", "sales_by_price_and_category"
    ).option(
        "user", f"{getenv('dw_user')}"
    ).option(
        "password", f"{getenv('dw_password')}"
    ).mode(
        "append"
    ).save()


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
            "regular_price",
            "sale_price",
            "sales_in_recent_year",
            date_trunc("hour", "created_at").alias("created_at"),
        )
        .dropna(subset=["sales_in_recent_year"])
    )

    df = transform_data(goods_joined)
    load_data(df)


if __name__ == "__main__":
    main()
