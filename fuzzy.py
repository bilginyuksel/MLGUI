"""

declare centroid number
declare error boundary
declare max iterations
declare fuzzy m -> number membership value usually 2

Calculate gammas. 
"""
from random import random
from math import sqrt


# If this makes you trouble, just create gamma 2D arrays to track gamma values.
class fcm_data:

  def __init__(self, data, n_cluster, gamma = None):
    self.data = data
    if not gamma:
      self.gamma = [random() for _ in range(n_cluster)]
    else: self.gamma = gamma
    # self.gamma = gamma
    self.cluster = -1
  def update(self, pos, val):
    # Update new gamma value for cluster->pos
    self.gamma[pos] = val

  def centroid_point(self, dpos, gpos):
    # print("data: %f, gamma: %f" % (self.data[dpos], self.gamma[gpos]))
    return self.data[dpos]*self.gamma[gpos]

  def clusterize(self):

    max_idx = 0
    max_val = self.gamma[max_idx]

    for i in range(1, len(self.gamma)):
      if max_val < self.gamma[i]:
        max_val = self.gamma[i]
        max_idx = i
    
    self.cluster = max_idx
    
  def to_json(self):
    f = "".join(map(lambda x: str(x)+",", self.data))
    g = "".join(map(lambda x: str(x)+",", self.gamma))
    return {'data':f, 'gamma':g, 'cluster':self.cluster}

    

class FCM(object):

  def __init__(self, centroid_length, m=2, error=0.001, max_iter=100):
    self.m = m
    self.min_error = error
    self.max_iter = max_iter
    self.n_cluster = centroid_length
    
    self.error = -1
    self.feature_size = 0
    self.fcm_objects = None
    self.fcm_clusters = None

    self.info = {
      'Membership':self.m,
      'Error Bound':self.min_error,
      'Actual Error':self.error,
      'Max iteration':self.max_iter,
      'Cluster':self.n_cluster,
    }

    
  def _set_info(self):
    
    counts = [0 for _ in range(self.n_cluster)]
    # calculate clusters elements
    for i in range(len(self.fcm_objects)):
      self.fcm_objects[i].clusterize()
      counts[self.fcm_objects[i].cluster] += 1
    
    for i in range(len(counts)):
      key = "Cluster_"+str(i+1)
      self.info[key] = counts[i]
    
    self.info['Actual Error'] = self.error

  def _update_centroids(self):
    clusters = [[0 for _ in range(len(self.fcm_objects[0].data))] for _ in range(self.n_cluster)]
    for cluster in range(self.n_cluster):
      # To calculate clusters[cluster], i need to traverse every data.
      for feature in range(self.feature_size):
          gamma = 0
          for obj in self.fcm_objects:
            clusters[cluster][feature] += obj.centroid_point(feature, cluster)
            gamma += obj.gamma[cluster]
          clusters[cluster][feature]/= gamma
    return clusters

  def _distance(self, data1, data2):
    
    if len(data1) != len(data2):
      raise IndexError()
    
    total = 0
    for i in range(len(data1)):
      total += (data1[i] - data2[i])**2

    return sqrt(total)    
      
  def _error(self, old_centroid, centroid):
    error = 0
    for i in range(len(old_centroid)):
      for j in range(i+1, len(old_centroid)):
        error += self._distance(old_centroid[i], centroid[j])
      
    return error


  def _update_gamma_values(self):
    
    for c in range(len(self.fcm_clusters)):
      for idx in range(len(self.fcm_objects)):
        distance_between_cluster_which_will_update = self._distance(self.fcm_clusters[c], self.fcm_objects[idx].data)
        val = 0
        for cluster in range(len(self.fcm_clusters)):
          tmp = self._distance(self.fcm_clusters[cluster], self.fcm_objects[idx].data)
          val += (distance_between_cluster_which_will_update**2) / (tmp**2)
        val = val**(1/(self.m - 1))
        self.fcm_objects[idx].update(c, (1/val)) # 1/[val^(1/m-1)]

  def _transform(self, data):
    self.feature_size = len(data[0])
    return [fcm_data(i, self.n_cluster) for i in data]


  def fit(self, data):

    self.fcm_objects = self._transform(data)
    self.fcm_clusters = self._update_centroids()

    
    error = 1
    iteration = 1
    while error > self.min_error and iteration<self.max_iter:
      self._update_gamma_values()
      old_centroids = self.fcm_clusters.copy()
      self.fcm_clusters = self._update_centroids()
      error = self._error(old_centroids, self.fcm_clusters)
      iteration+=1

    self.error = error
    # print(self.error)
    # print(iteration)
    # print(self.fcm_clusters)

    self._set_info()


    # for i in self.fcm_objects:
      # print("data:",i.data, "gammas:",i.gamma, "cluster:",i.cluster)
    print(self.info)



# fuzzy = FCM(2)
# x, y = generate_blobs_data()
# # fuzzy.fit([[1,3], [2,5], [4,8], [7,9]])
# fuzzy.fit(x)