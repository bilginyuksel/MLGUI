from dbscan import DBSCAN
from util import generate_cyclic_data, generate_blobs_data, export_model, import_model
from plot import ModelPlot

X, y = generate_blobs_data()
# X2, y2 = generate_cyclic_data() 

test = DBSCAN()
test.fit(X)

# test2 = DBSCAN()
# test2.fit(X2)


model_plot = ModelPlot(test)
model_plot.plot()

export_model(test)


test2 = import_model('DBSCAN.yuksel')
print(test2)

plot2 = ModelPlot(test2)
plot2.plot()