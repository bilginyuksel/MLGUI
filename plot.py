import matplotlib.pyplot as plt
from collections import defaultdict
from random import choice

class ModelPlot(object):

    

    def __init__(self, model):
        self.model = model
        self.features_length = 2

        self.modelset = {
        'DBSCAN':self._dbscan,
        'Gaussian':None,
        'MeanShift':self._mean_shift,
        'FCM': self._fuzzy
        }
        # We assume data is 2D 
        # We can check data here
        # If user tries to plot another model just raise Exception
        if not type(self.model).__name__ in self.modelset:
            raise TypeError()

        if self.features_length>2:
            raise Exception()
        
        self.colors = {}
        for j in range(100):
            hexcode = ['#']
            for i in range(6):
                hexcode.append(choice("0123456789ABCDEF"))
            self.colors[j+1] = "".join(hexcode)
        self.colors[-1] = '#000000'



    def plot(self):

        self.modelset[type(self.model).__name__]()


    def _mean_shift(self):

        color_data_x = defaultdict(list)
        color_data_y = defaultdict(list)

        for i in self.model.data:
            color_data_x[i.cluster].append(i.features[0])
            color_data_y[i.cluster].append(i.features[1])

        for i in color_data_x.keys():
            plt.scatter(color_data_x[i], color_data_y[i], c= self.colors[i])
        
        plt.title("Mean Shift Clustering")
        plt.show()

    def _fuzzy(self):
        
        color_data_x = defaultdict(list)
        color_data_y = defaultdict(list)

        for i in self.model.fcm_objects:
            color_data_x[i.cluster].append(i.data[0])
            color_data_y[i.cluster].append(i.data[1])

        for i in color_data_x.keys():
            plt.scatter(color_data_x[i], color_data_y[i], color= self.colors[i+1])
        
        plt.title("Fuzzy Means Clustering")
        plt.show()


    def _dbscan(self):
        
        color_data_x = defaultdict(list)
        color_data_y = defaultdict(list)
        for i in self.model.data:
            color_data_x[i.getCluster()].append(i.features[0])
            color_data_y[i.getCluster()].append(i.features[1])

        
        # plt.scatter(i.features[0], i.features[1],
        # color = self.colors[i.getCluster()], s=200 if i.isCore() else 18,
        # marker= "s" if i.isCore() else "o")
        for i in color_data_x.keys():
            plt.scatter(color_data_x[i], color_data_y[i], color= self.colors[i])

        plt.title("DBSCAN Clustering")
        plt.show()


def easy_plot_data(data):
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    plt.scatter(x, y)
    plt.title("İşlenmemiş Veri")
    plt.show()