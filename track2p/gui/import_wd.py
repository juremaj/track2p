

import os
from PyQt5.QtWidgets import QVBoxLayout, QWidget,  QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QFormLayout, QListWidget, QMessageBox,QListWidgetItem,QComboBox
from PyQt5.QtCore import Qt
from types import SimpleNamespace
import numpy as np


class ImportWindow(QWidget):
        
        def __init__(self, mainWindow):
            super(ImportWindow,self).__init__()
            self.main_window = mainWindow
            self.savedirectory = None
            layout = QFormLayout()
            self.storedPlane=None 
            self.setLayout(layout)
            
            import_label=QLabel("Import the directory containing the track2p folder:")
            self.saveButton = QPushButton("Import", self)
            self.saveButton.clicked.connect(self.saveDirectory)
            
            layout.addRow(import_label,self.saveButton)
            path_label=QLabel("Here is the path of the imported directory:")
            self.savedirectoryLabel = QLabel()
            layout.addRow(path_label,self.savedirectoryLabel)
            
            plane_label= QLabel("Choose the plane to analyze:")
            self.textbox = QLineEdit(self)
            self.textbox.setFixedWidth(50) 
            self.textbox.setText('0')
            layout.addRow(plane_label,self.textbox)
            
            label_combobox= QLabel("not_cell_count_over_days :")
            self.comboBox = QComboBox(self)
            layout.addRow(label_combobox,self.comboBox)
            
            label_run= QLabel("Run the analysis:")
            self.runButton = QPushButton("Run", self)
            self.runButton.clicked.connect(self.run)
            layout.addRow(label_run,self.runButton)
            
                
        def saveDirectory(self):
            savedirectory= QFileDialog.getExistingDirectory(self, "Select Directory")
            if savedirectory:
                self.savedirectory=savedirectory
                self.savedirectoryLabel.setText(f'{self.savedirectory}')
                track_ops_dict = np.load(os.path.join(self.savedirectory, "track2p", "track_ops.npy"), allow_pickle=True).item()
                track_ops = SimpleNamespace(**track_ops_dict)
                for i in range(len(track_ops.all_ds_path)):
                    self.comboBox.addItem(str(i + 1))
                
                
        def run(self):
            self.storedPlane = int(self.textbox.text())
            comboBoxResult = int(self.comboBox.currentText())
            self.main_window.loadFiles(self.savedirectory, plane=self.storedPlane, combobox_value=comboBoxResult)
                