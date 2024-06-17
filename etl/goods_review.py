import os

from crawler.process_goods_html import process_goods_review_html
from util.date import KST_now
from util.postgresql import manipulate_data
from util.s3 import get_s3_connection


def create_review_insert_query(goods):
    dt = KST_now()
    query = f"INSERT INTO review(review_id, goods_id, content, main_thumbnail_url, created_at) VALUES"
    for text, url in zip(goods["review_content"], goods["review_thumbnail_url"]):
        query += (
            f" (hashtext('{text}'), {goods['goods_id']}, E'{text}', '{url}', '{dt}'),"
        )

    return query[:-1]


def process_goods_review(s3, date):
    s3_conn = s3
    response = s3_conn.list_objects_v2(
        Bucket=os.getenv("s3_bucket_name"), Prefix=f"product_review/{date}/"
    )
    if "Contents" in response:
        files = response["Contents"]
        for file in files:
            file_key = file["Key"]
            print(file_key)
            obj = s3_conn.get_object(Bucket=os.getenv("s3_bucket_name"), Key=file_key)
            file_content = obj["Body"].read().decode("utf-8")
            goods_review = process_goods_review_html(file_content)
            goods_review["goods_id"] = file_key.split("/")[2]
            review_insert_query = create_review_insert_query(goods_review)
            manipulate_data(review_insert_query)

    else:
        print("No files found")


if __name__ == "__main__":
    s3 = get_s3_connection()
    process_goods_review(s3, KST_now())
