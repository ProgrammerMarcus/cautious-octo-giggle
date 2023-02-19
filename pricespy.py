from bs4 import BeautifulSoup
import requests

def _get_product(model: str):
    url = "https://pricespy.co.uk/search?search=" + model
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.h1)


_get_product("playstation")
