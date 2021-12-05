"""Compare the number of unique words after stemming and lemmatization"""

__author__    =  "Venkat S. Narayana"
__contact__   =  "narayana.svenkat.cse17@iitbhu.ac.in"
__date__      =  "Jan 25, 2020"


import os
import re
import math
import nltk
import datetime

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer


path = '/Users/narayanavenkat/desktop/20news-18828/'
words_frequency = dict()
words_stemming_porter = set()
words_stemming_snowball = set()
words_lemmatizing = set()

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
sstemmer = SnowballStemmer("english")


for root, d_names, f_names in os.walk(path):
    print("New Directory!")
    for f_name in f_names:
        openf = open(root + "/"+ f_name, 'r')
        file_string = openf.read()
        words = re.findall(r'(\b[A-Za-z][a-z]{2,9}\b)', file_string)
        for word in words:
            word = word.lower()
            words_stemming_porter.add(stemmer.stem(word))
            words_lemmatizing.add(lemmatizer.lemmatize(word))
            words_stemming_snowball.add(sstemmer.stem(word))
            if word in words_frequency:
                words_frequency[word]+=1
            else:
                words_frequency[word]=1
                
                
print("Number of unique words")
print("Raw Corpus"+" "+str(len(words_frequency)))
print("Porter Stemmer"+" "+str(len(words_stemming_porter)))
print("SnowBall Stemmer"+" "+str(len(words_stemming_snowball)))
print("Lemmatization"+" "+str(len(words_lemmatizing)))


