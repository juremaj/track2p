
import os
from PyQt5.QtWidgets import QVBoxLayout, QWidget,  QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QFormLayout, QListWidget, QMessageBox,QListWidgetItem,QComboBox
from PyQt5.QtCore import Qt
from types import SimpleNamespace
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
from types import SimpleNamespace
import re

class Suite2pWindow(QWidget):
    
    def __init__(self, mainWindow):
            super(Suite2pWindow,self).__init__()
            self.main_window = mainWindow
            layout = QFormLayout()
            self.setLayout(layout)
            
            foldelabel=QLabel("Select the track2p folder:")
            self.folderButton = QPushButton("Select Folder", self)
            self.folderButton.clicked.connect(self.selectFolder)
            layout.addRow(foldelabel,self.folderButton)
            
            self.track2p_folder_pathLabel=QLabel("Here is the path of the imported directory:")
            self.path= QLabel()
            layout.addRow(self.track2p_folder_pathLabel,self.path)
            
            number_of_days_label= QLabel("Number of days:")
            self.number_of_days=QLabel()
            layout.addRow(number_of_days_label,self.number_of_days)
            
            plane_label= QLabel("Choose the plane:")
            self.plane_textbox = QLineEdit(self)
            self.plane_textbox.setFixedWidth(50)
            self.plane_textbox.setText('0')
            layout.addRow(plane_label,self.plane_textbox)
            
            days_label= QLabel("Choose the minimum number of days required (the cell will be present at least x days and more):")
            self.days_textbox = QLineEdit(self)
            self.days_textbox.setFixedWidth(50)
            self.days_textbox.setText('0')
            layout.addRow(days_label,self.days_textbox)
            
            okButton = QPushButton("OK", self)
            okButton.clicked.connect(self.run)
            layout.addRow(okButton)
            

    def selectFolder(self):
            track2p_folder_path= QFileDialog.getExistingDirectory(self, "Select Directory")
            if track2p_folder_path:
                self.track2p_folder_path=track2p_folder_path
                self.path.setText(f'{self.track2p_folder_path}')
                track_ops_dict = np.load(os.path.join(track2p_folder_path,  "track_ops.npy"), allow_pickle=True).item()
                track_ops = SimpleNamespace(**track_ops_dict)
                number_of_days=len(track_ops.all_ds_path)
                self.number_of_days.setText(f'{number_of_days}')
                
            
    def run(self):
        plane = int(self.plane_textbox.text())
        user_choise_days = int(self.days_textbox.text())
        self.convert_in_s2p(path=self.track2p_folder_path, plane=plane, user_choice=user_choise_days)
        
    def convert_in_s2p(self,path,plane,user_choice):
    
        user_choice=user_choice   #put the number of day you want to convert
        plane=plane #put the path to the trakc2p folder 
        track2p_folder_path=  path#"/Users/manonmantez/Desktop/el/track2p" #Put the path to the track2p folder
        track_ops_dict = np.load(os.path.join(track2p_folder_path,  "track_ops.npy"), allow_pickle=True).item()
        track_ops = SimpleNamespace(**track_ops_dict)
        indexes_list = []
        data=os.path.join(track2p_folder_path,f'plane{plane}_info.txt') #"/Users/manonmantez/Desktop/el/track2p/info.txt"
    
        track2p_save_path=track_ops.save_path
        t2p_match_mat = np.load(os.path.join(track2p_save_path,f'plane{plane}_match_mat.npy'), allow_pickle=True)
        filtered_t2p_match_mat_allday = t2p_match_mat[~np.any(t2p_match_mat == None, axis=1), :]
        iscell_thr = track_ops.iscell_thr

        with open(data, 'r') as file:
            content = file.read()
        lines = content.strip().split('\n')
        indexes_list = [line for line in lines if line.startswith('Indexes')]      
        numbers_list = [re.findall(r'\d+', line) for line in indexes_list]
        all_indexes=[]
        numbers_list = [[int(num) for num in sublist] for sublist in numbers_list]
        for i, indices in enumerate(numbers_list):
            if i >= user_choice:
                all_indexes.append(indices)
        flat_list = [item for sublist in all_indexes for item in sublist]
        filtered_t2p_match_mat_allday = filtered_t2p_match_mat_allday[flat_list, :]
        np.save(os.path.join(track2p_folder_path, f"plane{plane}_match_mat_minday{user_choice}.npy"), filtered_t2p_match_mat_allday)
     
        all_f_t2p= []
        all_ops = []
        all_stat_t2p = []
        all_iscell_t2p = []
        fneu_iscell_t2p= []
        spks_iscell_t2p= []
        fneu_chan2_iscell_t2p = []
        f_chan2_iscell_t2p = []
        redcell_iscell_t2p = []


        for (i, ds_path) in enumerate(track_ops.all_ds_path):
                    ops = np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'ops.npy'), allow_pickle=True).item()
                    stat = np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'stat.npy'), allow_pickle=True)
                    f = np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'F.npy'), allow_pickle=True)
                    fneu= np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'Fneu.npy'), allow_pickle=True)
                    spks= np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'spks.npy'), allow_pickle=True)
                    iscell = np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'iscell.npy'), allow_pickle=True)
                    if track_ops.nchannels==2:
                        f_chan2=np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'F_chan2.npy'), allow_pickle=True)
                        fneu_chan2 = np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'Fneu_chan2.npy'), allow_pickle=True)
                        redcell=np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'redcell.npy'), allow_pickle=True)

                    if track_ops.iscell_thr==None:
                        stat_iscell = stat[iscell[:, 0] == 1]
                        f_iscell = f[iscell[:, 0] == 1, :]
                        fneu_iscell = fneu[iscell[:, 0] == 1, :]
                        spks_iscell = spks[iscell[:, 0] == 1, :]
                        is_cell = iscell[iscell[:, 0] == 1, :]
                        if track_ops.nchannels==2:
                            f_chan2_iscell = f_chan2[iscell[:, 0] == 1, :]
                            fneu_chan2_iscell = fneu_chan2[iscell[:, 0] == 1, :]
                            redcell_iscell = redcell[iscell[:, 0] == 1]
                    else:
                        stat_iscell = stat[iscell[:, 1] > iscell_thr]
                        f_iscell = f[iscell[:, 1] > iscell_thr, :]
                        fneu_iscell = fneu[iscell[:, 1] > iscell_thr, :]
                        spks_iscell = spks[iscell[:, 1] > iscell_thr, :]
                        is_cell = iscell[iscell[:, 1] > iscell_thr, :]
                        if track_ops.nchannels==2:
                            f_chan2_iscell = f_chan2[iscell[:, 1] > track_ops.iscell_thr, :]
                            fneu_chan2_iscell = fneu_chan2[iscell[:, 1] > track_ops.iscell_thr, :]
                            redcell_iscell = redcell[iscell[:, 1] > track_ops.iscell_thr]
                    
                
                    stat_t2p = stat_iscell[filtered_t2p_match_mat_allday[:, i].astype(int)]
                    f_t2p = f_iscell[filtered_t2p_match_mat_allday[:, i].astype(int), :]
                    fneu_t2p = fneu_iscell[filtered_t2p_match_mat_allday[:, i].astype(int), :]
                    spks_t2p = spks_iscell[filtered_t2p_match_mat_allday[:, i].astype(int), :]
                    iscell_t2p = is_cell[filtered_t2p_match_mat_allday[:, i].astype(int), :]
                    if track_ops.nchannels==2:
                        fneu_chan2_t2p = fneu_chan2_iscell[filtered_t2p_match_mat_allday[:, i].astype(int), :]
                        f_chan2_t2p = f_chan2_iscell[filtered_t2p_match_mat_allday[:, i].astype(int), :]
                        redcell_t2p = redcell_iscell[filtered_t2p_match_mat_allday[:, i].astype(int)]

                    all_stat_t2p.append(stat_t2p)
                    all_f_t2p.append(f_t2p)
                    all_ops.append(ops)
                    all_iscell_t2p.append(iscell_t2p)      
                    fneu_iscell_t2p.append(fneu_t2p)
                    spks_iscell_t2p.append(spks_t2p)  
                    if track_ops.nchannels==2:
                        fneu_chan2_iscell_t2p.append(fneu_chan2_t2p)
                        f_chan2_iscell_t2p.append(f_chan2_t2p)
                        redcell_iscell_t2p.append(redcell_t2p)  
    


