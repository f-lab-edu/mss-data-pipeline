import os

from crawler.load_to_rds import (
    create_immutable_goods_info_insert_query,
    create_mutable_goods_info_insert_query,
)
from util.date import KST_now
from util.postgresql import manipulate_data
from util.s3 import get_s3_connection
from crawler.process_goods_html import process_goods_html


s3 = get_s3_connection()
response = s3.list_objects_v2(
    Bucket=os.getenv("s3_bucket_name"), Prefix=f"product_detail/{KST_now()}/"
)
if "Contents" in response:
    files = response["Contents"]
    for file in files:
        file_key = file["Key"]
        print(file_key)
        obj = s3.get_object(Bucket=os.getenv("s3_bucket_name"), Key=file_key)
        file_content = obj["Body"].read().decode("utf-8")
        goods_info = process_goods_html(file_content)
        goods_info["goods_id"] = file_key.split("/")[-1].split(".")[0]
        immutable_goods_info_insert_query = create_immutable_goods_info_insert_query(
            goods_info
        )
        mutable_goods_info_insert_query = create_mutable_goods_info_insert_query(
            goods_info
        )

        manipulate_data(immutable_goods_info_insert_query)
        manipulate_data(mutable_goods_info_insert_query)


else:
    print("No files found")
