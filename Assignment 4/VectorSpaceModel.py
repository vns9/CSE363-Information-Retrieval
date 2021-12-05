import nltk, os, email, cPickle, math

from collections import defaultdict

"""
	The defaultdict tool is a container in the collections class of Python.
    It's similar to the usual dictionary (dict) container.
	Only difference being that a defaultdict will have a default value if that key has not been set yet.
"""

total_files = 200
inverted_index = defaultdict(list)
total_document_vectors = list()
document_frequency = dict()

def stemming(document_text):
	tokens = nltk.word_tokenize(document_text)
	porterStemmer = nltk.stem.PorterStemmer()
	ans = list()
	for word in tokens:
	        ans.append(porterStemmer.stem(word))
	return ans

def DOT(a, b):
	if len(a) > len(b):
	        temp = a
	        a = b
	        b = temp
	keys_a = a.keys()
	keys_b = b.keys()
	val = 0
	for key in keys_a:
	        if key in keys_b:
	        	val = val + a[key] * b[key]
	return val

def read_all_documents():
	for doc_id in range(total_files+1):
       		doc_text = document_string(doc_id)
        	token_list = stemming(doc_text)
        	v = generateTF(token_list)
        	total_document_vectors.append(v)

def document_string(doc_id):
	files_text = open("Dataset/" + str(doc_id)).read()
	files_text = unicode(str(files_text), errors='replace') # Decode utf-8
	return files_text

def inverted_index_all_documents():
	count = 0
	for document_vector in total_document_vectors:
	        for word in document_vector:
        		inverted_index[word].append(count)
        	count += 1

def input_query_to_vector(input_query):
	TFdict = dict()
	for token in input_query:
        	if token in TFdict:
        		TFdict[token] += 1.0
        	else:
        		TFdict[token] = 1.0
	return TFdict

def TFIDFvectorize():
	length = 0.0
	for document_vector in total_document_vectors:
        	for word in document_vector:
        		frequency = document_vector[word]
        		score = TFIDFscore(word, frequency)
    			document_vector[word] = score
        		length += score ** 2
        	length = math.sqrt(length)
        	for word in document_vector:
        		document_vector[word] /= length

def TFIDFquery(query):
	length = 0.0
	for word in query:
		frequency = query[word]
   		if word in document_frequency:
        		query[word] = TFIDFscore(word, frequency)
        	else:
        		query[word] = math.log(1 + frequency) * math.log(total_files+1)
        	length = length + query[word] ** 2
	length = math.sqrt(length)
	if length != 0:
	        for word in query:
        		query[word] = query[word]/length

def TFIDFscore(word, frequency):
	return math.log(1 + frequency) * math.log((total_files+1) / document_frequency[word])

def generateTF(tokens):
	TF = dict()
	global document_frequency
	for word in tokens:
	        if word in TF:
        		TF[word] += 1
	        else:
        		TF[word] = 1
        		if word in document_frequency:
					document_frequency[word] += 1
        		else:
					document_frequency[word] = 1
	return TF

def search_results(query):
	ans = list()
	for doc_id in range(total_files+1):
	        similarity = DOT(query, total_document_vectors[doc_id])
        	ans.append((doc_id, similarity))
        ans = sorted(ans, key=lambda x: x[1], reverse = True)
	return ans

read_all_documents()

inverted_index_all_documents()

TFIDFvectorize()

while True:
	query = raw_input("Enter search query:")
	token_list = stemming(query)
	query_vector = input_query_to_vector(token_list)
	TFIDFquery(query_vector)
	result = search_results(query_vector)
	final_result = result[:20]
	for document in final_result:
		print(str(document[0]))
