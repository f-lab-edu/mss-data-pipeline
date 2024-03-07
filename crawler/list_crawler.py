import requests
from bs4 import BeautifulSoup

# 웹 페이지 URL
url = "https://www.musinsa.com/categories/item/004"


def get_goods_url_from_list_page(list_page_url):
    # GET 요청으로 웹 페이지의 HTML 콘텐츠 받아오기
    response = requests.get(list_page_url)

    # 요청이 성공적으로 이루어졌는지 확인
    if response.status_code == 200:
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, "lxml")

        # name 속성이 'goods_link'인 모든 <a> 태그 찾기 (예시 속성, 실제 속성으로 대체 필요)
        links = soup.find_all("a", attrs={"name": "goods_link"})

        # 각 링크의 href 속성 값 출력
        for link in links[::2]:
            yield f"https:{link.get('href')}"
    else:
        print("Error:", response.status_code)


for i in get_goods_url_from_list_page(url):
    print(i)
