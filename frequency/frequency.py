import os
import uuid
from .helpers import split_into_sentences
from .word_tree import WordTree


class Frequency:
    """
    Class with capabilities of calculating, sorting, and saving word info from upload directory
    """
    def __init__(self):
        """
        Initializes Frequency Class as invoked by the /results route
        """
        self.session_word_tree = WordTree({})

    def calculate(self, folder_path):
        file_set = self._chk_folder(folder_path)
        for file in file_set:
            self._process_file(file)

    def _process_file(self, file, filter_stop_words=True):
        with open(file) as f:
            print(file)
            read_data = f.read()
        sentences_array = split_into_sentences(read_data)
        for sentence in sentences_array:
            self._process_sentence(sentence, file, filter_stop_words)

    def _process_sentence(self, sentence, filename, filter_stop_words):
        sent_uuid = uuid.uuid4()
        self.session_word_tree.set_key(sent_uuid, sentence)
        for word in sentence:
            if self.session_word_tree.get_word(word):
                self.session_word_tree.increment_count_known_word(word)
                self.session_word_tree.add_sentence_known_word(word, sent_uuid)
                self.session_word_tree.add_file_known_word(word, filename)
            else:
                self.session_word_tree.set_first_instance_word(word, sent_uuid, filename)

    @staticmethod
    def _chk_folder(folder_path):
        file_path_set = set()
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.txt'):
                    path = os.path.join(root, file)
                    file_path_set.add(path)
        return file_path_set
