#By Lydia Vasilyeva
#Data 620: Professor Carrie Beam
#Assignment 12.1
import os
import sys
import csv
import nltk
import string
import logging
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


logging.basicConfig(level='INFO')

NUM_WORDS = 70
YEAR = 2016

class FileParser:
    # creat a class
    DEF_STOPWORDS = ['1','2','3','4','5','6','7','8','9','0','one',
                 'u','two','o',"also",'however']

    def __init__(self, file_path, stopwords=stopwords.words('english')):
        #Perform Basic validation of input and reading the data from the file.
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            logging.error("File {} does not exist.".format(self.file_path))
            raise RuntimeError("File Does Not Exist")

        try:
            with open(self.file_path) as txtfile:
                self.text_data = txtfile.read().lower()

        except Exception as e:
            logging.error('File cannot be opened.')
            logging.exception(e)
            raise

        self.lemmatizer = WordNetLemmatizer()
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stopwords = stopwords + self.DEF_STOPWORDS


    def process(self, num_words=50):
        prepped_text = self.prep_text(self.text_data)
        word_freq = self.get_word_frequency(prepped_text, num_words)


    def prep_text(self, text):
        #Returns cleaned text after tokenization and stopwords removal.
        out = []
        tokens = self.tokenizer.tokenize(text)
        for token in tokens:
            if token in self.stopwords:
                continue
            try:
                self.lemmatizer.lemmatize(token)
            except Exception as e:
                logging.error("Error Using Lemattizer, sure nltk wordnet is donwnloaded.")
                raise
            out.append(token)
        return out


    def get_word_frequency(self, tokens, num_words):
        #Returns a list of touples (w, n), where w is term and n is frequency.
        self.counter = Counter(tokens)
        return self.counter.most_common(num_words)


    def print_top_words(self, num_words):
        #Prints a tab delimited list of top `num_words` from text.

        for i, wrd_tpl in enumerate(self.counter.most_common(num_words)):
            print("\t".join([str(i), *[str(x) for x in wrd_tpl]]))


    def write_output(self, output_file_path, num_words, year):
        #Writes a CSV of top `num_words` and a `year` to `output_file_path`.
        with open(output_file_path, 'a') as f:
            writer = csv.DictWriter(f, lineterminator='\n',
                                    fieldnames=['Rank', 'Word',
                                                'Frequency', 'Year'])
            writer.writeheader()
            for i, tpl in enumerate(self.counter.most_common(num_words)):
                writer.writerow({'Rank':i, 'Word': tpl[1],
                                 'Frequency': tpl[0],'Year':year})
        return output_file_path


if __name__ == "__main__": # only run if the script is run
    while True:
        inp = input('Please Enter the File Path or enter "exit" to end the program: ')
        if inp.lower() == 'exit':
            sys.exit(1)
        file_parser = FileParser(inp)
        file_parser.process(NUM_WORDS)
        print("The 50 most frequent words are")
        print("Rank\tFrequency\tWord")
        file_parser.print_top_words(NUM_WORDS)
        try:
            out_file_name = inp.split('.')[-2]+'.csv'
            logging.info("Writing Output to {}".format(out_file_name))
            file_parser.write_output(out_file_name, NUM_WORDS, YEAR)
        except Exception as e:
            logging.error("Unable to write output")
            logging.exception(e)
