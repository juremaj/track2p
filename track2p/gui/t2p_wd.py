
import os
from PyQt5.QtWidgets import QVBoxLayout, QWidget,  QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QFormLayout, QListWidget, QMessageBox,QListWidgetItem, QInputDialog,QCheckBox,QSizePolicy,QComboBox,QDialog
from PyQt5.QtCore import Qt
from track2p.t2p import run_t2p
from track2p.ops.default import DefaultTrackOps

class Track2pWindow(QWidget):
        """it is used to set the parameters of the track2p algorithm"""
        def __init__(self, main_wd):
            super(Track2pWindow,self).__init__()
            self.main_window = main_wd
            layout = QFormLayout()
            self.setLayout(layout)
            self.track_ops = DefaultTrackOps()
            self.saved_directory=None
            self.plane=None
       
            instruction1=QLabel(" Import the directory containing subfolders of different recordings for the same subject:")
            self.import_recording_button = QPushButton("Import", self)
            self.import_recording_button.clicked.connect(self.import_path_to_recordings)
            layout.addRow(instruction1,self.import_recording_button)
            
            instruction2= QLabel("Here is the path of the imported directory:")
            instruction2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.path_recording=QLabel()
            self.path_recording.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.addRow(instruction2,self.path_recording)
            
            instruction3=QLabel("Once loaded press '->' to add to the list of paths to use for track2p (in the right order):")
            
            instruction4= QLabel("Choose an option for selecting suite2p ROIs:")
            field_checkbox= QVBoxLayout()
            self.checkbox1 = QCheckBox('manually curated', self)
            self.checkbox2 = QCheckBox('iscell threshold', self)
            self.checkbox2.stateChanged.connect(self.display_iscell)
            field_checkbox.addWidget(self.checkbox1)
            field_checkbox.addWidget(self.checkbox2)

            
            self.is_cell_thr=  QLineEdit()
            self.is_cell_thr.setVisible(False)
            self.is_cell_thr.setText('0.5')
            self.is_cell_thr.setFixedWidth(50)
             

            file_layout = QHBoxLayout()
       
            self.computer_file_list = QListWidget(self)
            self.computer_file_list.setFixedHeight(200) 
            self.move_to_computer_list = QPushButton("<-", self)
            self.move_to_computer_list.clicked.connect(self.move_file_to_computer_list)
            self.move_to_paths_list = QPushButton("->", self)
            self.move_to_paths_list.clicked.connect(self.move_file_to_paths_list)
            self.paths_list=QListWidget(self)
            self.paths_list.setFixedHeight(200) 
            
            file_layout.addWidget(self.computer_file_list)
            file_layout.addWidget(self.move_to_computer_list)
            file_layout.addWidget(self.move_to_paths_list)
            file_layout.addWidget(self.paths_list)
            layout.addRow(instruction3, file_layout)
            layout.addRow(instruction4,field_checkbox)
            layout.addRow("iscell threshold:",self.is_cell_thr) 
            

            instruction5=QLabel("Choose the channel to use for day-to-day registration (0 : functional, 1 : anatomical (if available))")
            self.reg_chan= QLineEdit()
            self.reg_chan.setFixedWidth(50)
            self.reg_chan.setText('0')
            layout.addRow(instruction5,self.reg_chan)
            
            
            instruction6=QLabel("Import the directory where the outputs will be saved (a 'track2p' sub-folder will be created here):")
            self.t2p_path_button = QPushButton("Import", self)
            self.t2p_path_button.clicked.connect(self.save_directoy)
            layout.addRow(instruction6,self.t2p_path_button)
            
            instruction7= QLabel("Here is the path to access the track2P folder:")
            instruction7.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.save_path=QLabel()
            self.save_path.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.addRow(instruction7,self.save_path)
            
            instruction8= QLabel("Save the outputs in suite2p format (containing cells tracked on all days):")
            self.checkbox3 = QCheckBox(self)
            layout.addRow(instruction8,self.checkbox3)
            

            self.run_button = QPushButton("Run", self)
            self.run_button.clicked.connect(self.run)
            layout.addRow("Run the algorithm:", self.run_button)
            
            terminal_intruction=QLabel("To monitor the progress of the algorith see outputs in the terminal where the GUI was launched from")
            layout.addRow(terminal_intruction)
     
    
        def display_iscell(self,state):
            if state == Qt.Checked:
                self.is_cell_thr.setVisible(True)
            else:
                self.is_cell_thr.setVisible(False)

        def run(self):
    
            stored_all_ds_path = []
            for i in range(self.paths_list.count()):
                item=self.paths_list.item(i).data(Qt.UserRole)
                item_universel=item.replace("\\", "/")
                stored_all_ds_path.append(item_universel)
            print("All parameters have been recorded ! The track2p algorithm is running...")
            self.track_ops.all_ds_path= stored_all_ds_path
            save_path=self.saved_directory
            save_path=save_path.replace("\\", "/")
            self.track_ops.save_path = save_path
            self.track_ops.reg_chan=int(self.reg_chan.text())
            if self.checkbox1.isChecked():
                self.track_ops.iscell_thr=None
            if self.checkbox2.isChecked():
                self.track_ops.iscell_thr=float(self.is_cell_thr.text())
            if self.checkbox3.isChecked():
                self.track_ops.save_in_s2p_format=True
            run_t2p(self.track_ops)
            self.open_track2p_in_gui()

    
        def open_track2p_in_gui(self):
            reply = QMessageBox.question(self, "", "Run completed successfully!\nDo you want to launch the gui?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                text, ok = QInputDialog.getText(self, '', 'Enter your plane:')
                if ok:
                    self.plane=int(text)
                    self.main_window.central_widget.data_management.import_files(self.saved_directory, plane=self.plane)
                    self.close()
            if reply == QMessageBox.No:
                pass
        
        def save_directoy(self):
            saved_directory= QFileDialog.getExistingDirectory(self, "Select Directory")
            if saved_directory:
                self.saved_directory=saved_directory
                self.save_path.setText(f'{self.saved_directory}')
                
        def import_path_to_recordings(self):
            directory = QFileDialog.getExistingDirectory(self, "Select Directory")
            if directory:
                self.path_recording.setText(f'{directory}')
                self.computer_file_list.clear()
                files= os.listdir(directory)
                for file in sorted(files):
                    full_path = os.path.join(directory, file)
                    item=QListWidgetItem(file)
                    item.setData(Qt.UserRole, full_path)
                    self.computer_file_list.addItem(item)


        def move_file_to_paths_list(self):
            selected_items = self.computer_file_list.selectedItems()
            for item in selected_items:
                self.computer_file_list.takeItem(self.computer_file_list.row(item))
                self.paths_list.addItem(item)
     

        def move_file_to_computer_list(self):
            selected_items = self.paths_list.selectedItems()
            for item in selected_items:
                self.paths_list.takeItem(self.paths_list.row(item))
                self.computer_file_list.addItem(item)
    


        
          