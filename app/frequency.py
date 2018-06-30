import os
import json
from app import app
from .helpers import split_into_sentences, split_into_words
from .word_tree import WordTree
from app import redis_conn


class Frequency:
    """
    Class with capabilities of calculating, sorting, and saving word info from upload directory
    """
    def __init__(self):
        """
        Initializes Frequency Class as invoked by the /results route
        """
        self.word_tree = WordTree()
        self.session_word_tree = self.word_tree.words_dict

    def calculate(self, folder_path):
        """
        Only public method which should be called during the tabulation of the frequency and location of words
        :param str folder_path: The path of the folder which stores the .txts uploaded from the website
        """
        file_set = self._chk_folder(folder_path)
        for file in file_set:
            self._process_file(file)
        # save the whole tree for future after processing all files - TODO error handling in case connectivity issues
        redis_conn.hset(app.config['CACHE_NAME'], app.config['CACHE_KEY'], json.dumps(self.session_word_tree))
        # clear the local local cache since these have already been processed
        self.word_tree.clear_local_cache()
        sorted_result = sorted(self.session_word_tree.items(), key=(lambda x: x[1]['count']), reverse=True)
        return sorted_result

    def _process_file(self, file, filter_stop_words=True):
        """
        Private method that reads the file, tokenizes words into sentence arrays, and initiates processing of sentences
        :param str file: The file to digest
        :param bool filter_stop_words: Filter stop words would remove the most common words, leaving more relevant words
        """
        with open(file) as f:
            read_data = f.read()
        sentences_array = split_into_sentences(read_data)
        for sentence in sentences_array:
            short_filename = os.path.basename(file)
            self._process_sentence(sentence, short_filename, filter_stop_words)
        return

    def _process_sentence(self, sentence, filename, filter_stop_words):
        """
        Private method that takes a sentence, stores it, breaks sentence into word array, and stores info
        :param str sentence: The sentence to process
        :param str filename: The filename in which the sentence is located
        :param bool filter_stop_words: Filter stop words would remove the most common words, leaving more relevant words
        """
        # TODO filter stop words here
        sentence_array = split_into_words(sentence)
        for word in sentence_array:
            word = word.lower()
            if self.word_tree.get_word(word):
                self.word_tree.increment_count_known_word(word)
                self.word_tree.add_sentence_known_word(word, sentence)
                self.word_tree.add_file_known_word(word, filename)
            else:
                self.word_tree.set_first_instance_word(word, sentence, filename)
        return

    @staticmethod
    def _chk_folder(folder_path):
        """
        Private method that provides a set of all files in folder with .txt ending
        :param str folder_path: The path to the folder to process (in this case the Uploads folder)
        :return set : Set of all file paths with txt ending
        """
        file_path_set = set()
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.txt'):
                    path = os.path.join(root, file)
                    file_path_set.add(path)
        return file_path_set
