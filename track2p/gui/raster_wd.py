import os
import io
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QFileDialog, QLineEdit, QLabel, QFormLayout, QCheckBox, QComboBox,QGraphicsView,QGraphicsScene,QSplitter,QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.stats import zscore
from sklearn.decomposition import PCA
from openTSNE import TSNE
import matplotlib.pyplot as plt
import copy



class RasterWindow(QWidget):
        #QWidget is the parent class
        def __init__(self, mainWindow):
            super(RasterWindow,self).__init__()
            self.main_window = mainWindow
            self.all_f_t2p=None 
            self.all_stat_t2p=None
            self.raster_type=None
            self.bin_size = None
            self.filename=None
            self.all_f_t2p_preproc=None
            self.vmin_value=None
            self.vmax_value=None
         
            
            #Create the right-hand side of the window
            layout = QFormLayout()
            
            label_imp= QLabel("Import the directory containing the 'track2p' folder:")
            field_imp=QPushButton("Import")
            field_imp.clicked.connect(self.load_directory_contents)
            layout.addRow(label_imp,field_imp)
            
            label_imp_path= QLabel("Here is the path of the imported directory:")
            self.field_imp_path=QLabel()
            layout.addRow(label_imp_path,self.field_imp_path)
            
            label_plane= QLabel("Choose the plane to analyze:")
            self.field_plane=QLineEdit()
            self.field_plane.setText('0')
            self.field_plane.setFixedWidth(50)
            layout.addRow(label_plane,self.field_plane)
            
            label_checkbox= QLabel("Choose the sorting method:")
            field_checkbox= QVBoxLayout()
            self.checkbox1 = QCheckBox('without sorting', self)
            self.checkbox2 = QCheckBox('sorting by PCA', self)
            self.checkbox3 = QCheckBox('sorting by PCA on given day', self)
            self.checkbox4 = QCheckBox('sorting by tSNE', self)
            self.checkbox5 = QCheckBox('sorting by tSNE on given day', self)
            self.day_choice= QComboBox(self)
            self.day_choice.addItem('Choose recording index (for sorting on given day)')
            field_checkbox.addWidget(self.checkbox1)
            field_checkbox.addWidget(self.checkbox2)
            field_checkbox.addWidget(self.checkbox3)
            field_checkbox.addWidget(self.checkbox4)
            field_checkbox.addWidget(self.checkbox5)
            field_checkbox.addWidget(self.day_choice)
            layout.addRow(label_checkbox,field_checkbox)
            
            label_check=QLabel("Advanced options:")
            self.check=QCheckBox(self)
            self.check.stateChanged.connect(self.display_advanced_options)
            
            layout.addRow(label_check,self.check)
            self.advanced_options_group = QGroupBox()
            self.advanced_options_group.setVisible(False)
            group_layout = QFormLayout()
            self.bin= QLineEdit()
            self.bin.setText('1')
            self.bin.setFixedWidth(50)
            group_layout.addRow("Averaging bin size:", self.bin)
            self.vmin= QLineEdit()
            self.vmin.setText('0')
            self.vmin.setFixedWidth(50)
            group_layout.addRow("vmin:", self.vmin)
            self.vmax= QLineEdit()
            self.vmax.setText('1.96')
            self.vmax.setFixedWidth(50)
            group_layout.addRow("vmax:", self.vmax)
            self.advanced_options_group.setLayout(group_layout)
            layout.addRow('',self.advanced_options_group)
            

            # Initially hide the widgets
            self.bin.setVisible(False)
            self.vmin.setVisible(False)
            self.vmax.setVisible(False)         
            
            label_run= QLabel("Run the analysis:")
            field_run=QPushButton("Run")
            field_run.clicked.connect(self.generate_raster_plt)
            layout.addRow(label_run,field_run)
            
            label_save= QLabel("Save the figure:")
            field_save = QPushButton("Save")
            field_save.clicked.connect(self.get_output_save_path)
            layout.addRow(label_save,field_save)
            
            label_output_path= QLabel("The figure has been saved here:")
            self.field_output_path=QLabel()
            layout.addRow(label_output_path,self.field_output_path)
            
            self.view=QGraphicsView(self) #QGraphicsView is a subclass of QWidget
            
            splitter = QSplitter(Qt.Horizontal)            
            right_widget = QWidget()
            right_widget.setLayout(layout)
            splitter.addWidget(right_widget)
            splitter.addWidget(self.view)
            
            main_layout = QVBoxLayout(self)
            main_layout.addWidget(splitter)
            
            self.setLayout(main_layout)
           
