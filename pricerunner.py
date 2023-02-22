import requests
import json
import re
from bs4 import BeautifulSoup


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
    response = requests.get(url)

    parsed = json.loads(response.text)
    reviews = list()

    for content in parsed["reviewContent"]:
        review = content["subContent"]["reviewText"]
        if review is not None:
            list.append(reviews, review)

    return reviews


def _get_score_(model: str):
    """
    Get the already averaged score on a scale of 1-5, as a float.
    @param model: The model to get the score for.
    """
    url = "https://www.pricerunner.com/results?q=" + model
    response = requests.get(url)
    score = re.findall(r'>(\d\.\d)<', response.text).pop(0)
    return float(score)


def _get_list_(model: str, amount: int):
    """
    Attempts to return the specified amount of reviews about the specified product model.
    The product model whose reviews are returned are the one that is first in the
    search results.
    @param amount: The amount of reviews to return.
    @param model: The product model to gather reviews for.
    @return: A list of reviews.
    """
    return _get_reviews(_get_product(model), amount)


def get_reviews(url: str):
    """
    Returns the reviews in the URL.
    @param url: The URL with the reviews.
    @return: A list of reviews.
    """
    parsed = json.loads(requests.get(url).text)

    reviews = list()

    for content in parsed["reviewContent"]:
        review = content["subContent"]["reviewText"]
        if review is not None:
            list.append(reviews, review)

    return reviews


def get_score(url: str):
    """
    Returns the score as calculated from the reviews on a scale of 0-10
    @param url: The URL with the reviews.
    @return: The score as a floating point number on a scale of 0-10.
    """
    parsed = json.loads(requests.get(url).text)

    score = 0.0
    counter = 0

    for content in parsed["reviewContent"]:
        rating = content["subContent"]["rank"]
        if rating is not None:
            counter += 1
            score += float(rating)

    if counter > 0:
        return (score / counter) / 0.5
    else:
        return -1


def get_search(model: str):
    """
    Returns the "top 5" search results based on the model name.
    Currently, creates URLs with 30 reviews, which is the maximum that can be gotten in a single request.
    @param model: The model to "search" for.
    @return: A list containing dictionaries containing the name and URL of the products.
    """
    url = "https://www.pricerunner.com/results?q=" + model
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    names = soup.select("h3")
    ids = re.findall(r'href="/pl/\d*-(\d*)/', response)[:5]
    products = list()

    for i in range(len(ids)):
        item = {
            "url": "https://www.pricerunner.com/public/social/content/review/productversions/merged/" + ids[i] +
                   "/uk?offset=0&limit=" + str(30) + '&testFreak=true&section=prio',
            "name": names[i].text,
        }
        products.append(item)

    return products
