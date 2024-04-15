from dotenv import load_dotenv
from os import getenv

from pyspark.ml.feature import Bucketizer
from pyspark.sql.functions import col, date_trunc, explode, split, count

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
    words = df.select(
        "goods_id", explode(split("content", "\\s+")).alias("word")
    ).filter("word is not null and content is not null")
    word_counts = words.groupBy("goods_id", "word").agg(count("*").alias("count"))

    return word_counts


def load_data(df):
    load_dotenv()
    df.write.format("jdbc").option(
        "url", f"jdbc:postgresql://{getenv('dw_host')}/{getenv('dw_dbname')}"
    ).option("driver", "org.postgresql.Driver").option(
        "dbtable", "review_word_frequency"
    ).option(
        "user", f"{getenv('dw_user')}"
    ).option(
        "password", f"{getenv('dw_password')}"
    ).mode(
        "append"
    ).save()


def main():
    spark = start_spark()
    review = extract_data(spark, "review")

    df = transform_data(review)
    load_data(df)


if __name__ == "__main__":
    main()
