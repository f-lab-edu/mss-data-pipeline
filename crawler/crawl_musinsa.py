import requests
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from util.postgresql import select_data, manipulate_data
from util.date import subtract_date, KST_now


def get_page_html_from_url(url):
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("--headless")
    chrome_option.add_argument("--no-sandbox")
    chrome_option.add_argument("--disable-dev-shm-usage")
    chrome_option.add_argument(f'--user-agent={user_agent["User-Agent"]}')
    chrome_option.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_option)
    browser.get(url)
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.ID, "wrap-estimate-list"))
    )

    html = browser.page_source
    browser.quit()

    return html


def get_soup_object_from_html(html):
    soup = BeautifulSoup(html, "lxml")

    return soup


def get_goods_review(goods_id):
    for i, category in enumerate(["style", "photo", "goods"], 1):
        page_num = 0

        most_recently_created_review = select_data(
            f"select * from most_recently_posted_review \
              where goods_id ={goods_id}"
        )
        if most_recently_created_review:
            most_recently_created_review = most_recently_created_review[0][i]
        else:  # 처음보는 상품일경우
            most_recently_created_review = datetime.strptime(
                "1990-01-01", "%Y-%m-%d"
            ).date()
            manipulate_data(
                f"insert into most_recently_posted_review \
                  values ({goods_id}, '{most_recently_created_review}', '{most_recently_created_review}', '{most_recently_created_review}')"
            )
        first_comment_date = most_recently_created_review  #
        while True:
            page_num += 1
            url = f"https://goods.musinsa.com/api/goods/v2/review/{category}/list?similarNo={goods_id}&sort=new&selectedSimilarNo={goods_id}&page={page_num}&goodsNo={goods_id}"
            reviews = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
                },
            )

            reviews = reviews.text
            reviews = get_soup_object_from_html(reviews)
            is_no_review = reviews.find("p", class_="review-list--none__text")
            if is_no_review:  # 후기가 없는 페이지일 경우
                manipulate_data(
                    f"update most_recently_posted_review \
                      set {category} = '{first_comment_date}' \
                      where goods_id = {goods_id}"
                )
                break

            created_at = reviews.find("p", class_="review-profile__date").text
            if created_at is None:
                yield reviews.prettify(), page_num, category
                break

            if created_at[-1] == "전":
                today = KST_now()
                if "시간" in created_at:
                    created_at = subtract_date(today, 1)
                else:
                    if created_at[1] == "일":
                        created_at = subtract_date(today, created_at[0])
                    else:
                        created_at = subtract_date(today, created_at[:2])
            else:
                created_at = datetime.strptime(created_at, "%Y.%m.%d")

            created_at = created_at.date()
            if created_at <= most_recently_created_review:
                manipulate_data(
                    f"update most_recently_posted_review \
                      set {category} = '{first_comment_date}' \
                      where goods_id = {goods_id}"
                )
                break
            else:  # 크롤링한 댓글이 더 최신일 경우
                if page_num == 1:  # 첫 페이지의 날짜로 업데이트 되게끔
                    first_comment_date = created_at

            yield reviews.prettify(), page_num, category
