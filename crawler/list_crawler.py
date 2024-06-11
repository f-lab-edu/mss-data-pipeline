import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def get_goods_url_from_list_page(list_page_url):
    response = get_page_html_from_url(list_page_url)
    soup = BeautifulSoup(response, "lxml")

    links = soup.find_all("a", {"class": "category__sc-rb2kzk-7 ksmIyr"})

    for link in links:
        yield link.get("href")


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

    html = browser.page_source
    browser.quit()

    return html
