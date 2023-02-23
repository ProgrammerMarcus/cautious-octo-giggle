import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


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
    return hrefs[0]


def _get_reviews(product_page: str, amount: int):
    """
    Uses webdriver to retrieve product model reviews.
    It continues to add reviews to the list until the amount limit is reached.
    :param product_page: Product page of the selected product model.
    :param amount: The amount of reviews to get.
    :return: A list of reviews.
    """
    url = get_review_link(product_page)
    options = webdriver.ChromeOptions()

    # Creates a headless Chrome instance, runs in the background without displaying a visible window
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Locating the button with "Show more" as text
    button = WebDriverWait(driver, 10) \
        .until(ec.element_to_be_clickable((By.XPATH,
                                           '//button[contains(@class, "BaseButton--") and span[contains(text(), '
                                           '"Show more")]]')))

    # Scroll to the button element to bring it into view
    actions = ActionChains(driver)
    actions.move_to_element(button).perform()

    # Script that clicks the "Show More" button, which loads more user reviews
    driver.execute_script("arguments[0].click();", button)

    # Wait for the page to load the additional reviews
    user_review_div = WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[id^="review-text-"]')))

    reviews = set()
    while len(reviews) < amount:
        for review_div in user_review_div:
            review = review_div.text
            if review not in reviews:
                reviews.add(review)
                if len(reviews) >= amount:
                    break

        driver.execute_script("arguments[0].click();", button)

        user_review_div = WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[id^="review-text-"]')))

    driver.quit()
    return list(reviews)[:amount]


def get_review_link(product_page: str):
    """
    Returns a review page for the given product model.
    :param product_page: Product page link of a product model.
    :return: A review page link as a string.
    """
    return "https://pricespy.co.uk" + product_page + "#reviews"


def get_list(model: str, amount: int):
    """
    Returns a list with reviews of the size of the specified amount.
    The returned reviews are those of the product model that was on
    the top of the search results.
    :param model: The product model to gather reviews for.
    :param amount: The amount of reviews to gather.
    :return: A list of reviews.
    """
    return _get_reviews(_get_product_page(model), amount)


def get_score(review_link: str):
    """
    Returns an already averaged score of the product model,
    on a scale of 1 - 10.
    :param review_link: Review page of the product model.
    :return: score as a float.
    """
    response = requests.get(review_link)
    score = re.findall(r'[^rank ]>(\d.\d)<', response.text)[0]
    return float(score) * 2


def get_search(model: str):
    """
    Returns the top 5 search results based on the model name.
    :param model: The product model to search for.
    :return: A list of dictionaries containing the name and URL of the products.
    """
    search_url = "https://pricespy.co.uk/search?search=" + model
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_names = soup.find_all("span", {"data-test": "ProductName"})[:5]
    urls = [tag.get("href") for tag in soup.find_all("a") if "--p" in tag.get("href")][:5]
    products = list()

    for i in range(len(urls)):
        product = {
            "url": get_review_link(urls[i]),
            "name": product_names[i].text
        }
        products.append(product)
    return products

