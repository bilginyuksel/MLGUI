from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton
import sys
from util import export_model

class ExportDialog(QDialog):

  def __init__(self, model):
    super().__init__()
    
    self.setWindowTitle("Dosya Aktarımı")

    self.model = model
    self.extension = 1
    self.filename = None
    self._configure()


  def _configure(self):

    mainLayout = QVBoxLayout()

    infoLabel = QLabel("Dosya adı ve uzantısı seçilmezse dosya model isminde yaratılır. Uzantı varsayılan olarak .yuksel'dir.")

    finameHorLayout = QHBoxLayout()
    filenameLabel = QLabel("Dosya Adı:")
    self.filenameLineEdit = QLineEdit("")
    finameHorLayout.addWidget(filenameLabel)
    finameHorLayout.addWidget(self.filenameLineEdit)

    comboBoxExtensions = QComboBox()
    comboBoxExtensions.activated[str].connect(self.onChange)
    comboBoxExtensions.addItem("Bir dosya uzantısı seçiniz...")
    comboBoxExtensions.addItem('.yuksel')
    comboBoxExtensions.addItem('.bayram')


    exportButton = QPushButton("Dışa aktar")
    exportButton.clicked.connect(self._complete_export_button)


    self.infoMessage = QLabel("İşleminiz başarıyla tamamlandı...")
    self.infoMessage.setVisible(False)

    mainLayout.addWidget(infoLabel)
    mainLayout.addLayout(finameHorLayout)
    mainLayout.addWidget(comboBoxExtensions)
    mainLayout.addWidget(exportButton)
    mainLayout.addWidget(self.infoMessage)
    self.setLayout(mainLayout)

  def onChange(self, text):
    if text == '.yuksel':
      self.extension = 1
    elif text==".bayram":
      self.extension = 2


  def _complete_export_button(self):
    if not self.filenameLineEdit.text() == "":
      self.filename = self.filenameLineEdit.text()

    export_model(transform_model= self.model, filename= self.filename, extension=self.extension)
    self.infoMessage.setVisible(True)