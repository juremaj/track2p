
import os
from PyQt5.QtWidgets import QVBoxLayout, QWidget,  QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QFormLayout, QListWidget, QMessageBox
from PyQt5.QtCore import Qt
from track2p.t2p import run_t2p
from track2p.ops.default import DefaultTrackOps
import sys 
from track2p.gui.terminal_gui import ConsoleOutput


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
            
            iscellLayout=QVBoxLayout()
            iscellLayout.setAlignment(Qt.AlignLeft)
            textboxLayout = QHBoxLayout()
            self.textbox = QLineEdit(self)
            self.textbox.setFixedWidth(100) 
            self.textbox.setText('0.5')
            label= QLabel("iscell_thr", self.textbox)
            legend = QLabel("threshold used to filter suite2p output (based on suite2p classifier probability in iscell.npy)", self.textbox)
            textboxLayout.addWidget(self.textbox)
            textboxLayout.addWidget(legend)
            iscellLayout.addWidget(label)
            iscellLayout.addLayout(textboxLayout)
            layout.addRow(iscellLayout)
            
            regchanLayout=QVBoxLayout()
            regchanLayout.setAlignment(Qt.AlignLeft)
            textbox1Layout = QHBoxLayout()
            self.textbox1 = QLineEdit(self)
            self.textbox1.setFixedWidth(100)
            self.textbox1.setText('0')
            label1= QLabel("reg_chan", self.textbox1)
            legend1= QLabel("which channel to use for day-to-day registration (0 : functional, 1 : anatomical (if available))", self.textbox1)
            textbox1Layout.addWidget(self.textbox1)
            textbox1Layout.addWidget(legend1)
            regchanLayout.addWidget(label1)
            regchanLayout.addLayout(textbox1Layout)
            layout.addRow(regchanLayout)
            
   
            importdirLayout=QVBoxLayout()
            importdirLayout.setAlignment(Qt.AlignLeft)
            self.importButton = QPushButton("Import directory", self)
            self.importButton.clicked.connect(self.importDirectory)
            self.importButton.setFixedWidth(150)
            importbuttonLayout=QHBoxLayout()
            legend3= QLabel("directory containing subfolders of different recordings for the same mouse (each subfolder contains a ‘suite2p’ folder in default suite2p output format)", self.importButton)
            importbuttonLayout.addWidget(self.importButton)
            importbuttonLayout.addWidget(legend3)
            importdirLayout.addLayout(importbuttonLayout)
            self.directoryLabel = QLabel()
            importdirLayout.addWidget(self.directoryLabel)
            instruction=QLabel("Once loaded press -> to add to the list of paths to use for track2p (from oldest to most recent recording day !)")
            importdirLayout.addWidget(instruction)
            layout.addRow(importdirLayout)
        
            fileLayout = QHBoxLayout()
            self.computerFileListWidget = QListWidget(self)
            fileLayout.addWidget(self.computerFileListWidget)
            self.moveToComputerButton = QPushButton("<-", self)
            self.moveToComputerButton.clicked.connect(self.moveFileToComputer)
            fileLayout.addWidget(self.moveToComputerButton)
            self.moveToBoxButton = QPushButton("->", self)
            self.moveToBoxButton.clicked.connect(self.moveFileToBox)
            fileLayout.addWidget(self.moveToBoxButton)
            self.boxFileListWidget = QListWidget(self)
            fileLayout.addWidget(self.boxFileListWidget)
            layout.addRow("", fileLayout)
            
            runLayout=QHBoxLayout()
            runLayout.setAlignment(Qt.AlignLeft)
            self.runButton = QPushButton("Run", self)
            self.runButton.clicked.connect(self.run)
            self.runButton.setFixedWidth(100)
            runLayout.addWidget(self.runButton)
            layout.addRow(runLayout)
            
            consoleOutput = ConsoleOutput()
            consoleOutput.setFixedWidth(1000)
            sys.stdout = consoleOutput
            sys.stderr = consoleOutput
            layout.addWidget(consoleOutput)
        

        def run(self):
            # Store the text in a variable
            self.storedIscellText = self.textbox.text()
            self.storedRegchanText= self.textbox1.text()
            self.storedsavepathText= self.directory  
            self.storedall_ds_path = []
            for i in range(self.boxFileListWidget.count()):
                self.storedall_ds_path.append(os.path.join(self.directory,self.boxFileListWidget.item(i).text()))
            print("All parameters have been recorded ! The track2p algorithm is running...")
            track_ops = DefaultTrackOps()
            track_ops.all_ds_path= self.storedall_ds_path
            #print(track_ops.all_ds_path)
            track_ops.save_path = self.storedsavepathText
            #print(track_ops.save_path)
            track_ops.reg_chan=int(self.storedRegchanText)
            #print(track_ops.reg_chan)
            track_ops.iscell_thr=float(self.storedIscellText)
            #print(track_ops.iscell_thr)
            run_t2p(track_ops)
            self.askQuestion()
 
        
        def askQuestion(self):
            reply = QMessageBox.question(self, "","Run completed successfully!\nDo you want to launch the gui?", QMessageBox.Yes |
                                 QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.main_window.loadFiles(self.storedsavepathText)
            if reply == QMessageBox.No:
                self.close()
        
        def importDirectory(self):
        # Open a QFileDialog to select a directory
            directory = QFileDialog.getExistingDirectory(self, "Select Directory")
            if directory:
            # Clear the QListWidget
                self.computerFileListWidget.clear()
                self.directory=directory 
                self.directoryLabel.setText(f'A track2p subfolder containing outputs of the algorithm will be created in the directory: {self.directory}')
            # Add the files in the directory to the QListWidget
                for file in os.listdir(directory):
                    self.computerFileListWidget.addItem(file)

        def moveFileToBox(self):
        # Get the selected items in the computer file list
            selectedItems = self.computerFileListWidget.selectedItems()
            for item in selectedItems:
            # Remove the item from the computer file list
                self.computerFileListWidget.takeItem(self.computerFileListWidget.row(item))
                
            # Add the item to the box file list
                self.boxFileListWidget.addItem(item.text())

        def moveFileToComputer(self):
        # Get the selected items in the box file list
            selectedItems = self.boxFileListWidget.selectedItems()
            for item in selectedItems:
            # Remove the item from the box file list
                self.boxFileListWidget.takeItem(self.boxFileListWidget.row(item))
            # Add the item to the computer file list
                self.computerFileListWidget.addItem(item.text())
                