############################################################################################################################################################################
        def display_advanced_options(self,state):
            if state == Qt.Checked:
                self.advanced_options_group.setVisible(True)
                self.bin.setVisible(True)
                self.vmin.setVisible(True)
                self.vmax.setVisible(True)
            else:
                self.advanced_options_group.setVisible(False)
                self.bin.setVisible(False)
                self.vmin.setVisible(False)
                self.vmax.setVisible(False)
                
        def load_directory_contents(self):
            self.load_directory= QFileDialog.getExistingDirectory(self, "Select Directory")
            if self.load_directory:
                #self.savedirectory=savedirectory
                self.field_imp_path.setText(f'{self.load_directory}')
            #self.storedPlane = int(self.fieldPlane.text())
            plane=int(self.field_plane.text())
            value=1
            self.main_window.loadFiles(self.load_directory,plane,value)
            self.all_f_t2p= self.main_window.all_f_t2p
            self.all_stat_t2p= self.main_window.all_stat_t2p
            for i in range(len(self.all_stat_t2p)):
                self.day_choice.addItem(str(i + 1))
        
        def get_output_save_path(self):
            #save_path= QFileDialog.getExistingDirectory(self, "Select Directory")
            #if save_path:
            raster_folder = os.path.join(self.load_directory,'track2p', 'raster')
            os.makedirs(raster_folder, exist_ok=True)
            self.field_output_path.setText(f'{raster_folder}')
            filename=os.path.join(raster_folder,'rasterplot_{}_plane{}.pdf'.format(self.raster_type,str(self.field_plane.text())))
            plt.savefig(filename)
                
        def get_checkbox_choice(self):
            vmin=float(self.vmin.text())
            vmax=float(self.vmax.text())
            print(vmin)
            print(vmax)
            if self.checkbox1.isChecked():
                self.raster_type='without_sorting'
                self.plot_track2p_rasters(self.all_f_t2p_preproc, fs=30/self.bin_size, vmin=vmin, vmax=vmax)
            if self.checkbox2.isChecked():
                self.raster_type='sorting_by_PCA'
                all_pca_emb_1d = []
                for f in tqdm(self.all_f_t2p_preproc):
                    print(f.shape)
                    pca_emb_1d = self.fit_pca_1d(f.T)
                    print(pca_emb_1d.shape)
                    all_pca_emb_1d.append(pca_emb_1d)
                all_f_t2p_sorted = []
                for (i, f) in enumerate(self.all_f_t2p_preproc):
                    sort_inds = np.argsort(np.array(all_pca_emb_1d[i]).squeeze())
                    f_sorted = f[sort_inds, :].squeeze()
                    all_f_t2p_sorted.append(f_sorted)
                self.plot_track2p_rasters(all_f_t2p_sorted, fs=3, vmin=vmin, vmax=vmax) # plot the rasters
            if self.checkbox3.isChecked():
                self.raster_type='sorting_by_PCA_and_by_day_' + str(self.day_choice.currentText())
                all_pca_emb_1d = []
                for f in tqdm(self.all_f_t2p_preproc):
                    print(f.shape)
                    pca_emb_1d = self.fit_pca_1d(f.T)
                    print(pca_emb_1d.shape)
                    all_pca_emb_1d.append(pca_emb_1d)
                all_f_t2p_sorted = []
                for (i, f) in enumerate(self.all_f_t2p_preproc):
                    user_i= int(self.day_choice.currentText()) - 1
                    sort_inds = np.argsort(np.array(all_pca_emb_1d[user_i]).squeeze())
                    f_sorted = f[sort_inds, :].squeeze()
                    all_f_t2p_sorted.append(f_sorted)
                self.plot_track2p_rasters(all_f_t2p_sorted, fs=30/self.bin_size, vmin=vmin, vmax=vmax)
            if self.checkbox4.isChecked():
                self.raster_type='sorting_by_tSNE'
                all_tsne_emb_1d = []
                for f in tqdm(self.all_f_t2p_preproc):
                    print(f.shape)
                    tsne_emb_1d = self.fit_tsne_1d(f.T)
                    all_tsne_emb_1d.append(tsne_emb_1d)
                all_f_t2p_sorted = []
                for (i, f) in enumerate(self.all_f_t2p_preproc):
                    sort_inds = np.argsort(np.array(all_tsne_emb_1d[i]).squeeze())
                    f_sorted = f[sort_inds, :].squeeze()
                    all_f_t2p_sorted.append(f_sorted)
                self.plot_track2p_rasters(all_f_t2p_sorted, fs=30/self.bin_size, vmin=vmin, vmax=vmax) # plot the rasters
            if self.checkbox5.isChecked():
                self.raster_type='sorting_tSNE_and_by_day_' + str(self.day_choice.currentText())
                all_tsne_emb_1d = []
                for f in tqdm(self.all_f_t2p_preproc):
                    print(f.shape)
                    tsne_emb_1d = self.fit_tsne_1d(f.T)
                    all_tsne_emb_1d.append(tsne_emb_1d)
                all_f_t2p_sorted = []
                for (i, f) in enumerate(self.all_f_t2p_preproc):
                    user_i= int(self.day_choice.currentText()) - 1
                    sort_inds = np.argsort(np.array(all_tsne_emb_1d[user_i]).squeeze())
                    f_sorted = f[sort_inds, :].squeeze()
                    all_f_t2p_sorted.append(f_sorted)
                self.plot_track2p_rasters(all_f_t2p_sorted, fs=30/self.bin_size, vmin=vmin, vmax=vmax) # plot the rasters
       
                    
        
        def generate_raster_plt(self):
            self.set_initial_parameters()
            self.get_checkbox_choice()
        
        
