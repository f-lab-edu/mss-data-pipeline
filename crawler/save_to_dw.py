from dotenv import load_dotenv
import os

import psycopg2
from datetime import datetime, timezone, timedelta

from crawler.crawl_musinsa import crawl_goods
from crawler.list_crawler import get_goods_url_from_list_page


load_dotenv()
db = psycopg2.connect(
    host=os.environ.get("dw_host"),
    dbname=os.environ.get("dw_dbname"),
    user=os.environ.get("dw_user"),
    password=os.environ.get("dw_password"),
    port=os.environ.get("dw_port"),
)
cursor = db.cursor()


def create_immutable_goods_info_insert_query(goods):
    dt = datetime.now(timezone(timedelta(hours=9)))
    query = (
        f"INSERT INTO immutable_goods_info(goods_id, name, main_thumbnail_url, regular_price, category, sub_category, brand, created_at) "
        f"VALUES({goods['goods_id']}, '{goods['name']}', '{goods['thumbnail_url']}', {goods['regular_price']}, '{goods['category'][0]}', '{goods['category'][1]}', '{goods['brand']}', '{dt}')"
    )
    return query


def create_mutable_goods_info_insert_query(goods):
    dt = datetime.now(timezone(timedelta(hours=9)))
    query = (
        f"INSERT INTO mutable_goods_info(goods_id, sale_price, views_in_recent_month, sales_in_recent_year, likes, star_rating, reviews, created_at) "
        f"VALUES({goods['goods_id']}, {goods['sale_price']}, {goods['views']}, {goods['sales']}, {goods['likes']}, {goods['star_rating']}, {goods['reviews']}, '{dt}')"
    )
    return query


def call_db(sql):
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e, goods_url)


for i in range(1, 22):  # 무신사 사이트의 대분류는 1~21
    category_id = f"0{i}" if i >= 10 else f"00{i}"
    url = f"https://www.musinsa.com/categories/item/{category_id}"
    for goods_url in get_goods_url_from_list_page(url):
        try:
            goods = crawl_goods(goods_url)
        except Exception as e:
            print(e, goods_url)
            continue

        immutable_goods_info_insert_query = create_immutable_goods_info_insert_query(
            goods
        )
        mutable_goods_info_insert_query = create_mutable_goods_info_insert_query(goods)
        print(immutable_goods_info_insert_query)
        print(mutable_goods_info_insert_query)

        call_db(immutable_goods_info_insert_query)
        call_db(mutable_goods_info_insert_query)
