
import os
from PyQt5.QtWidgets import QVBoxLayout, QWidget,  QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QFormLayout, QListWidget, QMessageBox,QListWidgetItem, QInputDialog,QCheckBox,QSizePolicy
from PyQt5.QtCore import Qt
from track2p.t2p import run_t2p
from track2p.ops.default import DefaultTrackOps
import sys 
#from track2p.gui.terminal_gui import MultiStream, ConsoleOutput


class NewWindow(QWidget):
        """it is used to set the parameters of the track2p algorithm. 
    It is called when the user clicks on the run track2p algorithm button in the main window. 
    It allows to set the iscell_thr and reg_chan parameters of the track2p algorithm. 
    It also allows to import the directories containing the outputs of the suite2p algorithm.
    The user can also save the parameters and run the track2p algorithm."""
        def __init__(self, mainWindow):
            super(NewWindow,self).__init__()
            self.main_window = mainWindow
            layout = QFormLayout()
            self.setLayout(layout)
            self.stored_plane=None 
            self.file_paths = {}
            
        
            label_imp_button=QLabel(" Import the directory containing subfolders of different recordings for the same subject:")
            self.importButton = QPushButton("Import", self)
            self.importButton.clicked.connect(self.importDirectory)
            layout.addRow(label_imp_button,self.importButton)
            
            label_imp_path= QLabel("Here is the path of the imported directory:")
            label_imp_path.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.label_dir=QLabel()
            self.label_dir.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.addRow(label_imp_path,self.label_dir)
            
            instruction=QLabel("Once loaded press '->' to add to the list of paths to use for track2p (in the right order):")
            #layout.addRow(instruction)
            
            label_checkbox= QLabel("Choose an option for selecting suite2p ROIs:")
            field_checkbox= QVBoxLayout()
            self.checkbox1 = QCheckBox('manually curated', self)
            self.checkbox2 = QCheckBox('iscell threshold', self)
            self.checkbox2.stateChanged.connect(self.display_iscell)
            field_checkbox.addWidget(self.checkbox1)
            field_checkbox.addWidget(self.checkbox2)
            #layout.addRow(label_checkbox,field_checkbox)
            
            self.is_cell_thr=  QLineEdit()
            self.is_cell_thr.setVisible(False)
            self.is_cell_thr.setText('0.5')
            self.is_cell_thr.setFixedWidth(50)
            #layout.addRow("iscell threshold:",self.is_cell_thr)                    

            fileLayout = QHBoxLayout()
            #fileLayout.setAlignment(Qt.AlignLeft) 
            self.computer_file_list = QListWidget(self)
            self.computer_file_list.setFixedHeight(200) 
            self.move_to_computer_list = QPushButton("<-", self)
            self.move_to_computer_list.clicked.connect(self.moveFileToComputer)
            self.move_to_paths_list = QPushButton("->", self)
            self.move_to_paths_list.clicked.connect(self.moveFileToBox)
            self.paths_list=QListWidget(self)
            self.paths_list.setFixedHeight(200) 
            
            fileLayout.addWidget(self.computer_file_list)
            fileLayout.addWidget(self.move_to_computer_list)
            fileLayout.addWidget(self.move_to_paths_list)
            fileLayout.addWidget(self.paths_list)
            layout.addRow(instruction, fileLayout)
            layout.addRow(label_checkbox,field_checkbox)
            layout.addRow("iscell threshold:",self.is_cell_thr) 
            
            
            
            chan_label=QLabel("Choose the channel to use for day-to-day registration (0 : functional, 1 : anatomical (if available))")
            self.reg_chan= QLineEdit()
            self.reg_chan.setFixedWidth(50)
            self.reg_chan.setText('0')
            layout.addRow(chan_label,self.reg_chan)
            
            
            label_imp_save_button=QLabel("Import the directory where the outputs will be saved (a 'track2p' sub-folder will be created here):")
            self.importSaveButton = QPushButton("Import", self)
            self.importSaveButton.clicked.connect(self.saveDirectory)
            layout.addRow(label_imp_save_button,self.importSaveButton)
            
            label_save_path= QLabel("Here is the path to access the track2P folder:")
            label_save_path.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.save_path=QLabel()
            self.save_path.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.addRow(label_save_path,self.save_path)
            
        
            self.run_button = QPushButton("Run", self)
            self.run_button.clicked.connect(self.run)
            layout.addRow("Run the algorithm:", self.run_button)
            
            terminal_intruction=QLabel("To monitor the progress of the algorith see outputs in the terminal where the GUI was launched from")
            layout.addRow(terminal_intruction)
     
    
############################################################################################################################################################################

        def display_iscell(self,state):
            if state == Qt.Checked:
                self.is_cell_thr.setVisible(True)
            else:
                self.is_cell_thr.setVisible(False)

        def run(self):
            # Store the text in a variable
            self.is_cell= self.is_cell_thr.text()
            self.reg_channel= self.reg_chan.text()
            self.save_track2p_path= self.savedirectory
            self.stored_all_ds_path = []
            for i in range(self.paths_list.count()):
                self.stored_all_ds_path.append(self.paths_list.item(i).data(Qt.UserRole))
            print("All parameters have been recorded ! The track2p algorithm is running...")
            track_ops = DefaultTrackOps() #Initializes the track_ops object with the default parameters
            track_ops.all_ds_path= self.stored_all_ds_path
            print(f'track_ops.all_ds_path : {track_ops.all_ds_path}')
            track_ops.save_path = self.save_track2p_path
            track_ops.reg_chan=int(self.reg_channel)
            if self.checkbox1.isChecked():
                track_ops.iscell_thr=None
            if self.checkbox2.isChecked():
                track_ops.iscell_thr=float(self.is_cell)
            run_t2p(track_ops)
            self.askQuestion()
 

        def askQuestion(self):
            reply = QMessageBox.question(self, "", "Run completed successfully!\nDo you want to launch the gui?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                text, ok = QInputDialog.getText(self, '', 'Enter your plane:')
                if ok:
                    self.storedPlane=int(text)
                    self.main_window.loadFiles(self.save_track2p_path, plane=self.storedPlane)
                    self.close()
            if reply == QMessageBox.No:
                pass
        
        def saveDirectory(self):
            savedirectory= QFileDialog.getExistingDirectory(self, "Select Directory")
            if savedirectory:
                self.savedirectory=savedirectory
                self.save_path.setText(f'{self.savedirectory}')
                
        def importDirectory(self):
            directory = QFileDialog.getExistingDirectory(self, "Select Directory")
            if directory:
                self.label_dir.setText(f'{directory}')
                self.computer_file_list.clear()
                files= os.listdir(directory)
                for file in sorted(files):
                    full_path = os.path.join(directory, file)
                    item=QListWidgetItem(file)
                    item.setData(Qt.UserRole, full_path)
                   # print(f'file_name={item.text()}')
                    #print(f'full_path={item.data(Qt.UserRole)}')
                    self.computer_file_list.addItem(item)


        def moveFileToBox(self):
            selectedItems = self.computer_file_list.selectedItems()
            for item in selectedItems:
                self.computer_file_list.takeItem(self.computer_file_list.row(item))
                self.paths_list.addItem(item)
            #for i in range(self.boxFileListWidget.count()):
              #  print(self.boxFileListWidget.item(i).text())
              # print(self.boxFileListWidget.item(i).data(Qt.UserRole))

        def moveFileToComputer(self):
            selectedItems = self.paths_list.selectedItems()
            for item in selectedItems:
                self.paths_list.takeItem(self.paths_list.row(item))
                self.computer_file_list.addItem(item)
                

