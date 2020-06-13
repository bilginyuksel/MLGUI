from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton
import sys
from dbscan import DBSCAN

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

