import json
import dbscan
import fuzzy
# json.loads

class ModelExport(object):

    def __init__(self, model = None, filename = None, extension = 1):
        self.model = model
        self.model_name = type(model).__name__
        
        self.models = {
            'DBSCAN': self._dbscan,
            'FCM':self._fuzzy
        }

        self.extension = {
            1:'.yuksel',
            2:'.bayram'
        }

        if not filename:
            self.filename = self.model_name + self.extension[extension]
        else: self.filename = str(filename) + self.extension[extension]

    def export(self):
        self.models[self.model_name]()
        

    def _fuzzy(self):
        
        with open(self.filename, 'w') as f:
            f.write(self.model_name)
            f.write("\n")
            # Write model data
            f.write(json.dumps(self.model.info))
            f.write("\n")

            # Write points data
            for i in self.model.fcm_objects:
                f.write(json.dumps(i.to_json()))
                f.write("\n")
            f.write(json.dumps(self.model.fcm_clusters))

    def _dbscan(self):
        with open(self.filename, 'w') as f:
            # First write title to know when reading
            f.write(self.model_name)
            f.write("\n")
            # Then write model data
            f.write(json.dumps(self.model.info))
            f.write("\n")

            # Write points data
            for i in self.model.data:
                f.write(json.dumps(i.to_json()))
                f.write("\n")
            

class ModelImport(object):

    def __init__(self, filename):
        fs = filename.split('.')
        self.filename = filename
        self.extension = fs[-1]

        if self.extension!='yuksel' and self.extension!='bayram':
            raise Exception()

        self.models = {
            'DBSCAN':self._dbscan,
            'FCM': self._fuzzy
        }

    
    def import_(self):

        model_name = None
        model_info = None

        with open(self.filename, 'r') as f:
            data = f.read().split("\n")
            model_name = data[0]
            model_info = json.loads(data[1])

        # Sometimes it can be empty elements at the back
        if data[-1]=='': data.pop()

        self.model = self.models[model_name](model_info, data[2:])
        return self.model

    def _fuzzy(self, info, data):

        fuzzy_data_array = []

        for i in range(2, len(data)-1):
            fcm_object_dict = json.loads(data[i])
            obj_data = fcm_object_dict['data']
            obj_gamma = fcm_object_dict['gamma']
            obj_cluster = fcm_object_dict['cluster']

            splitted_obj_data = obj_data.split(",")
            if splitted_obj_data[-1]=='': splitted_obj_data.pop()
            clean_obj_data = list(map(float, splitted_obj_data))

            splitted_obj_gamma = obj_gamma.split(",")
            if splitted_obj_gamma[-1]=='':splitted_obj_gamma.pop()
            clean_obj_gamma = list(map(float, splitted_obj_gamma))

            tmp = fuzzy.fcm_data(clean_obj_data, -1, clean_obj_gamma)
            tmp.cluster = obj_cluster

            fuzzy_data_array.append(tmp)
        
        fuzzy_object = fuzzy.FCM(centroid_length= info['Cluster'], error= info['Error Bound'], m= info['Membership'], max_iter= info['Max iteration'])
        fuzzy_object.fcm_objects = fuzzy_data_array
        fuzzy_object.fcm_clusters = json.loads(data[-1])
        fuzzy_object.info = info
        fuzzy_object.error = info['Actual Error']

        return fuzzy_object

    def _dbscan(self, info, data):

        dbscan_data_array = []
        
    
        arrays = data

        for i in range(2, len(arrays)):
            # Load json points and convert them to actual point objects
            point_dictionary = json.loads(arrays[i])
            features = point_dictionary['features']
            status = point_dictionary['status']
            cluster = point_dictionary['cluster']

            splitted_features = features.split(",")
            if splitted_features[-1]=='': splitted_features.pop()
            clean_features = list(map(float, splitted_features))
            tmp_point = dbscan.Point(clean_features)
            tmp_point.setCluster(cluster)
            tmp_point.setStatus(status)
            dbscan_data_array.append(tmp_point)
        
        dbscan_object = dbscan.DBSCAN(epsilon= info['Epsilon'], minPoints= info['Min Points'])
        dbscan_object.data = dbscan_data_array
        dbscan_object.info = info
        dbscan_object.cluster = info['Cluster']
        

        return dbscan_object
            



