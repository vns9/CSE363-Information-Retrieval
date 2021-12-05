import os, nltk
import cPickle as pickle

from pprint import pprint
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

dataset = "20 Newsgroups"
directories = os.listdir(dataset)
processed_dataset = list()
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()
folder = directories[0] #We can choose any directory. Here, we chose 'alt.atheism'


for document in os.listdir(dataset+"/"+folder+"/"):

        file = open(dataset+"/"+folder+"/"+document)
        file_string = file.read()
        file.close()

        words = word_tokenize(file_string)
        for word in words:
            word = word.lower()
        words = [word for word in words if not word in stop_words and word.isalpha()]
        for word in words:
            word = stemmer.stem(word)

        processed_dataset.append(words)


index = dict()
document_frequency = dict()
corpus_frequency = dict()

for document in range(0,len(processed_dataset)):
        temp = dict()
        for word in processed_dataset[document]:
                if word not in temp:
                        temp[word] = 1
                else:
                        temp[word]+=1
        for word in temp:
                if word not in index:
                        index[word] = []
                        document_frequency[word] = 0
                        corpus_frequency[word] = 0
                index[word].append((document,temp[word]))
                document_frequency[word] += 1
                corpus_frequency[word] += temp[word]

keys=index.keys()
findex=dict()
for key in keys:
        findex[(key,document_frequency[key])]= index[key]

with open('dump.txt', 'w') as out:
    pprint(findex, stream=out)

#print(findex)
