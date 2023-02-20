import requests
import json
from bs4 import BeautifulSoup


def _get_page(model: str):
    """
    Uses the website's search to find the page with the product model's review.
    @param model: The model name.
    @return: The review page url.
    """
    url = "https://www.rtings.com/api/v1/pages?query=" + model
    return "https://www.rtings.com" + json.loads(requests.get(url).text)["data"][0]["url"]


def get_list(model: str):
    """
    Returns a list containing the review, and only the review.
    @param model: The model to find the review of.
    @return: A list containing the review.
    """
    soup = BeautifulSoup(requests.get(_get_page(model)).content, 'html.parser')
    reviews = list()
    review = ""
    for r in soup.select(".test_group-description > p"):
        review = review + r.text
    reviews.insert(0, review)
    return reviews


def get_score(model: str):
    """
    Get the already averaged score on a scale of 0-10, as a float.
    The website separates the score into various categories, this is the average of these.
    @param model: The model to get the score for.
    """
    soup = BeautifulSoup(requests.get(_get_page(model)).content, 'html.parser')
    score = 0
    scores = soup.select(".usage_card-usages .e-score_box-value")
    for n in scores:
        score += float(n.text)
    return float(score) / len(scores)


