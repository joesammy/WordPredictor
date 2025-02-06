from __future__ import unicode_literals
import math
import re
from collections import defaultdict
import codecs

class ModelBuilder(object):
    """
    This class constructs a bigram language model from a corpus.
    """

    def process_files(self, filename):
        done = False
        with codecs.open(filename, 'r', 'utf-8') as f:
            text = f.read().encode('utf-8').decode()
        
        # Split text into sentences first (roughly)
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            if sentence.strip():  # Skip empty sentences
                # Add start symbol for each sentence
                self.process_token("<s>")
                
                # Process words in the sentence
                words = re.findall(r"\b[A-Za-z]+(?:[-'’][A-Za-z]+)*\b", sentence)

                if "hadn" in words and not done:
                    print(words)
                    done = True

                
                for token in words :
                    self.process_token(token)

    def process_token(self, token):
        """
        Processes one word in the training corpus, and adjusts the unigram and
        bigram counts.

        :param token: The current word to be processed. 
        """
        if not (token in self.unigram_count): #Om första instansen
            self.unigram_count[token] = 1

            self.index[token] = self.unique_words
            self.word[self.unique_words] = token
    
            self.unique_words += 1            
        else: #Om den redan är med
            self.unigram_count[token] += 1


        if (self.last_index == -1):  #För att första ordet inte ska vara med i bigram
            pass

        elif not token in self.bigram_count[self.word[self.last_index]]:
            self.bigram_count[self.word[self.last_index]][token] = 1

        elif token in self.bigram_count[self.word[self.last_index]]:
            self.bigram_count[self.word[self.last_index]][token] += 1

        self.total_words += 1
        self.last_index = self.index[token]


    def stats(self):
        """
        Creates a list of rows to print of the language model.
        """
        rows_to_print = []
        
        rows_to_print.append(f"{self.unique_words} {self.total_words}") #Första raden

        for i in range(self.unique_words): #Unigram rader
            rows_to_print.append(f"{i} {self.word[i]} {self.unigram_count[self.word[i]]}")

        for word1, inner_dict in self.bigram_count.items(): #Bigram rader
            for word2, value in inner_dict.items():
                log_probability = math.log(value/self.unigram_count[word1])
                formatted_log_prob = f"{log_probability:.15f}"
                rows_to_print.append(f"{self.index[word1]} {self.index[word2]} {formatted_log_prob}")
        
        rows_to_print.append("-1") #Sista raden

        return rows_to_print


    def __init__(self):
        """
        Constructor. Processes the file f and builds a language model
        from it.

        :param f: The training file.
        """

        # The mapping from words to identifiers.
        self.index = {}

        # The mapping from identifiers to words.
        self.word = {}

        # An array holding the unigram counts.
        self.unigram_count = defaultdict(int)

        """
        The bigram counts. Since most of these are zero (why?), we store these
        in a hashmap rather than an array to save space (and since it is impossible
        to create such a big array anyway).
        """
        self.bigram_count = defaultdict(lambda: defaultdict(int))

        # The identifier of the previous word processed.
        self.last_index = -1

        # Number of unique words (word forms) in the training corpus.
        self.unique_words = 0

        # The total number of words in the training corpus.
        self.total_words = 0

        # Add the sentence start symbol to the vocabulary at initialization
        self.index["<s>"] = 0
        self.word[0] = "<s>"
        self.unigram_count["<s>"] = 0
        self.unique_words += 1