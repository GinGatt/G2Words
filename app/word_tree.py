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

from app import app, redis_conn
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

    def __init__(self):
        """
        Initializes WordTree Singleton Class
        """
        self.words_dict = self.pull_cache()
        # self.lock = threading.RLock()

    @staticmethod
    def pull_cache():
        """
        Pull existing tree held in Redis, else return {}
        :return dict
        """
        word_tree_from_cache = redis_conn.hgetall(app.config['CACHE_KEY'])
        print("previous cache", word_tree_from_cache)
        if word_tree_from_cache:
            word_tree_from_cache = word_tree_from_cache['word_tree']
        else:
            word_tree_from_cache = {}
        return word_tree_from_cache

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

    def increment_count_known_word(self, word):
        """
        Increment count of a known word
        ONLY USE WITH WORDS ALREADY IN DICT, ELSE KEY_ERROR
        :param str word: The word serving as the key
        :return None
        """
        # with self.lock.acquire():
        self.words_dict[word][self.count] += self.words_dict[word][self.count]

    def add_sentence_known_word(self, word, sentence):
        """
        Add additional sentence uuid of existing word to its sentence array
        ONLY USE WITH WORDS ALREADY IN DICT, ELSE KEY_ERROR
        :param str word: The word serving as the key
        :param str sentence: The sentence in which the word is located
        :return None
        """
        # with self.lock.acquire():
        if sentence not in self.words_dict[word][self.sentences]:
            self.words_dict[word][self.sentences].append(sentence)

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

    def set_first_instance_word(self, word, sentence, filename):
        """
        Set and establish the future structure for the new word key
        :param str word: The word serving as the key
        :param str sentence: The sentence in which the word is located
        :param str filename: The filename from which word originated
        :return None
        """
        self.words_dict[word] = {self.count: 1, self.sentences: [sentence], self.files: [filename]}
