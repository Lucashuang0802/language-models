import sys
import re
import traceback
import math

# sentence start and end
SENTENCE_START = "<s>"
SENTENCE_END = "</s>"

class UnigramModel:
    def __init__(self, sentences):
        self.unigram_frequencies = {}
        self.corpus_length = 0
        for sentence in sentences:
            for word in sentence:
                self.unigram_frequencies[word] = self.unigram_frequencies.get(word, 0) + 1
                if word != SENTENCE_START and word != SENTENCE_END:
                    self.corpus_length += 1

    def calculate_unigram_probability(self, word):
        return float(self.unigram_frequencies[word]) / float(self.corpus_length)

class BigramModel(UnigramModel):
    def __init__(self, sentences):
        UnigramModel.__init__(self, sentences)
        self.bigram_frequencies = {}
        for sentence in sentences:
            previous_word = None
            for word in sentence:
                if previous_word != None:
                    self.bigram_frequencies[(previous_word, word)] = self.bigram_frequencies.get((previous_word, word), 0) + 1
                previous_word = word

    def calculate_bigram_probabilty(self, previous_word, word):
        numerator = self.bigram_frequencies.get((previous_word, word), 0)
        denominator = self.unigram_frequencies[previous_word]
        if numerator == 0 or denominator == 0:
            return 0.0
        return float(numerator) / float(denominator)

def run():
    corpus = []
    try:
        file_handler = open('sampledata.txt', 'r')
        corpus = [re.split("\s+", line.rstrip('\n')) for line in file_handler]
    except IOError as err:
        print("IO error: {0}".format(err))
        sys.exit(1)
    except OSError as err:
        print("OS error: {0}".format(err))
        sys.exit(1)
    except:
        """handle generic errors"""
        print("Unexcept error: {0}".format(sys.exc_info()))
        traceback.print_exc()
        sys.exit(1)

    model = BigramModel(corpus)
    keys = list(model.unigram_frequencies.keys())

    print("=== UNIGRAM MODEL ===")
    for key in keys:
        if key != SENTENCE_START and key != SENTENCE_END:
            print("{}: {}".format(key, model.calculate_unigram_probability(key)))
    print("\n=== BIGRAM MODEL ===")
    print("\t\t", end="")
    for key in keys:
        if key != SENTENCE_START:
            print(key, end="\t\t")
    print()
    for key in keys:
        if key != SENTENCE_END:
            print(key, end="\t\t")
            for key_col in keys:
                if key_col != SENTENCE_START:
                    print("{0:.5f}".format(model.calculate_bigram_probabilty(key, key_col)), end="\t\t")
            print()

# print unigram and bigram probs
if __name__ == '__main__':
    run()
