from PyQt5.QtCore import Qt
import os
import numpy as np
from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QSplitter, QHBoxLayout, QFrame, QFrame, QPushButton, QFileDialog, QMenuBar, QLineEdit, QLabel, QFormLayout, QListWidget, QMessageBox
from PyQt5.QtCore import Qt
import matplotlib.colors as mcolors
import random
from types import SimpleNamespace
from track2p.gui.cell_plot import CellPlotWidget
from track2p.gui.fluo_plot import FluorescencePlotWidget
from track2p.gui.roi_plot import ZoomPlotWidget
from track2p.gui.t2p_wd import NewWindow
from track2p.gui.import_wd import ImportWindow
from track2p.gui.raster_wd import RasterWindow

class MainWindow(QWidget):
    """This class is used to create the main window of the application. QWidget is the base class for all user interface objects in PyQt5 """
    def __init__(self):
        """it initializes the class attributes and calls the initUI method to create the main window of the application. It also calls the show_cell method to display the first cell of the t2p_match_mat_allday and its fluorescence and zooms across days."""
        super(MainWindow,self).__init__()
        self.all_fluorescence = []
        self.all_ops = []
        self.all_stat_t2p = []
        self.all_is_cell = []
        self.colors = None #It's a list of colors used to color the contours of the cells. Each cell has a specific color mainly for the purpose of tracking the same cell across different recordings.
        self.t2p_match_mat_allday = None 
        self.selected_cell_index = None
        self.fluorescence_plot = None
        self.zoom_plot = None
        self.initUI()
        #self.show_cell(1)
        
   
    def show_cell(self,index):
        """it displays the first cell of the t2p_match_mat_allday and its fluorescence and zooms across days. It is called when the application is opened.
        An instance of FluorescencePlotWidget and an instance of ZoomPlotWidget are created and added to attributes of the MainWindow class. """
        tab_widget = self.tabs.widget(0)
        cell_object = tab_widget.findChild(CellPlotWidget) #It finds the instance of the CellPlotWidget class in the first tab of the QTabWidget
        cell_object.underline_cell(index)
        cell_object.draw()
            
        if self.fluorescence_plot is None:
            self.fluorescence_plot = FluorescencePlotWidget(all_fluorescence=self.all_fluorescence,
                                                           all_ops=self.all_ops,
                                                           colors=self.colors, all_stat_t2p=self.all_stat_t2p)
            self.bottom_layout_right.addWidget(self.fluorescence_plot)
        if self.zoom_plot is None:
            self.zoom_plot = ZoomPlotWidget(all_ops=self.all_ops,
                                            all_stat_t2p=self.all_stat_t2p,
                                            colors=self.colors,
                                            all_is_cell=self.all_is_cell,
                                            t2p_match_mat_allday=self.t2p_match_mat_allday)
            self.bottom_layout.addWidget(self.zoom_plot)
        
        self.fluorescence_plot.display_all_fluorescence(index)
        self.zoom_plot.display_zooms(index)

    def initUI(self):
        """it creates the main window of the application. It also creates the layout of the main window and sets the style of the application."""
        self.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #666; }"
            "QTabWidget::tab-bar { alignment: center; }"
            "QTabBar::tab { background-color: #666; color: white; }"
            "QTabBar::tab:selected { background-color: #222; color: white; }"
            "QSplitter::handle { background: #888; }"
            "QFrame { background-color: black; color: black;  border: 1px solid black;}"
            "QLabel { color: white; }"
            "QPushButton { background-color: #666; color: white; border: 1px solid #888; }"
            "QPushButton:hover { background-color: #888; color: white; }"
            "QPushButton:pressed { background-color: #333; color: white; }"
            "QLineEdit { background-color: #666; color: white; }"
            "QComboBox { background-color: black; color: white; }"
            "QComboBox QAbstractItemView { background-color: #666; color: white; }"
            "QToolTip { background-color: #222; color: white; border: 1px solid white; }")
        self.central_widget = QHBoxLayout(self)
        #QTabWidget is used to create the tabs of the main window.
        self.tabs = QTabWidget(self) 
    
        menuBar=QMenuBar(self)
        menuBar.setGeometry(0,0, 500, 25)
        
        File=menuBar.addMenu("File")
        Run=menuBar.addMenu("Run")
        Visualization=menuBar.addMenu("Visualization")
        File.addAction("Load processed data", self.runProcessedData)
        Run.addAction("Run track2p alogorithm", self.runTrack2p)
        Visualization.addAction("Generate raster plot", self.generateRasterPlot)
        
        self.bottom = QFrame()
        self.bottom.setFrameShape(QFrame.StyledPanel)
        self.bottom_layout = QHBoxLayout(self.bottom)

        self.topright = QFrame()
        self.topright.setFrameShape(QFrame.StyledPanel)
        self.topright_layout = QVBoxLayout(self.topright)

        self.bottomright = QFrame()
        self.bottomright.setFrameShape(QFrame.StyledPanel)
        self.bottom_layout_right = QVBoxLayout(self.bottomright)

        #QSplitter is used to create the different sections of the main window
        self.splitter1 = QSplitter(Qt.Horizontal) 
        self.splitter1.addWidget(self.tabs)
        self.splitter1.addWidget(self.bottom)
        self.splitter1.setSizes([100, 100])

        self.splitter2 = QSplitter(Qt.Horizontal)
        self.splitter2.addWidget(self.bottomright)

        self.splitter3 = QSplitter(Qt.Vertical)
        self.splitter3.addWidget(self.splitter1)
        self.splitter3.addWidget(self.splitter2)
        self.splitter3.setSizes([100, 100])

        self.central_widget.addWidget(self.splitter3)

        self.setLayout(self.central_widget)
        QApplication.setStyle('Cleanlooks')
        self.setWindowTitle("track2p GUI")
        self.resize(800,600)
        self.show()
            

    #def importFolder(self):
      #  folderPath = QFileDialog.getExistingDirectory(self, "Select suite2p Folder")
      #  if folderPath:
          #  self.loadFiles(folderPath)

    
    def loadFiles(self, folderPath, plane):
        
        if self.fluorescence_plot is not None:
            #self.close()
            self.clearData()
           # if self.close():  # Check if the window was successfully closed
              #  self.__init__()  # Create a new instance of MainWindow
        
        if plane==0:
            t2p_match_mat = np.load(os.path.join(folderPath,"track2p" ,"plane0_match_mat.npy"), allow_pickle=True)
            self.t2p_match_mat_allday = t2p_match_mat[~np.any(t2p_match_mat == None, axis=1), :]
            vector_curation=np.arange(self.t2p_match_mat_allday.shape[0])

            track_ops_dict = np.load(os.path.join(folderPath, "track2p", "track_ops.npy"), allow_pickle=True).item()
            track_ops = SimpleNamespace(**track_ops_dict)

            iscell_thr = track_ops.iscell_thr

            
            for (i, ds_path) in enumerate(track_ops.all_ds_path):
                ops = np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'ops.npy'), allow_pickle=True).item()
                stat = np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'stat.npy'), allow_pickle=True)
                f = np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'F.npy'), allow_pickle=True)
                iscell = np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'iscell.npy'), allow_pickle=True)

                if track_ops.iscell_thr==None:
                    stat_iscell = stat[iscell[:, 0] == 1]
                    f_iscell = f[iscell[:, 0] == 1, :]

                else:
                    stat_iscell = stat[iscell[:, 1] > iscell_thr]
                    f_iscell = f[iscell[:, 1] > iscell_thr, :]
                  

                stat_t2p = stat_iscell[self.t2p_match_mat_allday[:, i].astype(int)]
                f_t2p = f_iscell[self.t2p_match_mat_allday[:, i].astype(int), :]

                self.all_stat_t2p.append(stat_t2p)
                self.all_fluorescence.append(f_t2p)
                self.all_ops.append(ops)
                self.all_is_cell.append(iscell)
            self.meanimage()
            self.show_cell(1)

        elif plane==1:
            t2p_match_mat = np.load(os.path.join(folderPath, "track2p", "plane1_match_mat.npy"), allow_pickle=True)
            self.t2p_match_mat_allday = t2p_match_mat[~np.any(t2p_match_mat == None, axis=1), :]
            track_ops_dict = np.load(os.path.join(folderPath, "track2p", "track_ops.npy"), allow_pickle=True).item()
            track_ops = SimpleNamespace(**track_ops_dict)

            iscell_thr = track_ops.iscell_thr

            for (i, ds_path) in enumerate(track_ops.all_ds_path):
                ops = np.load(os.path.join(ds_path, 'suite2p', 'plane1', 'ops.npy'), allow_pickle=True).item()
                stat = np.load(os.path.join(ds_path, 'suite2p', 'plane1', 'stat.npy'), allow_pickle=True)
                f = np.load(os.path.join(ds_path, 'suite2p', 'plane1', 'F.npy'), allow_pickle=True)
                iscell = np.load(os.path.join(ds_path, 'suite2p', 'plane1', 'iscell.npy'), allow_pickle=True)
                
                if track_ops.iscell_thr==None:
                    stat_iscell = stat[iscell[:, 0] == 1]
                    f_iscell = f[iscell[:, 0] == 1, :]
             
                
                else:
                    stat_iscell = stat[iscell[:, 1] > iscell_thr]
                    f_iscell = f[iscell[:, 1] > iscell_thr, :]
     

                stat_t2p = stat_iscell[self.t2p_match_mat_allday[:, i].astype(int)]
                f_t2p = f_iscell[self.t2p_match_mat_allday[:, i].astype(int), :]

                self.all_stat_t2p.append(stat_t2p)
                self.all_fluorescence.append(f_t2p)
                self.all_ops.append(ops)
                self.all_is_cell.append(iscell)
            self.meanimage()
            self.show_cell(1)

    def clearData(self):
        self.all_fluorescence = []
        self.all_ops = []
        self.all_stat_t2p = []
        self.all_is_cell = []
        self.colors = None
        self.t2p_match_mat_allday = None
        if self.fluorescence_plot:
            self.bottom_layout_right.removeWidget(self.fluorescence_plot)
            self.fluorescence_plot.deleteLater()
            self.fluorescence_plot = None
        if self.zoom_plot:
            self.bottom_layout.removeWidget(self.zoom_plot)
            self.zoom_plot.deleteLater()
            self.zoom_plot = None
        for i in range(self.tabs.count()):
            self.tabs.removeTab(0)
    
    def runTrack2p(self):
        self.newWindow=NewWindow(self)
        self.newWindow.show()
    
    def runProcessedData(self):
        self.importWindow=ImportWindow(self)
        self.importWindow.show()
        
    def generateRasterPlot(self):
        self.rasterWindow=RasterWindow(self)
        self.rasterWindow.show()
        
    def meanimage(self):
        self.colors = self.generate_vibrant_colors(len(self.all_stat_t2p[0]))    
        for i, (ops, stat_t2p) in enumerate(zip(self.all_ops, self.all_stat_t2p)):
            tab = QWidget()  
            cell_plot = CellPlotWidget(tab, ops=ops, stat_t2p=stat_t2p, f_t2p=self.all_fluorescence[i],
                                       colors=self.colors, update_selection_callback=self.update_selection,
                                       all_fluorescence=self.all_fluorescence, all_ops=self.all_ops)
            layout = QVBoxLayout(tab)
            layout.addWidget(cell_plot)
            tab.setLayout(layout)
            self.tabs.addTab(tab, f"Day {i + 1}")

   
            cell_plot.cell_selected.connect(self.update_selection)
        
    def update_selection(self, selected_cell_index):
        self.selected_cell_index = selected_cell_index
        if self.fluorescence_plot is None:
            self.fluorescence_plot = FluorescencePlotWidget(all_fluorescence=self.all_fluorescence,
                                                           all_ops=self.all_ops,
                                                          colors=self.colors)
            self.bottom_layout_right.addWidget(self.fluorescence_plot)
        if self.zoom_plot is None:
            self.zoom_plot = ZoomPlotWidget(all_ops=self.all_ops,
                                            all_stat_t2p=self.all_stat_t2p,
                                            colors=self.colors,
                                            all_is_cell=self.all_is_cell,
                                            t2p_match_mat_allday=self.t2p_match_mat_allday)
            self.bottom_layout.addWidget(self.zoom_plot)
        self.fluorescence_plot.display_all_fluorescence(selected_cell_index)
        self.zoom_plot.display_zooms(selected_cell_index)
        
        #it removes the underline of the previsouly selected cell even if the tab is not visible (not the current tab)
        for i in range(self.tabs.count()): 
            tab_widget = self.tabs.widget(i)
            cell_object = tab_widget.findChild(CellPlotWidget)
            cell_object.remove_previous_underline()

        current_tab_index = self.tabs.currentIndex()
        current_tab_widget = self.tabs.widget(current_tab_index)
        cell_plot = current_tab_widget.findChild(CellPlotWidget)
        if cell_plot:
            cell_plot.underline_cell(selected_cell_index)
    
    def generate_vibrant_colors(self, num_colors):
        vibrant_colors = []
        for _ in range(num_colors):
            l = np.random.uniform(0.55, 0.80) #luminosity
            color = mcolors.hsv_to_rgb((random.random(), 1, l)) #saturarion is set to 1 and the hue is random
            vibrant_colors.append(color)

        return vibrant_colors