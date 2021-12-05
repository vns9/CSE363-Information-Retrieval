import numpy as np
from scipy.sparse import *

def column(M, i):
    
    return [r[i] for r in M]

def HITS(G):

    N = G.shape[1]
    Gt = np.transpose(G)
    hubScoresList = list()
    for i in range(N):
        hubScoresList.append(1)
    hubScores = np.array(hubScoresList)
    authorityScores = np.dot(Gt, hubScores)
    hubScores = np.dot(G, authorityScores)
    print("Authority Scores:") 
    print((authorityScores*1.0)/sum(authorityScores))
    print("Hub Scores: ")
    print((hubScores*1.0)/sum(hubScores))

def WeightedPageRank(G, alpha = 0.15, SATURATION = .001):
    
    N = G.shape[1]
    Matrix = csc_matrix(G)
    rowsums = np.array(Matrix.sum(1))[:,0]
    rowi, columni = Matrix.nonzero()
    Matrix.data /= rowsums[rowi]
    link_sink = rowsums==0
    rprev, r = np.zeros(N), np.ones(N)
    # PageRank Iterations
    while np.sum(np.abs(r-rprev)) >= SATURATION:
        rprev = r.copy()
        for i in xrange(0,N):
            inline = np.array(Matrix[:,i].todense())[:,0]
            sinki = (link_sink*1.0) / N
            transitioni = (np.ones(N)*1.0) / N
            # Weighted Page Rank Expression
            r[i] = rprev.dot(transitioni*(1-alpha)*G[i]+(inline+sinki)*alpha) 
    print("Weighted PageRank scores:") 
    print(r/sum(r))
    
# G represents adjacency matrix of a directed web graph
G = np.array(
            [
            [1,0,0,0,0,0,1],
            [1,1,0,0,0,0,0],
            [1,1,1,0,0,0,0],
            [1,1,0,1,0,0,0],
            [1,1,0,0,1,0,0],
            [1,1,0,0,0,0,0],
            [1,1,0,0,0,1,1]
            ]
            )

WeightedPageRank(G, alpha=0.15) # "alpha" represents weight in weighted page rank
HITS(G) # Calculate Hubs and Authority scores