# Define the output folder path
    #output_folderpath = "/Users/manonmantez/Desktop/el/fake_suite2p"
        output_folderpath=os.path.join(track2p_folder_path, f'fake_suite2p_plane{plane}_minday{user_choice}')
        last_elements = [os.path.basename(path) for path in track_ops.all_ds_path]
# Save each element of each list to a .npy file
        for i, (stat_t2p, f_t2p, ops, iscell_t2p, fneu_t2p, spks_t2p) in enumerate(zip(all_stat_t2p, all_f_t2p, all_ops, all_iscell_t2p, fneu_iscell_t2p, spks_iscell_t2p)):
            subfolder_path = os.path.join(output_folderpath, last_elements[i])
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
    
            np.save(os.path.join(subfolder_path, f"stat.npy"), stat_t2p)
            np.save(os.path.join(subfolder_path, f"F.npy"), f_t2p)
            np.save(os.path.join(subfolder_path, f"ops.npy"), ops)
            np.save(os.path.join(subfolder_path, f"iscell.npy"), iscell_t2p)
            np.save(os.path.join(subfolder_path, f"Fneu.npy"), fneu_t2p)
            np.save(os.path.join(subfolder_path, f"spks.npy"), spks_t2p)
            if track_ops.nchannels==2:
                for i, (redcell_t2p, f_chan2_t2p, fneu_chan2_t2p) in enumerate(zip(redcell_iscell_t2p, f_chan2_iscell_t2p, fneu_chan2_iscell_t2p)):
                    np.save(os.path.join(subfolder_path, f"F_chan2.npy"), f_chan2_t2p)
                    np.save(os.path.join(subfolder_path, f"Fneu_chan2.npy"), fneu_chan2_t2p)
                    np.save(os.path.join(subfolder_path, f"redcell.npy"), redcell_t2p)
        
        print("Done")      

#save_in_s2p_format(3,0,"/Users/manonmantez/Desktop/el/prob_and_faket2p/track2p")