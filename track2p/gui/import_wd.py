
from PyQt5.QtWidgets import  QWidget, QPushButton, QFileDialog, QLineEdit, QLabel, QFormLayout

class ImportWindow(QWidget):
        
        def __init__(self, main_wd):
            super(ImportWindow,self).__init__()
            
            self.main_window = main_wd
            self.path_to_t2p = None
            self.plane=None
            
            layout = QFormLayout()
            
            import_label=QLabel("Import the directory containing the track2p folder:")
            self.import_button = QPushButton("Import", self)
            self.import_button.clicked.connect(self.save_t2p_path)
            layout.addRow(import_label,self.import_button)
            path_label=QLabel("Here is the path of the imported directory:")
            self.path = QLabel()
            layout.addRow(path_label,self.path)
            plane_label= QLabel("Choose the plane to analyze:")
            self.textbox = QLineEdit(self)
            self.textbox.setFixedWidth(50) 
            self.textbox.setText('0')
            layout.addRow(plane_label,self.textbox)
            label_run= QLabel("Run the analysis:")
            self.run_button = QPushButton("Run", self)
            self.run_button.clicked.connect(self.run)
            layout.addRow(label_run,self.run_button)
            
            self.setLayout(layout)
            
                
        def save_t2p_path(self):
            path_to_t2p= QFileDialog.getExistingDirectory(self, "Select Directory")
            if path_to_t2p:
                self.path_to_t2p=path_to_t2p
                self.path.setText(f'{self.path_to_t2p}')  
                
        def run(self):
            self.plane = int(self.textbox.text())
            self.main_window.central_widget.data_management.import_files(self.path_to_t2p, plane=self.plane)
                