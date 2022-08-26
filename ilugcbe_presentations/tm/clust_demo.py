#!/usr/bin/env python
"""Demonstration of using NLTK for Clustering

Cluster documents using the NLTK clustering implementations.
"""
from nltk.corpus import brown
#from nltk.feature import *
#from nltk.feature.document import *
from nltk.cluster import *
from nltk.probability import *
#import numarray
from numpy import numarray
###############################################################################
# Functions
###############################################################################
def document_set(classes, items):
    """Create a set of documents from the brown corpus."""

    ds = []                                  # Document set
    for c in classes:
        #for item in brown.items(group=c)[:items]:
        print c
        for item in brown.fileids(categories=c)[:items]:
            print item
            d = brown.raw(item)
            #d = brown.read(item)
            #help(d)
            #d['ITEM'] = item                 # For document based indices
            #d['CLASS'] = c                   # Set the document class
            print d
            ds.append(d)
            
    return ds

def encode_documents(ds):
    """Encode the document in the document sent as word frequency vectors.

    Stores a numarray array object in the FEATURES key of each document
    token. This format is required by NLTK clusterers.
    """
    words = set()              # All words in the document set
    cf = ConditionalFreqDist()
    for d in ds:               # Loop over all documents
        for w in d['WORDS']:
            t = w['TEXT']      # Word text instead of token object
            words.add(t)       # Identify all possible words
            cf[d['ITEM']].inc(t)       # Calculate word frequency

    # Now encode the word frequency vectors
    for d in ds:
        v = [ cf[d['ITEM']].count(w) for w in words ]
        d['FEATURES'] = numarray.array(v)

    return words

###############################################################################
# Demonstration, parts taken from nltk.classifier.naivebayes
###############################################################################
def demo():
    classes = brown.categories()
    print "read document set..."
    ds = document_set(classes,5)       # Take 5 documents from each class

    print "encode the document set..."
    words = encode_documents(ds)

    # Create a clusterer and cluster the data
    print "k-means clustering..."
    clusterer = KMeansClusterer(len(classes), euclidean_distance)
    clusterer.cluster(words, True)
    #clusterer.cluster(ds, True)
    means = clusterer.means()         # Starting points for EM clustering

    # Print out cluster assignments
    print "K-Means Cluster assignments"
    print "---------------------------"
    for i in range(len(ds)):
        print ds[i]['ITEM'], "\t", ds[i]['CLUSTER'], "\t", classes[i / 5]

    # Perform agglomerative clustering, uses cosine distance
    print "GAAC clustering..."
    clusterer = GroupAverageAgglomerativeClusterer(len(classes))
    clusterer.cluster(ds, True)

    # Print out cluster assignments
    print "GAAC Cluster assignments"
    print "------------------------"
    for i in range(len(ds)):
        print ds[i]['ITEM'], "\t", ds[i]['CLUSTER'], "\t", classes[i / 5]

    # Show the dendrogram, note the NLTK method is mispelled!!!!
    #clusterer.dendogram().show()

    # Use EM clustering, performing feature reduction using SVD
    print "EM clustering..."
    print "Identifying initial cluster means..."
    clusterer = KMeansClusterer(len(classes), euclidean_distance, 
            svd_dimensions = 1)
    clusterer.cluster(ds, False)
    means = clusterer.means()         # Starting points for EM clustering
    print "Performing EM clustering..."
    clusterer = ExpectationMaximizationClusterer(means, svd_dimensions = 1)
    clusterer.cluster(ds, True)

    # Print out cluster assignments
    print "EM Cluster assignments"
    print "----------------------"
    for i in range(len(ds)):
        print ds[i]['ITEM'], "\t", ds[i]['CLUSTER'], "\t", classes[i / 5]

if __name__ == '__main__': demo()

#http://webcache.googleusercontent.com/search?q=cache:aVwJt0Bq_5YJ:https://www.mscs.mu.edu/~cstruble/moodle/mod/resource/view.php%3Finpopup%3Dtrue%26id%3D157+def+encode_documents%28ds%29:&cd=1&hl=en&ct=clnk&gl=in
