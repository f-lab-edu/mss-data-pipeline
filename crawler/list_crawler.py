import requests
from bs4 import BeautifulSoup


def get_goods_url_from_list_page(list_page_url):
    response = requests.get(list_page_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")

        links = soup.find_all("a", attrs={"name": "goods_link"})

        for link in links[::2]:
            yield f"https:{link.get('href')}"
    else:
        print("Error:", response.status_code)
