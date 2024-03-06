from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://www.musinsa.com/app/goods/2990274"

user_agent = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}
chrome_option = webdriver.ChromeOptions()
# chrome_option.add_argument("headless")
chrome_option.add_argument(f'--user-agent={user_agent["User-Agent"]}')
chrome_option.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_option)
browser.get(url)
html = browser.page_source
browser.quit()

soup = BeautifulSoup(html, "html.parser")
goods_detail = soup.find("div", attrs={"class": "product-detail__sc-8631sn-1 fPAiGD"})
goods_info = goods_detail.find(
    "ul", attrs={"class": "product-detail__sc-achptn-1 VIWAI"}
).find_all("li", attrs={"class": "product-detail__sc-achptn-2 idPepF"})
review = soup.find("div", attrs={"class": "review-list-wrap"}).find_all(
    "div", attrs={"class": "review-list"}
)


def get_goods_name():
    name = soup.find("h3", attrs={"class": "product-detail__sc-1klhlce-3 fitNPd"})
    name = name.get_text()
    return name


def get_goods_thumbnail_url():
    img_url = goods_detail.find(
        "img", attrs={"class": "product-detail__sc-p62agb-9 cXcZGv"}
    )


def get_goods_regular_price():
    regular_price = goods_detail.find(
        "span", attrs={"class": "product-detail__sc-1p1ulhg-7 JZAP"}
    )


def get_goods_sale_price():
    sale_price = goods_detail.find(
        "span", attrs={"class": "product-detail__sc-1p1ulhg-7 kijFAA"}
    )


def get_goods_category():
    category = soup.find("a", attrs={"class": "product-detail__sc-up77yl-1 doykVD"})


def get_goods_brand():
    brand = goods_detail.find(
        "a", attrs={"class": "product-detail__sc-achptn-9 dEnNme"}
    )


def get_goods_likes():
    likes = goods_detail.find(
        "span", attrs={"class": "product-detail__sc-achptn-4 coaOzR"}
    )


def get_goods_start_rating():
    star_rating = goods_detail.find(
        "span", attrs={"class": "product-detail__sc-achptn-4 bfPlAf"}
    )


def get_goods_reviews():
    reviews = goods_detail.find(
        "span", attrs={"class": "product-detail__sc-achptn-4 fgobnC"}
    )


print(get_goods_name())
