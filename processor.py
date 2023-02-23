import nltk
import re

import pricerunner


def process(*args: list):
    """
    From any number of lists of reviews, generate a dictionary of statistics about each word.
    Dictionary contains the "count", the "stemmed" word, and the "original" word.
    Original meaning the first occurrence of the word.
    @param args: Any number of lists of reviews.
    @return: A dictionary containing review statistics.
    """
    stemmer = nltk.stem.SnowballStemmer("english")
    dictionary = dict()
    for reviews in args:
        for review in reviews:
            words = re.sub(r"([,.;()]|\\n)", " ", review).split()
            for word in words:
                stem = stemmer.stem(word)
                if dictionary.get(stem):
                    previous = dictionary.get(stem)
                    previous["count"] += 1
                    dictionary.update(previous)
                    print(dictionary.get(stem))
                else:
                    dictionary.update({
                        stem: {
                            "count": 1,
                            "stemmed": stem,
                            "original": word,
                        },
                    })
        return dictionary


def score(*args: float):
    """
    Calculates the average of the arguments.
    @param args: Any number of floating point arguments.
    @return: The average of the arguments.
    """
    total = 0.0
    for num in args:
        total += num
    if len(args) < 1:
        return -1
    return total / len(args)


process(pricerunner.get_reviews(pricerunner.get_search("airpods").pop()["url"]))
