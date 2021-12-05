import os, email, nltk
import cPickle as pickle

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from pprint import pprint


def initial_result(posting_list, word):
	newList = list()
	if  word not in posting_list:
		return newList
	for var in posting_list[word]:
		if isinstance(var, basestring):
			newList.append(var)
	return newList

def set_union(posting_list, result_list, word):
	first = set(initial_result(posting_list, word))
	second = set(result_list)
	return first.union(second)

def set_intersection(posting_list, result_list, word):
	first = set(initial_result(posting_list, word))
	second = set(result_list)
	return first.intersection(second)

def set_difference(posting_list, result_list, word):
	first = set(initial_result(posting_list, word))
	second = set(result_list)
	return second.difference(first)

def lemmatizing(wnl, processed_sentence):
	filtered = list()
	for word in processed_sentence:

			if wnl.lemmatize(word)!=word:
				filtered.append(wnl.lemmatize(word))

			elif wnl.lemmatize(word,'a')!=word:
				filtered.append(wnl.lemmatize(word,'a'))

			elif wnl.lemmatize(word,'r')!=word:
				filtered.append(wnl.lemmatize(word,'r'))

			elif wnl.lemmatize(word,'v')!=word:
				filtered.append(wnl.lemmatize(word,'v'))

			else:
				filtered.append(word)

	return filtered

def dump_file(file, path):
	f = open('dump.txt', "a+")
	document = open(path+'/'+file,'r')
	message = email.message_from_file(document)
	items_list =  message.get_payload()
	items_list = unicode(items_list, errors = 'ignore')
	f.write(items_list)


if __name__ == "__main__":

	stop_words = set(stopwords.words('english'))
	symbols =  ['.', ')', '[', ']', '"', "'", '?', '!', '{', '}', '*', ',',  ':', ';', '(']
	stop_words |= set(symbols)
	wnl = WordNetLemmatizer()

	corpus_frequency = dict()
	posting_list = dict()

	current_path = os.getcwd()+ '/alt.atheism'
	for file in os.listdir(current_path):
		document = open(current_path+'/'+file,'r')
		message = email.message_from_file(document) # Return a message object structure tree from an open file object
		items_list =  message.get_payload() # email.message.Message.get_payload() returns a list with one item for each part.
		items_list = items_list.decode('utf-8','ignore') # Decode utf-8

		temp = word_tokenize(items_list)

		processed_sentence = []
		for w in temp:
		    if w.lower() not in stop_words:
		        processed_sentence.append(w.lower())

		processed_sentence = lemmatizing(wnl,processed_sentence)

		document_frequency = {}
		for word in processed_sentence:
			if word in corpus_frequency:
				corpus_frequency[word] = corpus_frequency[word] + 1
			else:
				corpus_frequency[word] = 1

			if word in document_frequency:
				document_frequency[word] = document_frequency[word] + 1
			else:
				document_frequency[word] = 1

			if word not in posting_list:
				posting_list[word] = []

			if file not in posting_list[word]:
				posting_list[word].append(file)
				posting_list[word].append(document_frequency[word])


	query = raw_input("Input Boolean query: ") # Dump file for the query 'atheism not tyrant and original'.

	booleanOperations = {"and","not","or"}
	tokenized_query = word_tokenize(query)
	processed_query = list()

	for word in tokenized_query:
	    if (word.lower() not in stop_words) or (word.lower() in booleanOperations):
	        processed_query.append(word.lower())
	processed_query = lemmatizing(wnl, processed_query)

	final_result = dict()
	i = 0

	while i < len(processed_query):

		if i == 0:
			final_result = initial_result(posting_list,processed_query[0])
			i=i+1
			continue

		if processed_query[i] in booleanOperations:

			if processed_query[i] == "and":
				final_result = set_intersection(posting_list,final_result,processed_query[i+1])
				i = i+1

			elif processed_query[i] == "or":
				final_result = set_union(posting_list,final_result,processed_query[i+1])
				i = i+1

			else:
				final_result = set_difference(posting_list,final_result,processed_query[i+1])
				i = i+1

		else:
			final_result = set_union(posting_list,final_result,processed_query[i])

		i = i+1

	print "Search results: ", len(final_result)

	# Dump results
	for result in final_result:
	 	dump_file(result,current_path)
