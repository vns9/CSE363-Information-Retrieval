import nltk, os, string, numpy, warnings
from sklearn import metrics, preprocessing, decomposition, feature_extraction
import matplotlib.pyplot as plt

# Custom K-Means model
class KMeansClustering:
    def __init__(self, k, total_iterations = 500):
        self.k = k
        self.total_iterations = total_iterations
        
    def initialize(self, input_data):
        self.centroids = input_data[numpy.random.permutation(input_data.shape[0])[:self.k]]
        return self.centroids

    def assign(self, input_data):
        if input_data.ndim == 1:
            input_data = input_data.reshape(-1, 1)
        self.labels = numpy.argmin(metrics.pairwise_distances(input_data, self.centroids, metric = 'euclidean'), axis = 1)
        return  self.labels
    
    def update(self, input_data):
        self.centroids = numpy.array([input_data[self.labels == i].mean(axis = 0) for i in range(self.k)])
        return self.centroids
    
    def predict(self, input_data):
        return self.assign(input_data)
    
    # Fit model, driver code.
    def fit(self, input_data):
        self.centroids = self.initialize(input_data)
        for _ in range(self.total_iterations):
            self.labels = self.assign(input_data)
            if (self.centroids).all() == (self.update(input_data)).all():
                break
            else:
                self.centroids = self.update(input_data)          
        return self 


data = []
dataset = "20NewsGroups"

for repository in os.listdir(dataset+"/"):
    # ".DS_Store" file stores the custom attributes of its containing folder in Mac OS X - https://en.wikipedia.org/wiki/.DS_Store
    if repository==".DS_Store":
        pass
    else:
        for document in os.listdir(dataset+"/"+repository+"/"):
            file = open(dataset+"/"+repository+"/"+document)
            # Ignore UTF-8 conversion changes - https://docs.pylonsproject.org/projects/pylons-webframework/en/latest/tutorials/understanding_unicode.html
            data.append(unicode(file.read(), errors='ignore'))
            file.close()

sklearn_tfidf_vectorizer = feature_extraction.text.TfidfVectorizer(stop_words = 'english', max_features = 200) 
tf_idf = sklearn_tfidf_vectorizer.fit_transform(data)
normalized_tfidf = preprocessing.normalize(tf_idf)

# Use builtin Principal Component Analysis for dimensionality reduction into 2D Space for better visualization
pca = decomposition.PCA(n_components = 2)
Y = pca.fit_transform(normalized_tfidf.toarray())
model = KMeansClustering(20, 1000)
fitted = model.fit(Y)
predicted = model.predict(Y)

# Suppress future warnings in matplotlib - https://github.com/matplotlib/matplotlib/issues/5209 
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    plt.title('Text Clustering 20 Newsgroups dataset')
    plt.scatter(Y[:, 0], Y[:, 1], c=predicted, s=30)
    plt.scatter(fitted.centroids[:, 0], fitted.centroids[:, 1], s=100, c='black')
    plt.show()