import psycopg2
from datetime import datetime, timezone

from crawler.crawl_musinsa import crawl_goods
from crawler.list_crawler import get_goods_url_from_list_page

db = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="1234", port=5432
)
cursor = db.cursor()


def create_insert_query(goods):
    dt = datetime.now(timezone.utc)
    query = (
        f"INSERT INTO goods(goods_id, name, main_thumbnail_url, regular_price, sale_price, category, sub_category, brand, views_in_recent_month, sales_in_recent_year, likes, star_rating, reviews, created_at) "
        f"VALUES({goods[0]}, '{goods[1]}', '{goods[2]}', {goods[3]}, {goods[4]}, '{goods[5][0]}', '{goods[5][1]}', '{goods[6]}', {goods[7]}, {goods[8]}, {goods[9]}, {goods[10]}, {goods[11]}, '{dt}')"
    )
    return query


for i in range(1, 21):  # 무신사 사이트의 대분류는 1~21
    category_id = f"0{i}" if i >= 10 else f"00{i}"
    url = f"https://www.musinsa.com/categories/item/{category_id}"
    for goods_url in get_goods_url_from_list_page(url):
        goods = crawl_goods(goods_url)
        sql = create_insert_query(goods)
        print(sql)
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e, goods_url)

        db.commit()
