import requests
import json
from bs4 import BeautifulSoup


def _get_page_(model: str):
    """
    Uses the website's search to find the page with the product model's review.
    @param model: The model name.
    @return: The review page url.
    """
    url = "https://www.rtings.com/api/v1/pages?query=" + model
    return "https://www.rtings.com" + json.loads(requests.get(url).text)["data"][0]["url"]


def get_reviews(url: str):
    """
    Returns a list containing the review, and only the review.
    @param url: The URL for the page with the review.
    @return: A list containing the review.
    """
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    reviews = list()
    review = ""
    for r in soup.select(".test_group-description > p"):
        review += r.text
    reviews.insert(0, review)
    return reviews


def get_score(url: str):
    """
    Get the averaged score on a scale of 0-10, as a float.
    The website separates the score into various categories, this is the average of these.
    @param url: The URL containing the review.
    """
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    score = 0
    scores = soup.select(".usage_card-usages .e-score_box-value")
    for n in scores:
        score += float(n.text)
    return float(score) / len(scores)


def get_search(model: str):
    """
    Returns the "top 5" search results based on the model name.
    @param model: The model to "search" for.
    @return: A list containing dictionaries containing the name and URL of the products.
    """

    response = json.loads(requests.get("https://www.rtings.com/api/v1/pages?query=" + model).text)
    products = list()
    try:
        for i in range(5):
            item = {
                "url": "https://www.rtings.com" + response["data"][i]["url"],
                "name": response["data"][i]["name"],
            }
            products.append(item)
    finally:
        return products
