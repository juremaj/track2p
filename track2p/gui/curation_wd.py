

from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QSplitter, QHBoxLayout, QFrame, QFrame, QPushButton, QFileDialog, QMenuBar, QLineEdit, QLabel, QFormLayout, QListWidget, QMessageBox,QSpinBox,QScrollArea,QGraphicsView,QGraphicsScene
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from track2p.gui.fluo_plot import FluorescencePlotWidget
import colorsys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
from PyQt5.QtCore import Qt
import matplotlib.patches as patches
from PyQt5 import QtCore
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from track2p.gui.roi_plot import ZoomPlotWidget
from matplotlib.figure import Figure
import io
from PyQt5.QtGui import QPixmap

class CurationWindow(QWidget):
    def __init__(self, mainWindow):
        super(CurationWindow,self).__init__()
        self.main_window = mainWindow
        self.colors=self.main_window.colors

        splitter = QSplitter(Qt.Vertical)
        self.figure=QGraphicsView(self) #QGraphicsView is a subclass of QWidget

        layout = QFormLayout()
        # Create a QSpinBox
        label=QLabel("Cell number:")
        self.spin_box = QSpinBox()
        self.spin_box.setSuffix(f'/{len(self.main_window.t2p_match_mat_allday)}')
        self.spin_box.setMinimum(0)
        self.spin_box.setMaximum(len(self.main_window.t2p_match_mat_allday)) 
        self.spin_box.setFixedWidth(100)
        self.spin_box.valueChanged.connect(self.spin_box_changed)
        cross_button =QPushButton('✖️')
        cross_button.clicked.connect(self.cross_button_clicked)
        
        layout.addRow(label, self.spin_box)
        layout.addRow(cross_button)
        right_widget = QWidget()
        right_widget.setLayout(layout)
        splitter.addWidget(self.figure)
        splitter.addWidget(right_widget)

        layout= QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
       

    def spin_box_changed(self):
        # Get the current value of the spin box
        current_value = self.spin_box.value()
        print(f'current value: {current_value}')
        self.plot_fluo_and_ROIs(current_value)
    
    def cross_button_clicked(self):
    # Handle the button click here
        pass
    
    # extracting the ‘little image’ and the fluorescence trace:

    def plot_fluo_and_ROIs(self,nrn_idx):
        wind = 24
        color=self.main_window.colors[nrn_idx]
        nrn_idx = nrn_idx
        wind_imgs = []
        cell_f_traces = []

        for i in range(len(self.main_window.track_ops.all_ds_path)):
            mean_img = self.main_window.all_ops[i]['meanImg']
            stat_t2p = self.main_window.all_stat_t2p[i]
            median_coord = stat_t2p[nrn_idx]['med']


        # add code to get ROI contour...
        # also dont forget code to equalise histograms for small images...


            wind_imgs.append(mean_img[int(median_coord[0])-wind:int(median_coord[0])+wind, int(median_coord[1])-wind:int(median_coord[1])+wind])
            
            cell_f_traces = [zscore(fluorescence_data, axis=1, ddof=1)[nrn_idx, :] for fluorescence_data in self.main_window.all_fluorescence]
        
        # plotting (outputs plot above):
# now mak sublots with kwidths ratio of 1 to 10, number of rows is len(track_ops.all_ds_path) and number of columns is 2
            

        fig, axs = plt.subplots(len(self.main_window.all_fluorescence), 2, figsize=(10, 1 * len(self.main_window.all_fluorescence)), gridspec_kw={'width_ratios': [1, 5]}, dpi=200)


        for i in range(len(self.main_window.track_ops.all_ds_path)):
            print(i)
  
            axs[i, 0].imshow(wind_imgs[i], cmap='gray')
            axs[i, 0].axis('off')
  
   # add code to plot ROI contour...
                
            axs[i, 1].plot(cell_f_traces[i],color=color) 
            axs[i, 1].axis('off')
            
        plt.subplots_adjust(wspace=0.2)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        scene=QGraphicsScene()
        scene.addPixmap(pixmap)
        self.figure.setScene(scene) 

      
