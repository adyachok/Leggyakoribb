import os
import string

import pandas as pd

from collections import Counter

from nltk.tokenize import word_tokenize



ROOT = os.path.abspath(os.path.dirname(__file__))


def get_all_books():
    books = []
    books_path = os.path.join(ROOT, 'books')
    for book in os.listdir(books_path):
        books.append(os.path.join(books_path, book))
    return books


def get_stopwords():
    stopwords_path = os.path.join(ROOT, 'utils/stopwords.txt')
    with open(stopwords_path, 'r') as s:
        return s.read().split('\n')


def get_custom_stopwords():
    stopwords_path = os.path.join(ROOT, 'utils/custom_stopwords.txt')
    with open(stopwords_path, 'r') as s:
        return s.read().split('\n')


def get_excluded_words_list():
    stopwords_path = os.path.join(ROOT, 'utils/excluded_words.txt')
    with open(stopwords_path, 'r') as s:
        return s.read().split('\n')


def get_custom_lemmatizer():
    df = pd.read_csv(os.path.join(ROOT, 'utils/lemmas.csv'))
    return df


def get_base_value(lemmatizer, variant):
    row = lemmatizer.loc[lemmatizer['variant'] == variant]
    if row.empty:
        return variant
    return row.values[0][1].strip()



def parse_corpus():
    books = get_all_books()
    stopwords = get_stopwords()
    custom_stopwords = get_custom_stopwords()
    stopwords.extend(custom_stopwords)
    stopwords = set(stopwords)
    counter = Counter()
    lemmatizer = get_custom_lemmatizer()
    excluded_words = get_excluded_words_list()
    for book in books[:2]:
        with open(book, 'r') as b:
            text = b.read()
            text = text.lower()
            text = text.translate(str.maketrans('', '',
                                                string.punctuation + '–”„“»«'))
            tokenized = word_tokenize(text)
            words = [word for word in tokenized if word not in stopwords]
            words = [get_base_value(lemmatizer, word) for word in words]
            words = [word for word in words if word not in excluded_words]
            counter.update(words)
    return counter.most_common(300)

if __name__ == '__main__':
    print(parse_corpus())
