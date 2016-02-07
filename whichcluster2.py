from scipy.spatial.distance import euclidean
import pandas as pd
from scipy import sparse
import cPickle as pickle
from numpy import array
import numpy
from sklearn.decomposition import RandomizedPCA

def whichcluster(array):
    mu=pd.read_csv('mu.csv').as_matrix()
    distance=[]
    for i in range(mu.shape[0]):
        distance.append(euclidean(array,mu[i]))
    for i, dis in enumerate(distance):
        if dis==min(distance):
            return i

