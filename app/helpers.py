# TODO: It is noted that a library, such as SpaCy or nltk would be invaluable here and render helpers obsolete
# TODO cont ... However, I was uncomfortable with a library doing all my work in a coding exercise..

import re

caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|me|edu)"
digits = "([0-9])"


def split_into_sentences(text):
    """
    Given a block of text, split into an list of sentences using crude rules to determine sentence end
    :param str text: The full text body of the file
    :return list : List of all the sentences within a file
    """
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    if "i.e." in text: text = text.replace("i.e.", "i<prd>e<prd>")
    if "..." in text: text = text.replace("...", "<prd><prd><prd>")
    text = re.sub("\s" + caps + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(acronyms+" " + caps, "\\1<stop> \\2", text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] "+ starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]" + caps, " \\1<stop> \\2", text)
    text = re.sub(" " + caps + "[.]", " \\1<prd>", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def split_into_words(sentence):
    """
    Given a raw sentence, split into a list of words using crude rules to determine a period's appropriateness
    :param str sentence: The original sentence string before removal of stop words etc
    :return list : List of all the words in a given sentence
    """
    word_array = sentence.split()
    word_array[-1] = re.sub(suffixes + "[.]", "\\1..", word_array[-1])
    word_array[-1] = re.sub(acronyms, "\\1.", word_array[-1])
    if "Ph.D" in word_array[-1]: word_array[-1] = word_array[-1].replace("Ph.D.", "Ph.D..")
    if "..." in word_array[-1]: word_array[-1] = word_array[-1].replace("...", "....")
    word_array[-1] = word_array[-1][:-1]
    return word_array
