#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import string

import pandas as pd

from collections import Counter

from nltk.tokenize import word_tokenize



ROOT = os.path.abspath(os.path.dirname(__file__))


def get_all_books():
    books = {}
    books_path = os.path.join(ROOT, 'books')
    for book in os.listdir(books_path):
        books[os.path.splitext(book)[0]] = os.path.join(books_path, book)
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



def parse_corpus(book_name=None):
    books = get_all_books()
    stopwords = get_stopwords()
    custom_stopwords = get_custom_stopwords()
    stopwords.extend(custom_stopwords)
    stopwords = set(stopwords)
    counter = Counter()
    lemmatizer = get_custom_lemmatizer()
    excluded_words = get_excluded_words_list()
    build_most_commom_words(book_name, books, counter, excluded_words,
                            lemmatizer, stopwords)
    return counter.most_common(1300)


def build_most_commom_words(book_name, books, counter, excluded_words,
                            lemmatizer, stopwords):
    for name, book in books.items():
        if book_name and book_name not in name:
            print(f'Book {name} skipped...')
            continue
        with open(book, 'r') as b:
            text = b.read()
            text = text.lower()
            text = text.translate(str.maketrans('', '',
                                                string.punctuation + '–”„“»«'))
            words = process_text(excluded_words, lemmatizer, stopwords, text)
            counter.update(words)


def process_text(excluded_words, lemmatizer, stopwords, text):
    # tokenized = word_tokenize(text)
    # words = [word for word in tokenized if word not in stopwords]
    # words = [get_base_value(lemmatizer, word) for word in words]
    # words = [word for word in words if word not in excluded_words]
    # return words
    import hu_core_ud_lg

    nlp = hu_core_ud_lg.load()
    doc = nlp(text)
    return [token.lemma_ for token in doc
            if token.tag_ not in ['PUNCT', 'NUM']
            and not token.is_stop
            and token.tag_ == 'VERB']


if __name__ == '__main__':
    # print(parse_corpus())
    # from deps.emmorphpy.emmorphpy import emmorphpy as emmorph
    #
    # m = emmorph.EmMorphPy(hfst_lookup='deps/apertium')
    # m.stem('működik')
    # import hu_core_ud_lg
    #
    # nlp = hu_core_ud_lg.load()
    # doc = nlp('Csiribiri csiribiri zabszalma peter - négy csillag közt alszom ma.')
    #
    # for token in doc:
    #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #           token.shape_, token.is_alpha, token.is_stop)
    words = parse_corpus(book_name='egri')


