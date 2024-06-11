import os

from util.date import KST_now
from util.postgresql import manipulate_data
from util.s3 import get_s3_connection
from crawler.process_goods_html import process_goods_info_html


def create_immutable_goods_info_insert_query(goods):
    dt = KST_now()
    query = (
        f"INSERT INTO immutable_goods_info(goods_id, name, main_thumbnail_url, regular_price, category, sub_category, brand, created_at) "
        f"VALUES({goods['goods_id']}, '{goods['name']}', '{goods['thumbnail_url']}', {goods['regular_price']}, '{goods['category'][0]}', '{goods['category'][1]}', '{goods['brand']}', '{dt}')"
    )
    return query


def create_mutable_goods_info_insert_query(goods):
    dt = KST_now()
    query = (
        f"INSERT INTO mutable_goods_info(goods_id, sale_price, views_in_recent_month, sales_in_recent_year, likes, star_rating, reviews, created_at) "
        f"VALUES({goods['goods_id']}, {goods['sale_price']}, {goods['views']}, {goods['sales']}, {goods['likes']}, {goods['star_rating']}, {goods['reviews']}, '{dt}')"
    )
    return query


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
        goods_info = process_goods_info_html(file_content)
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
