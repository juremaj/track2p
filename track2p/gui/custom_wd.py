import os
from PyQt5.QtWidgets import QVBoxLayout, QWidget,  QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QFormLayout, QListWidget, QMessageBox,QListWidgetItem, QInputDialog,QCheckBox,QSizePolicy,QComboBox,QDialog
from PyQt5.QtCore import Qt
from track2p.t2p import run_t2p
from track2p.ops.default import DefaultTrackOps

class CustomDialog(QDialog):
    def __init__(self, main_window, save_directory, channel):
        super(CustomDialog,self).__init__()
        self.main_window = main_window
        self.save_directory = save_directory
        self.channel = channel
        self.cancel_clicked = False

        # Layout
        layout = QVBoxLayout(self)
        
        # Plane input
        self.plane_label = QLabel("Enter your plane:", self)
        layout.addWidget(self.plane_label)
        self.plane_input = QLineEdit(self)
        layout.addWidget(self.plane_input)
        
        # Trace type input
        self.trace_label = QLabel("Choose trace type:", self)
        layout.addWidget(self.trace_label)
        self.trace_combo = QComboBox(self)
        self.trace_combo.addItems(["F", "spks", "dF/F0"])  
        layout.addWidget(self.trace_combo)
        
        # OK and Cancel buttons
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.import_data)
        layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        layout.addWidget(self.cancel_button)

    def get_inputs(self):
        return self.plane_input.text(), self.trace_combo.currentText(), 
    
    def on_cancel_clicked(self):
        self.cancel_clicked = True
        self.import_data()

    def import_data(self):
        if self.cancel_clicked:
            self.close()
            pass
        else: 
            print("Opening GUI...")
            plane_text, trace_type = self.get_inputs()
            self.plane = int(plane_text)
            self.trace_type = trace_type
            print(f"Converted plane: {self.plane}, Trace type: {self.trace_type}")  # Debugging print
            self.main_window.central_widget.data_management.import_files(t2p_folder_path = self.save_directory, plane=self.plane, trace_type=self.trace_type, channel= self.channel)
            self.close()

