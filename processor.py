from itertools import chain
import os
from operator import itemgetter
from functools import reduce
import nltk


def s_counter(words: list):
    """
    Takes a list of words and returns a sorted list containing both the count of each word after applying stemming
    and the original word.
    @param words: The list of words to count.
    @return: A sorted list containing the count and original word.
    """
    stemmer = nltk.stem.SnowballStemmer("english")
    counted = dict()
    for word in words:
        stemmed = stemmer.stem(word)
        if stemmed in counted.keys():
            counted.update({stemmed: [word, counted.get(stemmed)[1] + 1]})
        else:
            counted.update({stemmed: [word, 1]})
    return sorted(counted.values(), key=itemgetter(1), reverse=True)


def process(*args: list):
    """
    From any number of lists of reviews, generate a dictionary of statistics about each word.
    Dictionary contains the "count", the "stemmed" word, and the "original" word.
    Original meaning the first occurrence of the word.
    @param args: Any number of lists of reviews.
    @return: A dictionary containing review statistics.
    """

    nltk.data.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "nltk_data"))
    stemmer = nltk.stem.SnowballStemmer("english")

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "whitelist.txt")) as file:
        whitelist = [stemmer.stem(line.strip()) for line in file]
        filtered = s_counter(list(filter(lambda w: stemmer.stem(w) in whitelist,
                                         reduce(lambda a, t: a + t, map(lambda i: nltk.word_tokenize(i, "english"),
                                                                        chain(chain(*args)))))))

    return filtered


def score(scores: list):
    """
    Calculates the average of the arguments.
    @param scores: Any number of floating point arguments.
    @return: The average of the arguments.
    """
    total = 0.0
    for num in scores:
        total += num
    if len(scores) < 1:
        return -1
    return total / len(scores)
