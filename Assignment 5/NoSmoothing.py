import os, nltk
import cPickle as pickle
import json

from pprint import pprint
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

dataset = "20Newsgroups"
directories = os.listdir(dataset)
directories.sort()
processed_dataset = list()
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()
folder = directories[2]
given_string = "computer graphics"
folder_prob = dict()


for document in os.listdir(dataset+"/"+folder+"/"):
    processed_dataset *= 0 
    file = open(dataset+"/"+folder+"/"+document)
    file_string = file.read()
    file.close()

    words = word_tokenize(str(file_string))
    for word in words:
        word = word.lower()
    words = [word for word in words if not word in stop_words and word.isalpha()]
    for word in words:
        word = stemmer.stem(word)

    processed_dataset.append(words)

    temp = dict()
    for doc in range(0,len(processed_dataset)):
            for word in processed_dataset[doc]:
                    if word not in temp:
                            temp[word] = 1
                    else:
                            temp[word]+=1

    total_frequency = sum(temp.values())
    ans=1.0
    for word in given_string.split():
        if word in temp:
            ans*=temp[word]
            ans/=total_frequency
        else:
            ans=0
    folder_prob[document] = ans
sfp = sorted(folder_prob.items(), key=lambda x: x[1])
#pprint(sfp)
with open('result.json', 'w') as fp:
    json.dump(sfp, fp)