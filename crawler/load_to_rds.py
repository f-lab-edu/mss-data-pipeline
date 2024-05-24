from datetime import datetime, timezone, timedelta

from crawler.crawl_musinsa import crawl_goods
from crawler.list_crawler import get_goods_url_from_list_page
from crawler.util.postgresql import manipulate_data
from crawler.util.date import KST_now


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


def create_review_insert_query(goods):
    dt = KST_now()
    queries = []
    for text, url, likes in zip(
        goods["review_content"], goods["review_thumbnail_url"], goods["review_likes"]
    ):
        queries.append(
            f"INSERT INTO review(review_id, goods_id, content, main_thumbnail_url, likes, created_at)"
            f"VALUES(hashtext('{text}'), {goods['goods_id']}, E'{text}', '{url}', {likes}, '{dt}')"
        )

    return queries


if __name__ == "__main__":
    for i in range(1, 22):  # 무신사 사이트의 대분류는 1~21
        category_id = f"0{i}" if i >= 10 else f"00{i}"
        url = f"https://www.musinsa.com/categories/item/{category_id}"
        for goods_url in get_goods_url_from_list_page(url):
            try:
                goods = crawl_goods(goods_url)
            except Exception as e:
                print(e, goods_url)
                continue

            immutable_goods_info_insert_query = (
                create_immutable_goods_info_insert_query(goods)
            )
            mutable_goods_info_insert_query = create_mutable_goods_info_insert_query(
                goods
            )
            review_insert_query = create_review_insert_query(goods)

            manipulate_data(immutable_goods_info_insert_query)
            manipulate_data(mutable_goods_info_insert_query)
            manipulate_data(review_insert_query)
