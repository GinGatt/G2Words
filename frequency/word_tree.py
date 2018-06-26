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
Furthermore, it is imperative that an instance of this singleton can be updated
in a thread-safe fashion, hence the RLock. The threads can call the methods of the singleton
"""

import threading


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
        self.lock = threading.RLock()

    def get_word(self, word):
        self.lock.acquire()
        try:
            return self.words_dict.get(word)
        finally:
            self.lock.release()

    def set_word(self, word, value):
        self.lock.acquire()
        try:
            self.words_dict[word] = value
        finally:
            self.lock.release()

    def increment_count_known_word(self, word):
        self.lock.acquire()
        try:
            self.words_dict[word][self.count] += self.words_dict[word][self.count]
        finally:
            self.lock.release()

    def add_sentence_known_word(self, word, sent_uuid):
        self.lock.acquire()
        try:
            if sent_uuid not in self.words_dict[word][self.sentences]:
                self.words_dict[word][self.sentences].append(sent_uuid)
        finally:
            self.lock.release()

    def add_file_known_word(self, word, filename):
        self.lock.acquire()
        try:
            if filename not in self.words_dict[word][self.files]:
                self.words_dict[word][self.files].append(filename)
        finally:
            self.lock.release()
