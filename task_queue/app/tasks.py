from bs4 import BeautifulSoup
from collections import Counter
import requests
import time
import datetime
from nltk import wordpunct_tokenize, sent_tokenize
from string import punctuation
import pickle
from util import ValueInserter


HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36', 'referer':'https://www.google.com/'}


addtional_special_chars = ['—', '“', '”']
stop_words = pickle.load(open("stopwords.pkl", "rb"))

for symbol in addtional_special_chars:
    punctuation += symbol

executor = ValueInserter(table_name="words", db_name="word.db")

######################-Tasks-######################

def count_words(url):

    print(f"Counting words at {url}")

    start = time.time()
    resp = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(resp.content, 'html.parser')

    paragraphs = " ".join([p.text.lower() for p in soup.find_all('p')])

    # with tokenizer
    word_tokenized = wordpunct_tokenize(paragraphs)
    word_tokenized_cleaned = [word for word in word_tokenized if (word.lower() not in punctuation) and (word.lower() not in stop_words) and (len(word) > 1)]
    word_count = Counter(word_tokenized_cleaned)

    end = time.time()

    time_passsed = end - start

    print(f"Inserting Data to Database...")

    for word, count in word_count.items():
        executor.insert((datetime.datetime.now(), word, count, url), "words")

    print(f'Total Words: {len(word_count)} Time Elapsed: {time_passsed}')

    executor.close()

