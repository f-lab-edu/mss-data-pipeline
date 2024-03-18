from bs4 import BeautifulSoup
from selenium import webdriver


def crawl_goods(url):
    html = get_page_html_from_url(url)
    soup = get_soup_object_from_html(html)
    goods_detail = get_detail_segment_from_soup_object(soup)
    goods_review = get_review_segment_from_soup_object(soup)
    goods_info = goods_detail.find(
        "ul", attrs={"class": "product-detail__sc-achptn-1 VIWAI"}
    ).find_all("li", attrs={"class": "product-detail__sc-achptn-2 idPepF"})
    infos = dict()
    for info in goods_info:
        info = info.get_text(separator="::").split("::")
        infos[info[0]] = info[1:]

    goods = [url.split("/")[-1]]  # goods id
    goods.append(get_goods_name(soup))
    goods.append(get_goods_thumbnail_url(goods_detail))
    goods.append(get_goods_regular_price(goods_detail))
    goods.append(get_goods_sale_price(goods_detail))
    goods.append(get_goods_category(soup))
    goods.append(get_goods_brand(infos))
    goods.append(get_goods_views(infos))
    goods.append(get_goods_sales(infos))
    goods.append(get_goods_likes(infos))
    goods.append(get_goods_star_rating(infos))
    goods.append(get_goods_reviews(infos))

    return goods


def get_page_html_from_url(url):
    user_agent = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("headless")
    chrome_option.add_argument(f'--user-agent={user_agent["User-Agent"]}')
    chrome_option.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_option)
    browser.get(url)
    html = browser.page_source
    browser.quit()

    return html


def get_soup_object_from_html(html):
    soup = BeautifulSoup(html, "lxml")

    return soup


def get_detail_segment_from_soup_object(soup):
    goods_detail = soup.find(
        "div", attrs={"class": "product-detail__sc-8631sn-1 fPAiGD"}
    )

    return goods_detail


def get_review_segment_from_soup_object(soup):
    review = soup.find("div", attrs={"class": "review-list-wrap"}).find_all(
        "div", attrs={"class": "review-list"}
    )

    return review


def get_goods_name(soup):
    name = soup.find("h3", attrs={"class": "product-detail__sc-1klhlce-3 fitNPd"})
    name = name.get_text()
    return name


def get_goods_thumbnail_url(goods_detail):
    img_url = goods_detail.find(
        "img", attrs={"class": "product-detail__sc-p62agb-9 cXcZGv"}
    )
    img_url_text = img_url.get("src")
    return img_url_text


def get_goods_regular_price(goods_detail):
    regular_price = goods_detail.find(
        "span", attrs={"class": "product-detail__sc-1p1ulhg-7"}
    )
    regular_price = regular_price.get_text()
    regular_price = regular_price[:-1]
    return regular_price.replace(",", "")


def get_goods_sale_price(goods_detail):
    sale_price = goods_detail.find(
        "span", attrs={"class": "product-detail__sc-1p1ulhg-7"}
    )
    sale_price = sale_price.get_text()
    sale_price = sale_price.split(" ~ ")[-1]
    sale_price = sale_price[:-1]
    return sale_price.replace(",", "")


def get_goods_category(soup):
    all_category = soup.find_all(
        "a", attrs={"class": "product-detail__sc-up77yl-1 doykVD"}
    )
    category = []
    for cg in all_category:
        category.append(cg.get_text())

    return category


def get_goods_brand(infos):
    return infos["브랜드"][1]  # 0: 품번(텍스트고정), 1: 브랜드이름, 2: 품번

    # brand = goods_detail.find(
    #     "a", attrs={"class": "product-detail__sc-achptn-9 dEnNme"}
    # )
    # brand = brand.get_text()
    # return brand


def get_goods_views(infos):
    won = {"만": 10000, "천": 1000}
    if "조회수(1개월)" in infos:
        views = infos["조회수(1개월)"][0]
        views = views.split(" ")[0]

        if views[-1] in won:
            num = views[:-1]
            views = float(num) * won[views[-1]]
        return int(views)
    else:
        return "NULL"


def get_goods_sales(infos):
    won = {"만": 10000, "천": 1000, "개": 1}
    if "누적판매(1년)" in infos:
        sales = infos["누적판매(1년)"][0]
        sales = sales.split(" ")[0]

        if sales[-1] in won:
            num = sales[:-1]
            scale = sales[-1]
            sales = float(num) * won[scale]
        return int(sales)
    else:
        return "NULL"


def get_goods_likes(infos):
    if "좋아요" in infos:
        likes = infos["좋아요"][0]
        return likes.replace(",", "")
    else:
        return "NULL"

    # likes = goods_detail.find(
    #     "span", attrs={"class": "product-detail__sc-achptn-4 coaOzR"}
    # )
    # likes = likes.get_text()
    # return likes


def get_goods_star_rating(infos):
    if "구매 후기" in infos:
        return infos["구매 후기"][0]  # 0: 별점, 1: 후기 개수
    else:
        return "NULL"

    # star_rating = goods_detail.find(
    #     "span", attrs={"class": "product-detail__sc-achptn-4 bfPlAf"}
    # )
    # star_rating = star_rating.get_text()
    # return star_rating


def get_goods_reviews(infos):
    if "구매 후기" in infos:
        reviews = infos["구매 후기"][1]  # 0: 별점, 1: 후기 개수
        reviews = reviews.split(" ")  # [후기, {개수}개]
        reviews = reviews[1][:-1]
        return reviews.replace(",", "")
    else:
        return "NULL"

    # reviews = goods_detail.find(
    #     "span", attrs={"class": "product-detail__sc-achptn-4 fgobnC"}
    # )
    # reviews = reviews.get_text()
    # return reviews
