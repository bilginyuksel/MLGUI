from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton
import sys
from dbscan import DBSCAN
from fuzzy import FCM
from mean_shift import MeanShift

class DbscanDialog(QDialog):

  def __init__(self, data):
    super().__init__()

    self.setWindowTitle("DBSCAN özellikleri")
    self.data = data
    self.model = None
    self.run = False

    self._configure()

  def _configure(self):

    mainLayout = QVBoxLayout()

    hor1 = QHBoxLayout()
    epsilonLabel = QLabel("Epsilon: ")
    self.epsilonLineEdit = QLineEdit("0.3")
    hor1.addWidget(epsilonLabel)
    hor1.addWidget(self.epsilonLineEdit)

    hor2 = QHBoxLayout()
    minPointsLabel = QLabel("Min Points: ")
    self.minPointsLineEdit = QLineEdit("10")
    hor2.addWidget(minPointsLabel)
    hor2.addWidget(self.minPointsLineEdit)

    trainButton = QPushButton("Modeli çalıştır")
    trainButton.clicked.connect(self._run_model)

    mainLayout.addLayout(hor1)
    mainLayout.addLayout(hor2)
    mainLayout.addWidget(trainButton)

    self.setLayout(mainLayout)
    
  def _run_model(self):

    eps = float(self.epsilonLineEdit.text())
    minPoints = int(self.minPointsLineEdit.text())

    self.model = DBSCAN(epsilon=eps, minPoints=minPoints)
    self.model.fit(self.data)
    self.run = True
    self.accept()
    self.close()

class FuzzyDialog(QDialog):

  def __init__(self, data):
    super().__init__()
    self.data = data
    self.setWindowTitle('FCM özellikleri')
    self.model = None

    self._configure()


  def _configure(self):
    mainLayout = QVBoxLayout()

    hor1 = QHBoxLayout()
    cluster = QLabel("Cluster: ")
    self.clusterLineEdit = QLineEdit("2")
    hor1.addWidget(cluster)
    hor1.addWidget(self.clusterLineEdit)

    hor2 = QHBoxLayout()
    membership = QLabel("Membership: ")
    self.membershipLineEdit = QLineEdit("2")
    hor2.addWidget(membership)
    hor2.addWidget(self.membershipLineEdit)

    hor3 = QHBoxLayout()
    error = QLabel("Error Bound: ")
    self.errorLineEdit = QLineEdit("0.001")
    hor3.addWidget(error)
    hor3.addWidget(self.errorLineEdit)

    hor4 = QHBoxLayout()
    max_iter = QLabel("Max iteration: ")
    self.max_iterLineEdit = QLineEdit("100")
    hor4.addWidget(max_iter)
    hor4.addWidget(self.max_iterLineEdit)

    train_button = QPushButton("Modeli çalıştır")
    train_button.clicked.connect(self._run_model)

    mainLayout.addLayout(hor1)
    mainLayout.addLayout(hor2)
    mainLayout.addLayout(hor3)
    mainLayout.addLayout(hor4)
    mainLayout.addWidget(train_button)

    self.setLayout(mainLayout)

  def _run_model(self):
    cluster = int(self.clusterLineEdit.text())
    membership = int(self.membershipLineEdit.text())
    error = float(self.errorLineEdit.text())
    max_iter = int(self.max_iterLineEdit.text())

    self.model = FCM(cluster, m= membership, error= error, max_iter=max_iter)
    self.model.fit(self.data)
    self.accept()
    self.close()

class MeanShiftDialog(QDialog):

  def __init__(self, data):
    super().__init__()

    self.data = data
    self.model = None
    self.setWindowTitle("Mean Shift Özellikleri")

    self._configure()

  def _configure(self):
    
    mainLayout = QVBoxLayout()

    hor1 = QHBoxLayout()
    bandwidthLabel = QLabel("Bandwidth: ")
    self.bandwidthLineEdit = QLineEdit("1.5")
    hor1.addWidget(bandwidthLabel)
    hor1.addWidget(self.bandwidthLineEdit)

    hor2 = QHBoxLayout()
    errorLabel = QLabel("Minimum Error: ")
    self.errorLineEdit = QLineEdit("0.001")
    hor2.addWidget(errorLabel)
    hor2.addWidget(self.errorLineEdit)

    train_button = QPushButton("Modeli çalıştır")
    train_button.clicked.connect(self._run_model)

    mainLayout.addLayout(hor1)
    mainLayout.addLayout(hor2)
    mainLayout.addWidget(train_button)

    self.setLayout(mainLayout)

  def _run_model(self):
    
    bandwidth = float(self.bandwidthLineEdit.text())
    min_error = float(self.errorLineEdit.text())

    self.model = MeanShift(bandwidth=bandwidth, error=min_error)
    self.model.fit(self.data)

    self.accept()
    self.close()

