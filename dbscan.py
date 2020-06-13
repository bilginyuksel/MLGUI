from math import sqrt
import random

# Enum to represent point status
class Status:
    UNCLASSIFIED = "Unclassifed"
    BORDER = "Border Point"
    NOISE = "Noise Point"
    CORE = "Core Point"

# const_dbscan_class_signature = '#ifndef'

# Calculate the distance between two points
def euclidian_distance(point1, point2):

    # Error checking
    if not point1 and not point2 and not len(point1.features) == len(point2.features):
        return -1

    val = 0
    for i in range(len(point1.features)):
        val += (point1.features[i] - point2.features[i])**2
    
    return sqrt(val)
    
    

class Point:

    def __init__(self, features):
        
        self.features = features
        self._status = Status.UNCLASSIFIED
        self._cluster = -1

    def setStatus(self, st):
        self._status = st
    def getStatus(self):
        return self._status

    def getCluster(self):
        return self._cluster

    def setCluster(self, cluster):
        self._cluster = cluster

    def isCore(self):
        return self._status == Status.CORE

    def isClassified(self):
        return not self._status == Status.UNCLASSIFIED

    def to_json(self):
        f = "".join(map(lambda x: str(x)+",", self.features))
        return {'features':f, 'status':self._status, 'cluster':self._cluster}

    def __str__(self):
        return "".join(map(str, self.features))+", "+self._status+", C: "+ str(self._cluster)


class DBSCAN(object):

    def __init__(self, epsilon = 0.3, minPoints = 10):

        self.epsilon = epsilon
        self.minPoints = minPoints
        
        self.data = None
        self.cluster = 0

        self.info = {
            'Cluster':self.cluster,
            'Epsilon':self.epsilon,
            'Min Points':self.minPoints,
            Status.CORE:0,
            Status.BORDER:0,
            Status.NOISE:0,
            Status.UNCLASSIFIED:0
        }

    def _transform(self, X):
        return [Point(i) for i in X]


    def _set_info(self):
        for i in self.data:
            self.info[i.getStatus()]+=1
        self.info['Cluster'] = self.cluster

    def _expandCluster(self, element):

        self.data[element].setCluster(self.cluster)
        self.data[element].setStatus(Status.BORDER)

        neighbors = self._findNeighbors(element)

        if len(neighbors) >= self.minPoints:
            for i in range(len(neighbors)):
                if not self.data[neighbors[i]].isClassified():
                    self._expandCluster(neighbors[i])
            
    def _findNeighbors(self, pos):
        # This function finds the closest points.
        neighbors = []

        for i in range(len(self.data)):
            if  euclidian_distance(self.data[pos], self.data[i]) <= self.epsilon:
                neighbors.append(i)
        return neighbors
        

    def fit(self, data):
        
        self.data = self._transform(data)

        self.cluster = 0

        for i in range(len(self.data)):
            if not self.data[i].isClassified():
                neighbors = self._findNeighbors(i)

                if len(neighbors) < self.minPoints:
                    self.data[i].setStatus(Status.NOISE)
                    continue

                    
                core_point_index = 0
                self.cluster+=1
                for j in range(len(neighbors)):
                    self.data[neighbors[j]].setStatus(Status.BORDER)
                    self.data[neighbors[j]].setCluster(self.cluster)

                    if self.data[neighbors[j]] == self.data[i]: 
                        self.data[i].setStatus(Status.CORE)
                        core_point_index = j

                self.data[neighbors[core_point_index]].setStatus(Status.CORE)
                self.data[neighbors[core_point_index]].setCluster(self.cluster)

                neighbors.pop(core_point_index)

                for j in range(len(neighbors)):
                    self._expandCluster(neighbors[j])
        
        # Set informations
        self._set_info()
        print(self.info)

    

    def predict(self):
        pass



# X, y = generate_blobs_data()
# # X2, y2 = generate_cyclic_data() 

# test = DBSCAN()
# test.fit(X)

# # test2 = DBSCAN()
# # test2.fit(X2)


# model_plot = ModelPlot(test)
# model_plot.plot()

# export_model(test)


# test2 = import_model('DBSCAN.yuksel')
# plot2 = ModelPlot(test2)
# plot2.plot()