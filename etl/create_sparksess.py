from pyspark.sql import SparkSession


def start_spark(app_name="my_spark_app", master="local[*]"):
    spark = (
        SparkSession.builder.appName(app_name)
        .master(master)
        .config("spark.jars", "/Users/humanlearning/Downloads/postgresql-42.7.3.jar")
        .getOrCreate()
    )

    return spark
