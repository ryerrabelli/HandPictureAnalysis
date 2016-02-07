#################
#PCA decomposition
#################

from scipy.spatial.distance import euclidean
from sklearn.decomposition import PCA
import pandas as pd

def whichcluster(filename):
#file read
    f=open(filename,'r')#read picture information
    arrayPic=pd.read_csv('{}.csv'.format(filename)).as_matrix()
    pca = PCA(n_components=150)
    x=pca.fit(arrayPic).transform()

    arrayMu=pd.read_csv('mu.csv').as_matrix()
    distance=[]
    for i in range(x.shape[0]):
        distance.append(euclidean(x[i],arrayMu))
    for i, dis in enumerate(distance):
        if dis==min(distance):
            return i
    

                    

