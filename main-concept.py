import pandas as pd
import numpy as np
import math
import operator

# Importing data 
data = pd.read_csv('dataset.csv')

print(data.head(10))

# Defining euclidean distance between two data points
def euclideanDistance(data1, data2, length):
    distance = 0
    for x in range(length):
        distance += np.square(data1[x] - data2[x])
    return np.sqrt(distance)

# Defining KNN model
def knn(trainingSet, testInstance, k):
    distances = {}
    sort = {}
    length = testInstance.shape[1]
    # Calculating euclidean distance between each row of training data and test data
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet.iloc[x], length)
        distances[x] = dist[0]
 
    # Sorting them on the basis of distance
    sorted_d = sorted(distances.items(), key=operator.itemgetter(1))
 
    neighbors = []
    
    # Extracting top k neighbors
    for x in range(k):
        neighbors.append(sorted_d[x][0])

    classVotes = {}
    # Calculating the most freq class in the neighbors
    for x in range(len(neighbors)):
        response = trainingSet.iloc[neighbors[x]][-1]
 
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1

    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return(sortedVotes[0][0], neighbors)

testSet = [[89, 6.7, 3, 41]]
test = pd.DataFrame(testSet)

# Setting number of neighbors
k = 1
print('\nWith',k,'Nearest Neighbour')

# Running KNN model
result,neigh = knn(data, test, k)

# Predicted class
print('\nPredicted Class of the datapoint = ', result)

# Nearest neighbor
print('\nNearest Neighbour of the datapoints = ',neigh)