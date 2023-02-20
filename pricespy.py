import re
from bs4 import BeautifulSoup
import requests


def _get_product_page(model: str):
    """
    Matches the product model name with a product page link by using PriceSpy's search.
    :param model: The model name.
    :return: A link to the product model page.
    """
    url = "https://pricespy.co.uk/search?search=" + model
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all("a")
    hrefs = [tag.get("href") for tag in tags if "--p" in tag.get("href")]
    if hrefs:
        return hrefs[0]


def _get_reviews(product_page: str, amount: int):
    """

    :param product_page:
    :param amount: The amount of reviews to get.
    :return: A list of reviews.
    """
    # review_url = get_review_link(product_page)
    # response = requests.get(review_url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # tags = soup.find_all(string=re.compile("£.*"))
    # tags = soup.find_all("div", attrs={"data-test": True})
    # for tag in tags:
    #     print(tag)
    # tag = soup.find_all(class_=re.compile("Reviews.*"))
    # for d in soup.find_all("div"):
    #     print(d.get('style'))
    # pattern = r'::before\s*{\s*content:\s*"([^"]+)"\s*;}'
    # pattern = r'::before\s*'
    #
    # print(re.search(pattern, response.text).group())
    #
    # reviews = []
    reviews = []
    return reviews


def get_review_link(product_page: str):
    """
    Returns a review page for the given product model.
    :param product_page: Product page link of a product model.
    :return: A review page link as a string.
    """
    return "https://pricespy.co.uk" + product_page + "#reviews"


def get_list(model: str, amount: int):
    return _get_reviews(_get_product_page(model), amount)


def get_score(review_link: str):
    """
    Returns an already averaged score of the product model,
    on a scale of 1 - 5.
    :param review_link: Review page of the product model.
    :return: score as a float.
    """
    response = requests.get(review_link)
    score = re.findall(r'[^rank ]>(\d.\d)<', response.text)[0]
    return float(score)


# _get_reviews(_get_product_page("microsoft xbox"), 0)
