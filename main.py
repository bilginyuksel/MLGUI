from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QFileDialog, QLabel
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import (
    QColor, QPalette, QFont
)
import sys
from util import generate_blobs_data, generate_cyclic_data, generate_friedman_data, import_model
from plot import ModelPlot, easy_plot_data
# from dbscan import DBSCAN
from algorithm_dialogs import DbscanDialog

from export_dialog import ExportDialog


class Window(QWidget):

    def __init__(self, parent=None, flags= Qt.WindowFlags()):
        super().__init__(parent = parent, flags = flags)

        self.setWindowTitle("Yüksel ve Bayram Unsupervised ML")
        self._configuration()

        self.data = []
        self.labels = None
        self.model = None
    
    def _configuration(self):
        
        self.mainVerticalBox = QVBoxLayout()
        
        dialogButton = QPushButton("Veri dosyası seç...")
        dialogButton.clicked.connect(self._chooseFile)
        

        sample_label = QLabel("Örnek datalardan birisini kullanmak için tıklayınız")
        sample_1_button = QPushButton("Örnek 1")
        sample_1_button.clicked.connect(self._sample1_data_button)
        sample_2_button = QPushButton("Örnek 2")
        sample_2_button.clicked.connect(self._sample2_data_button)
        sample_3_button = QPushButton("Örnek 3")
        sample_3_button.clicked.connect(self._sample3_data_button)
        sampleHorizontalBox = QHBoxLayout()
        sampleHorizontalBox.addWidget(sample_label)
        sampleHorizontalBox.addWidget(sample_1_button)
        sampleHorizontalBox.addWidget(sample_2_button)
        sampleHorizontalBox.addWidget(sample_3_button)


        # Visualize data file if it has 2 dimensions
        # For better visualization capsule push button with horizontal box
        self.plotRowDataButton = QPushButton("Ham veriyi görselleştir.")
        self.plotRowDataButton.clicked.connect(self._plot_raw_data)
        plotHorizontalBox = QHBoxLayout()
        plotHorizontalBox.addStretch()
        plotHorizontalBox.addWidget(self.plotRowDataButton)
        plotHorizontalBox.addStretch()

        
        # To show last chosen data file,
        # Show user what he choose (sample1, sample2, anydatafile)
        self.lastFileLabel = QLabel("Veri dosyası seçilmedi.")


        # Choose any button to run algorithm
        # You can run every algorithm
        algoLabel = QLabel("Aşağıdaki algoritmalardan eğitmek istediğinizi seçiniz.")
        dbscanButton = QPushButton("DBSCAN")
        dbscanButton.clicked.connect(self._run_dbscan)
        fuzzyMeansButton = QPushButton("Fuzzy Means")
        firstHalf = QHBoxLayout()
        firstHalf.addWidget(dbscanButton)
        firstHalf.addWidget(fuzzyMeansButton)

        gaussianButton = QPushButton("Gaussian")
        meanShiftButton = QPushButton("Mean Shift")
        secondHalf = QHBoxLayout()
        secondHalf.addWidget(gaussianButton)
        secondHalf.addWidget(meanShiftButton)


        # Plot processed data.
        self.lastAlgorithmLabel = QLabel("Algoritma seçilmedi.")
        self.plotProcessedDataButton = QPushButton("İşlenmiş veriyi görselleştir.")
        self.plotProcessedDataButton.clicked.connect(self._plot_processed_data)
        plotHBox = QHBoxLayout()
        plotHBox.addStretch()
        plotHBox.addWidget(self.plotProcessedDataButton)
        plotHBox.addStretch()


        # Statistical data, (ran algorithm results)
        self.statisticsList = QListWidget()

        # Export trained model.
        expHBox = QHBoxLayout()
        importButton = QPushButton("Dosyadan modeli oku")
        importButton.clicked.connect(self._import_model_button)
        expHBox.addWidget(importButton)
        expHBox.addStretch()
        exportButton = QPushButton("Modeli dışa aktar")
        exportButton.clicked.connect(self._export_model_button)
        expHBox.addWidget(exportButton)


        self.mainVerticalBox.addWidget(dialogButton)
        self.mainVerticalBox.addLayout(sampleHorizontalBox)
        self.mainVerticalBox.addWidget(self.lastFileLabel)
        self.mainVerticalBox.addLayout(plotHorizontalBox)
        self.mainVerticalBox.addSpacing(50)
        self.mainVerticalBox.addWidget(algoLabel)
        self.mainVerticalBox.addLayout(firstHalf)
        self.mainVerticalBox.addLayout(secondHalf)
        self.mainVerticalBox.addWidget(self.lastAlgorithmLabel)
        self.mainVerticalBox.addLayout(plotHBox)
        self.mainVerticalBox.addWidget(self.statisticsList)
        self.mainVerticalBox.addLayout(expHBox)

        self.setLayout(self.mainVerticalBox)

    def _sample1_data_button(self):
        self.data, self.labels = generate_blobs_data()
        self.lastFileLabel.setText("Örnek 1 veri örneği seçildi.")

    def _sample2_data_button(self):
        self.data, self.labels = generate_cyclic_data()
        self.lastFileLabel.setText("Örnek 2 veri örneği seçildi.")

    def _sample3_data_button(self):
        self.data, self.labels = generate_friedman_data()
        self.lastFileLabel.setText("Örnek 3 veri örneği seçildi.")

    def _plot_raw_data(self):
        if not len(self.data) > 0:
            return None
        easy_plot_data(self.data)

    def _plot_processed_data(self):
        if not self.model:
            return None
        
        model_plot = ModelPlot(self.model)
        model_plot.plot()
    
    def _run_dbscan(self):

        # self.statisticsList.addItem("DBSCAN algoritması çalıştırılıyor...\nLütfen Bekleyiniz..")
        
        # Check error conditions 
        # IF no data exists and some kind of things like that
        
        dialog = DbscanDialog(self.data)
        if dialog.exec_():
            self.model = dialog.model
        
        if not self.model: return None
        for key, value in self.model.info.items():
            self.statisticsList.addItem(key+": "+str(value))

        self.lastAlgorithmLabel.setText("DBSCAN algoritması çalıştırıldı ve hazır.")


    def _export_model_button(self):

        # Check if no model exists.
        
        dialog = ExportDialog(self.model)
        dialog.exec_()

    def _import_model_button(self):

        dialog = QFileDialog()
        # dialog.setFileMode("Text (*.txt)")
        # dialog.setFilter("Text (*.txt)")
        dialog.setNameFilter("Model dosyası (*.yuksel *.bayram)")

        if dialog.exec_():
            filename = dialog.selectedFiles()
            # İmport model from file
            self.model = import_model(filename[0])
            # Edit last algorithm text
            self.lastAlgorithmLabel.setText(filename[0])

            # Write model info to listView
            for key, value in self.model.info.items():
                self.statisticsList.addItem(key+": "+str(value))

    def _chooseFile(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)

        if dialog.exec_():
            filename = dialog.selectedFiles()
            self.lastFileLabel.setText(filename[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    view = Window()
    view.show()
    sys.exit(app.exec_())