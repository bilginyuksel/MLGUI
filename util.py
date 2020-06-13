from sklearn.datasets import make_blobs, make_circles, make_s_curve
from sklearn.preprocessing import StandardScaler
from export import ModelExport, ModelImport

def generate_blobs_data(n_samples = 750, centers = None, cluster_std = 0.4, random_state = 0):
    
    if not centers:
        centers = [
        [1, 1],
        [-1, -1],
        [1, -1]]

    data, labels = make_blobs(n_samples = n_samples, centers=centers, cluster_std = cluster_std, random_state= random_state)   
    data = StandardScaler().fit_transform(data)
    

    
    return data, labels

def generate_friedman_data(n_samples = 750, n_features= 2):
    data, labels = make_s_curve(n_samples= n_samples)
    data = StandardScaler().fit_transform(data)

    return data, labels

def generate_cyclic_data(n_samples = 750, factor=0.3, noise=0.1):
   

    data, labels = make_circles(n_samples= n_samples, factor=0.3, noise=0.1)
    data = StandardScaler().fit_transform(data)

    return data, labels

def export_model(transform_model, filename=None, extension = 1):

    # Get important feature according to model
    # For DBSCAN, self.data is the most important component
    # We have to right it to a file and read it afterwards.
    model = ModelExport(model = transform_model,filename= filename, extension= extension)
    model.export()


def import_model(filename):
    imported_model = ModelImport(filename)
    imported_model.import_()
    model = imported_model.model
    return model