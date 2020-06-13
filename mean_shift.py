from random import randint
from math import sqrt

class mean_shift_data:

  def __init__(self, features):

    self.features = features
    self.cluster = -1

  def to_json(self):
    f = "".join(list(map(lambda x: str(x)+",", self.features)))
    return {'features':f, 'cluster':self.cluster}
  

class MeanShift:
  
  def __init__(self, bandwidth=1.5, error = 0.001):
    self.bandwidth = bandwidth
    self.cluster = 0

    self.min_error = error
    self.current_centroid = None
    self.centroids = []
    self.data = None
    
    self.seen = None

    self.info = {
      'Bandwidth':self.bandwidth,
      'Cluster':self.cluster,
      'Min Error':self.min_error,
    }

  def _initialize_centroid(self):
    self.cluster+=1
    element_idx = 0
    for i in self.seen:
      element_idx = i
      break
    # rand_num = randint(0, len(self.data))
    # If this data is not already clustered.
    return self.data[element_idx].features

  def _update_centroid(self):
    total = [0 for _ in range(len(self.current_centroid))]
    count = 0
    for i in range(len(self.data)):
      dist = self._distance(self.current_centroid, self.data[i].features)
      if dist<=self.bandwidth:
        # calculate mean values
        if i in self.seen: self.seen.remove(i)
        count += 1
        self.data[i].cluster = self.cluster
        # self.data[i] 
        for feature in range(len(self.data[i].features)):
          total[feature]+=self.data[i].features[feature]

    for idx in range(len(total)): total[idx]/=count

    return total
    
  def _transform(self, data):
    self.seen = [i for i in range(len(data))]
    return [mean_shift_data(i) for i in data]

  def _distance(self, data1, data2):

    if len(data1) != len(data2):
      raise IndexError()

    dist = 0
    for idx in range(len(data1)):
      dist+= (data1[idx] - data2[idx])**2

    return sqrt(dist)

  def fit(self, data):
    self.data = self._transform(data)

    self.current_centroid = self._initialize_centroid()
    
    error = 1
    iteration = 0
    while len(self.seen) != 0:
      error = 1
      while error > self.min_error:
        iteration += 1
        
        # Calculate the distance between data points and current centroid
        old_centroid = self.current_centroid.copy()
        self.current_centroid = self._update_centroid()

        error = self._distance(old_centroid, self.current_centroid)

      self.centroids.append(self.current_centroid)
      self.current_centroid = self._initialize_centroid()
  
   
    self.info['Cluster'] = self.cluster -1 
    
    print(self.info)

