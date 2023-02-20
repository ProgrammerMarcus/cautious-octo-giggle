from bs4 import BeautifulSoup
import requests
import re


def _get_product(model: str):
    """
    Matches the product model name with an id by using PriceSpy's search.
    :param model: The model name.
    :return: The product model id as a string.
    """
    url = "https://pricespy.co.uk/search?search=" + model
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all("a")
    hrefs = [tag.get("href") for tag in tags if "--p" in tag.get("href")]
    if hrefs:
        result = re.findall(r'--p\d+', hrefs[0])
        return result[0]


def _get_reviews():
    pass


print(_get_product("nintendo"))
