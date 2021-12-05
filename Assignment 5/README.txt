Information Retrieval (CSE - 363)
Assignment #5: Implement Language Modelling.


Name: Venkat Shanmukha Narayana
Roll number: 17075036

Python3 libraries used: os, nltk

Dataset URL: http://qwone.com/~jason/20Newsgroups/20news-18828.tar.gz

Instructions to execute:

Since Unigram is experimentally found to work good for IR, I implemented 2 versions of Unigram Model,

1. Unigram Language Model without smoothing
    1. Execute the file "NoSmoothing.py" to determine the probability of a given input sentence for given document in the folder.
    2. You can change the input sentence variable, "given_string" in "NoSmoothing.py" file.
    3. You can choose any folder, here we choose "comp.graphics".

2. Unigram Language Model with smoothing
    1. Execute the file "Smoothing.py" to determine the probability of a given input sentence for given document in the folder.
    2. You can change the input sentence variable, "given_string" in "Smoothing.py" file.
    3. You can choose any folder, here we choose "comp.graphics".
    4. I implemented Add 1 smoothing here - https://en.wikipedia.org/wiki/Additive_smoothing

The results will dumped into 'result.json' file.
The folder 'results' has previously dumped results.