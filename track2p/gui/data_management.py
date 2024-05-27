
import os
import numpy as np
import matplotlib.colors as mcolors
import random
from types import SimpleNamespace

class DataManagement:
    def __init__(self, central_widget):
        self.central_widget = central_widget
        self.main_window = central_widget.main_window
        self.all_f_t2p = []
        self.all_ops = []
        self.all_stat_t2p = []
        self.all_iscell = []
        self.colors = None
        self.t2p_match_mat_allday = None
        self.track_ops = None
        self.vector_curation_t2p = None
        self.curation_npy = None
        self.colors_copy=None
        self.plane=None
        
    def reset_attributes(self):
        self.all_f_t2p = []
        self.all_ops = []
        self.all_stat_t2p = []
        self.all_iscell = []
        self.colors = None
        self.t2p_match_mat_allday = None
        self.track_ops = None
        self.vector_curation_t2p = None
        
    def import_files(self, t2p_folder_path, plane):
        
        self.plane=plane

        if self.central_widget.fluorescences_plotting is not None:
            self.central_widget.clear()
        # load track2p outputs           
        t2p_match_mat = np.load(os.path.join(t2p_folder_path,"track2p" ,f"plane{plane}_match_mat.npy"), allow_pickle=True)
        self.t2p_match_mat_allday = t2p_match_mat[~np.any(t2p_match_mat == None, axis=1), :]
        track_ops_dict = np.load(os.path.join(t2p_folder_path, "track2p", "track_ops.npy"), allow_pickle=True).item()
        track_ops = SimpleNamespace(**track_ops_dict)
      
        
        # process suite2p files 
        for (i, ds_path) in enumerate(track_ops.all_ds_path):
            ops = np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'ops.npy'), allow_pickle=True).item()
            stat = np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'stat.npy'), allow_pickle=True)
            f = np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'F.npy'), allow_pickle=True)
            iscell = np.load(os.path.join(ds_path, 'suite2p', f'plane{plane}', 'iscell.npy'), allow_pickle=True)
            
            if track_ops.iscell_thr is None:
                    stat_iscell = stat[iscell[:, 0] == 1]
                    f_iscell = f[iscell[:, 0] == 1, :]
            else:
                    stat_iscell = stat[iscell[:, 1] > track_ops.iscell_thr]
                    f_iscell = f[iscell[:, 1] > track_ops.iscell_thr, :] 

            stat_t2p = stat_iscell[self.t2p_match_mat_allday[:, i].astype(int)]
            f_t2p = f_iscell[self.t2p_match_mat_allday[:, i].astype(int), :]
            self.all_stat_t2p.append(stat_t2p)
            self.all_f_t2p.append(f_t2p)
            self.all_ops.append(ops)
            self.all_iscell.append(iscell)
        
        
        attr_name = 'vector_curation_plane_' + str(plane)
        if hasattr(track_ops, attr_name):
            key = 'vector_curation_plane_' + str(plane)
            self.vector_curation_t2p=track_ops_dict[key] 
        else:
            vector_curation_keys=np.arange(self.t2p_match_mat_allday.shape[0]) 
            vector_curation_values = np.ones_like(vector_curation_keys)
            self.vector_curation_t2p_dict = dict(zip(vector_curation_keys, vector_curation_values))
            values = list(self.vector_curation_t2p_dict.values())
            self.vector_curation_t2p = np.array(values)
            key = 'vector_curation_plane_' + str(plane)
            track_ops_dict[key] = self.vector_curation_t2p 
            np.save(os.path.join(t2p_folder_path, "track2p", "track_ops.npy"), track_ops_dict) 

  
        attr_name_color = 'colors_plane_' + str(plane)
        if hasattr(track_ops, attr_name_color):
            self.colors= track_ops_dict[attr_name_color]
        else:
            self.colors=self.generate_vibrant_colors(len(self.all_stat_t2p[0]))
            track_ops_dict[attr_name_color] = self.colors
            np.save(os.path.join(t2p_folder_path, "track2p", "track_ops.npy"), track_ops_dict) 
           
            
        self.track_ops = track_ops
        track_ops_dict = np.load(os.path.join(t2p_folder_path, "track2p", "track_ops.npy"), allow_pickle=True).item()
        self.central_widget.track_ops_dict=track_ops_dict
        self.main_window.status_bar.vector_curation_t2p = self.vector_curation_t2p
        
        self.main_window.status_bar.vector_curation_t2p = self.vector_curation_t2p
            
        self.main_window.status_bar.spin_box.setSuffix(f'/{len(self.t2p_match_mat_allday)-1}')
        self.main_window.status_bar.spin_box.setMinimum(0)
        self.main_window.status_bar.spin_box.setMaximum(len(self.t2p_match_mat_allday)-1) 
        
        num_ones = {}  
        
        for cell, line in enumerate(self.t2p_match_mat_allday): 
                all_iscell_value=[]
                
                for day,index_match in enumerate(line):
                    if track_ops.iscell_thr is None:
                        iscell=self.all_iscell[day]
                        indices_lignes_1 = np.where(iscell[:,0]==1)[0] # take the indices where the ROIs were considered as cells in suite2p
                        true_index=indices_lignes_1[index_match] # take the "true index"
                        iscell_value=iscell[true_index,0] 
                        all_iscell_value.append(iscell_value)
                    else: 
                        iscell=self.all_iscell[day]
                        indices_lignes_1= np.where(iscell[:,1]>track_ops.iscell_thr)[0] # take the indices where the ROIs have a probability greater than trackops.is_cell_thr
                        true_index=indices_lignes_1[index_match] # take the "true index"
                        iscell_value=iscell[true_index,0] 
                        all_iscell_value.append(iscell_value)
                        
                num_ones[cell] = all_iscell_value.count(1)
                
        for i, line in enumerate(self.t2p_match_mat_allday): 
            if self.vector_curation_t2p[i]==0:
                self.colors[i] =(0.78, 0.78, 0.78)   
                print(f'ROI {i} is considered as "not cell"')  
        
      
        self.central_widget.create_mean_img()
        self.central_widget.vector_curation_t2p = self.vector_curation_t2p
        self.central_widget.display_first_ROI(0)

        
        
    def generate_vibrant_colors(self, num_colors):
        vibrant_colors = []
        for _ in range(num_colors):
            l = np.random.uniform(0.55, 0.80) 
            color = mcolors.hsv_to_rgb((random.random(), 1, l)) 
            vibrant_colors.append(color)

        return vibrant_colors
    
    