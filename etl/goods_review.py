import os

from crawler.load_to_rds import create_review_insert_query
from crawler.process_goods_html import process_goods_review_html
from util.date import KST_now
from util.postgresql import manipulate_data
from util.s3 import get_s3_connection


s3 = get_s3_connection()
response = s3.list_objects_v2(
    Bucket=os.getenv("s3_bucket_name"), Prefix=f"product_review/{KST_now()}/"
)
if "Contents" in response:
    files = response["Contents"]
    for file in files:
        file_key = file["Key"]
        print(file_key)
        obj = s3.get_object(Bucket=os.getenv("s3_bucket_name"), Key=file_key)
        file_content = obj["Body"].read().decode("utf-8")
        goods_review = process_goods_review_html(file_content)
        goods_review["goods_id"] = file_key.split("/")[2]
        review_insert_query = create_review_insert_query(goods_review)
        manipulate_data(review_insert_query)

else:
    print("No files found")