import boto3
from dotenv import load_dotenv
import os
from datetime import datetime, timezone, timedelta

from crawler.crawl_musinsa import (
    get_page_html_from_url,
    get_goods_review,
    get_soup_object_from_html,
)
from crawler.list_crawler import get_goods_url_from_list_page

load_dotenv()


def get_s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name=os.getenv("aws_region"),
            aws_access_key_id=os.getenv("aws_access_key"),
            aws_secret_access_key=os.getenv("aws_secret_key"),
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3


def upload_html_to_s3(s3, html, s3_path):
    try:
        s3.put_object(
            Bucket=os.getenv("s3_bucket_name"),
            Key=s3_path,
            Body=html,
            ContentType="text/html",
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    s3 = get_s3_connection()
    file_path = "temp.html"
    dt = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    for i in range(1, 22):  # 무신사 사이트의 대분류는 1~21
        category_id = f"0{i}" if i >= 10 else f"00{i}"
        url = f"https://www.musinsa.com/categories/item/{category_id}"
        for goods_url in get_goods_url_from_list_page(url):
            print("start crawl goods")
            goods_id = goods_url.split("/")[-1]
            try:
                goods_html = get_page_html_from_url(goods_url)
            except Exception as e:
                print(e, goods_url)
                continue

            soup = get_soup_object_from_html(goods_html)
            upload_html_to_s3(
                s3, soup.prettify(), f"product_detail/{dt}/{goods_id}.html"
            )
            print("start crawl review")
            for review, page_num, review_category in get_goods_review(goods_id):
                upload_html_to_s3(
                    s3,
                    review,
                    f"product_review/{dt}/{goods_id}/{review_category}/{page_num}.html",
                )
