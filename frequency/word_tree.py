"""
The intended goal of the structure of the singleton master_words_dict is to mimic
the tree/leaves structures found in other languages. Each word represents a tree,
and each piece of information (parent sentences, parent files, and frequency)
represents the leaves.

Organizing by word, allows us to build upon our previous work.
If we run 5 files initially and then desire to add 2 more files, our program shouldn't
have to analyze all 7 files. Instead it should only have to analyze the 2 new files.
With this goal in mind, we store the master_words_dict in Redis upon run completion
and rehydrate upon run start. Since it is imperative there is ONLY one dict of this type,
efforts have been made to make it a singleton. It must be initialized outside of a thread.
"""

import threading

# TODO determine if Threading or parallel processing of each file or sentence is needed...


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class WordTree(object):
    """
    Singleton class that holds all word information during the program's run.
    Upon completion, this dict is saved as cache to be re-hydrated on load.
    When populated, available keys include count(int), sentences(array), and files(array)
    """
    count = "count"
    sentences = "sentences"
    files = "files"

    def __init__(self, words_dict):
        """
        Initializes WordTree Singleton Class
        :param dict words_dict: The dict from cache or empty dict
        """
        self.words_dict = words_dict
        # self.lock = threading.RLock()

    # TODO written explicitly to highlight the equivalency of the context manager in the following function
    def get_word(self, word):
        """
        Fetches value of word if word exists, else returns undefined;
        A direct dict[k] call could result in KeyError, hence .get() choice
        :param str word: The word serving as the key
        :return value as a dict or undefined
        """
        # with self.lock.acquire():
        return self.words_dict.get(word)

    def set_key(self, key, value):
        """
        Set value for the given word serving as a key
        :param str key: The key to set
        :param _ value: The value of the key
        :return None
        """
        # with self.lock.acquire():
        self.words_dict[key] = value

    def increment_count_known_word(self, word):
        """
        Increment count of a known word
        ONLY USE WITH WORDS ALREADY IN DICT, ELSE KEY_ERROR
        :param str word: The word serving as the key
        :return None
        """
        # with self.lock.acquire():
        self.words_dict[word][self.count] += self.words_dict[word][self.count]

    def add_sentence_known_word(self, word, sent_uuid):
        """
        Add additional sentence uuid of existing word to its sentence array
        ONLY USE WITH WORDS ALREADY IN DICT, ELSE KEY_ERROR
        :param str word: The word serving as the key
        :param  sent_uuid: The uuid serving as a reference to the sentence in which the word is located
        :return None
        """
        # with self.lock.acquire():
        if sent_uuid not in self.words_dict[word][self.sentences]:
            self.words_dict[word][self.sentences].append(sent_uuid)

    def add_file_known_word(self, word, filename):
        """
        Add additional filename of existing word to its filename array
        ONLY USE WITH WORDS ALREADY IN DICT, ELSE KEY_ERROR
        :param str word: The word serving as the key
        :param str filename: The filename from which word originated
        :return None
        """
        # with self.lock.acquire():
        if filename not in self.words_dict[word][self.files]:
            self.words_dict[word][self.files].append(filename)

    def set_first_instance_word(self, word, sentence_uuid, filename):
        """
        Set and establish the future structure for the new word key
        :param str word: The word serving as the key
        :param  sentence_uuid: The uuid serving as a reference to the sentence in which the word is located
        :param str filename: The filename from which word originated
        :return None
        """
        self.set_key(word, {self.count: 1, self.sentences: [sentence_uuid], self.files: [filename]})