############################################################################################################################################################################      
        def set_initial_parameters(self):
         
            bin_data = True
            self.bin_size = int(self.bin.text()) #numer of frames to average, 1 means no averging 
            print(self.bin_size)
            rem_zero_rows = True

            if bin_data:
                # f is a matrix of shape (neurons, frames) i want to average each 10 frames
                all_f_t2p_original = copy.deepcopy(self.all_f_t2p)
                self.all_f_t2p_preproc = [np.mean(f.reshape(f.shape[0], -1, self.bin_size), axis=2) for f in all_f_t2p_original]
                for f in self.all_f_t2p.copy():
                    print(f.shape)
                # renormalize
                self.all_f_t2p_preproc =self.zscore_all_f_t2p(self.all_f_t2p_preproc)
                #self.all_f_t2p = all_f_t2p_preproc
            if rem_zero_rows:
                # get zero rows in any of the datasets
                zero_rows = np.any([np.sum(np.isnan(f), axis=1) for f in self.all_f_t2p_preproc], axis=0)
                print(f'Number of zero rows: {np.sum(zero_rows)}') 
                self.all_f_t2p_preproc= [f[~zero_rows, :] for f in self.all_f_t2p_preproc]
                #self.all_stat_t2p = [stat[~zero_rows] for stat in self.all_stat_t2p]
                
                
                
        def zscore(self, f, axis=1): #axis=1 means that we are normalizing each neuron's activity (each line of the matrix f)
            '''this method calculates the z-score for each element in the input array f along the specified axis, ignoring NaN values.'''
            return (f - np.nanmean(f, axis=axis, keepdims=True)) / np.nanstd(f, axis=axis, keepdims=True)

        def zscore_all_f_t2p(self, all_f_t2p):
            return [zscore(f, axis=1) for f in all_f_t2p]
        
        def norm_minmax(self, x):
            """(x - np.min(x)) / (np.max(x) - np.min(x)) This line performs the Min-Max normalization. For each element in x, it subtracts the minimum value of x and then divides by the range of x (maximum value - minimum value). The result is an array where all values are in the range [0, 1]."""
            return (x - np.min(x)) / (np.max(x) - np.min(x))
        
                
        def plot_track2p_rasters(self, all_f_t2p, fs=30, vmin=None, vmax=None):
                
            fig, ax = plt.subplots(len(all_f_t2p), 1, figsize=(6, len(all_f_t2p)*1), dpi=150) #(rows, columns, size, resolution)

            for i, f in enumerate(all_f_t2p):
                ax[i].imshow(zscore(f, axis=1), aspect='auto', cmap='Greys', vmin=vmin, vmax=vmax)
                # only first and last yticks
                ax[i].set_yticks([0, f.shape[0]-1])
                ax[i].set_yticklabels([0, f.shape[0]])
                # move the text of the yticklabels a bit: the first one down and the last one up
                ax[i].set_yticklabels(ax[i].get_yticklabels(), rotation=0, va='center', ha='right')
        
                # only first and last xticks on y axis in minutes
                if i == len(all_f_t2p)-1:
                    ax[i].set_xlabel('Time (min)')
                    ax[i].set_xticks([0, f.shape[1]/2, f.shape[1]-1])
                    ax[i].set_xticklabels([0, int(f.shape[1]/fs/(2*60)), int(f.shape[1]/fs/60)])
            
                else:
                    ax[i].set_xticks([])
                    ax[i].set_xticklabels([])
            
                plt.subplots_adjust(bottom=0.2)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(buf.getvalue())
            scene=QGraphicsScene()
            scene.addPixmap(pixmap)
            self.view.setScene(scene)
                
            
        def fit_pca_1d(self,data):
            print('fitting 1d-PCA...')
            pca=PCA(n_components=1)
            pca.fit(data)
            embedding = pca.components_.T
            return embedding

        def fit_tsne_1d(self,data):
            print('fitting 1d-tSNE...')
            # default openTSNE params
            tsne = TSNE(
            n_components=1,
            perplexity=30,
            initialization="pca",
            metric="euclidean",
            n_jobs=8,
            random_state=3
            )

            tsne_emb = tsne.fit(data.T)
            return tsne_emb



            
            
        