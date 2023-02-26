
def summary(words: list):
    """
    Formats a string based on the list (generated in processor.py).
    @param words: A list containing a list of a score and a string.
    @return: A string formatted based on the parameter.
    """
    text = ""

    for word in words[:10]:
        text += word[0].title() + ": " + str(word[1]) + "x\n"

    if text == "":
        return "Insufficient reviews."
    else:
        return text
