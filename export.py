import json
import dbscan
# json.loads

class ModelExport(object):

    def __init__(self, model = None, filename = None, extent = 1):
        self.model = model
        self.model_name = type(model).__name__
        
        self.models = {
            'DBSCAN': self._dbscan,
        }

        self.extent = {
            1:'.yuksel',
            2:'.bayram'
        }

        if not filename:
            self.filename = self.model_name + self.extent[extent]
        else: self.filename = filename + self.extent[extent]

    def export(self):
        self.models[self.model_name]()
        


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
        self.extent = fs[-1]

        if self.extent!='yuksel' and self.extent!='bayram':
            raise Exception()

        self.models = {
            'DBSCAN':self._dbscan
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
            



