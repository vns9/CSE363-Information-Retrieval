"""Collect the word statistics and check whether there exists a Zipf's Law there or not."""

__author__    =  "Venkat S. Narayana"
__contact__   =  "narayana.svenkat.cse17@iitbhu.ac.in"
__date__      =  "Jan 25, 2020"


import os
import re
import math
import nltk
import datetime
import string

import matplotlib.pyplot as plt
from operator import itemgetter



path = '/Users/narayanavenkat/desktop/20news-18828/'
words_frequency = dict()

symbols = re.escape(string.punctuation)

#a = datetime.datetime.now()

for root, d_names, f_names in os.walk(path):
    print("New Directory!")
    for f_name in f_names:
        openf = open(root + "/"+ f_name, 'rb')
        file_string = openf.readlines()
        #words = re.findall(r'(\b[A-Za-z][a-z]{2,9}\b)', file_string)
        for line in file_string:
            line = re.sub(r'['+symbols+']', '',str(line))
            words = line.split()
            for word in words:
                word = word.lower()
#                words_stemming_porter.add(stemmer.stem(word))
#                words_lemmatizing.add(lemmatizer.lemmatize(word))
#                words_stemming_snowball.add(sstemmer.stem(word))
                if word in words_frequency:
                    words_frequency[word]+=1
                else:
                    words_frequency[word]=1
                
                
##TASK 2
#print("Number of unique words")
#print("Raw Corpus"+" "+str(len(words_frequency)))
#print("Porter Stemmer"+" "+str(len(words_stemming_porter)))
#print("SnowBall Stemmer"+" "+str(len(words_stemming_snowball)))
#print("Lemmatization"+" "+str(len(words_lemmatizing)))

counter=0
rank_list = list()
freq_list = list()

#TASK 1
for key, value in reversed(sorted(words_frequency.items(), key = itemgetter(1))):
    counter+=1
    rank_list.append(math.log10(counter))
    freq_list.append(math.log10(value))
    
#b = datetime.datetime.now()
#print("Total time taken: "),
#print(b-a)
    
plt.plot(rank_list, freq_list)
plt.xlabel('log(rank)')
plt.ylabel('log(frequency)')
plt.ylim(0,6)
plt.xlim(0,5)
plt.title('Verification of Zipf\'s Law in Newsgroup 20 Dataset')
plt.show()
