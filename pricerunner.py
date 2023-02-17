import requests
import json
import re


def _get_product(model: str):
    """
    Matches the product name with an id by using Pricerunner's search.
    @param model: The model name.
    @return: A product model "id".
    """
    url = "https://www.pricerunner.com/results?q=" + model
    response = requests.get(url)
    product = re.findall(r'href="/pl/\d*-(\d*)/', response.text).pop(0)
    return product


def _get_reviews(product: int, amount: int):
    """
    Get the reviews for the product "id".
    @param product: The product "id".
    @param amount: The amount of reviews to get.
    @return: A list of reviews.
    """
    base = 'https://www.pricerunner.com/public/social/content/review/productversions/merged/'
    data = '/uk?offset=0&limit=' + str(amount) + '&testFreak=true&section=prio'
    url = base + str(product) + data
    print(url)
    response = requests.get(url)

    parsed = json.loads(response.text)
    reviews = list()

    for content in parsed["reviewContent"]:
        review = content["subContent"]["reviewText"]
        if review is not None:
            list.append(reviews, review)

    return reviews


def get_list(model: str, amount: int):
    """
    Attempts to return the specified amount of reviews about the specified product model.
    The product model whose reviews are returned are the one that is first in the
    search results.
    @param amount: The amount of reviews to return.
    @param model: The product model to gather reviews for.
    @return: A list of reviews.
    """
    return _get_reviews(_get_product(model), amount)

