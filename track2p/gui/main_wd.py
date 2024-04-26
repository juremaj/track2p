from PyQt5.QtCore import Qt
import os
import numpy as np
from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QSplitter, QHBoxLayout, QFrame, QFrame,  QMenuBar,QToolBar,QMainWindow,QMenu,QAction,QToolButton,QSpinBox,QPushButton,QLabel,QLineEdit,QSizePolicy,QSpacerItem
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
import pandas as pd 


class MainWindow(QMainWindow):
    """This class is used to create the main window of the application. QWidget is the base class for all user interface objects in PyQt5 """
    def __init__(self):
        """it initializes the class attributes and calls the initUI method to create the main window of the application. It also calls the init_cell method to display the first cell of the t2p_match_mat_allday and its fluorescence and zooms across days."""
        super(MainWindow,self).__init__()
        self.all_f_t2p= []
        self.all_ops = []
        self.all_stat_t2p = []
        self.all_iscell_t2p = []
        self.init_colors = None
        self.colors = None 
        self.t2p_match_mat_allday = None 
        self.selected_cell_index = None
        self.fluorescence_plot = None
        self.roi_plot = None
        self.plot_dict =None
        self.track_ops = None
        self.initUI()
        
    def initUI(self):
        """it creates the main window of the application. It also creates the layout of the main window and sets the style of the application."""
        self.setStyleSheet(
            "QTabWidget::pane { border: 1px solid #666; }"
            "QTabWidget::tab-bar { alignment: center; }"
            "QTabBar::tab { background-color: #666; color: white; }"
            "QTabBar::tab:selected { background-color: #222; color: white; }"
            "QSplitter::handle { background: #888; }"
            "QFrame { background-color: black; color: black;  border: 1px solid black;}"
            "QLabel { color: black; background-color: none; border: none; font-size: 13px}"
            "QPushButton { background-color: #666; color: white; border: 1px solid #888; }"
            "QPushButton:hover { background-color: #888; color: white; }"
            "QPushButton:pressed { background-color: #333; color: white; }"
            "QToolButton:pressed { background-color: #888; }"
            "QComboBox { background-color: black; color: white; }"
            "QComboBox QAbstractItemView { background-color: #666; color: white; }"
            )
    
        
        toolbar=QToolBar()
      
        self.addToolBar(toolbar)
        file_menu = QMenu(self)
        run_menu = QMenu(self)
        visualization_menu = QMenu( self)
        
        load_data_action = QAction("Load processed data (⌘L or Ctrl+L)", self)
        load_data_action.setShortcut("Ctrl+L")
        load_data_action.triggered.connect(self.runProcessedData)
        file_menu.addAction(load_data_action)
        
        run_track_action = QAction("Run track2p alogorithm (⌘R or Ctrl+)", self)
        run_track_action.setShortcut("Ctrl+R")
        run_track_action.triggered.connect(self.runTrack2p)
        run_menu.addAction(run_track_action)
        
        generate_rasterplot_action = QAction("Generate raster plot (⌘G or Ctrl+G)", self)
        generate_rasterplot_action.setShortcut("Ctrl+G")
        generate_rasterplot_action.triggered.connect(self.generateRasterPlot)
        visualization_menu.addAction(generate_rasterplot_action)
        
        file_button = QToolButton()
        file_button.setStyleSheet("""
        QToolButton:pressed { background-color: gray; }
        """)
        file_button.setMenu(file_menu)
        file_button.setPopupMode(QToolButton.InstantPopup)
        file_button.setStyleSheet("font-size: 13px")
        file_button.setText("File")
        toolbar.addWidget(file_button)
        
        run_button = QToolButton()
        run_button.setMenu(run_menu)
        run_button.setPopupMode(QToolButton.InstantPopup)
        run_button.setStyleSheet("font-size: 13px")
        run_button.setText("Run")
        toolbar.addWidget(run_button)

        visualization_button = QToolButton()
        visualization_button.setMenu(visualization_menu)
        visualization_button.setPopupMode(QToolButton.InstantPopup)
        visualization_button.setStyleSheet("font-size: 13px")
        visualization_button.setText("Visualization")
        toolbar.addWidget(visualization_button)
      
        self.bottom = QFrame()
        self.bottom.setFrameShape(QFrame.StyledPanel)
        self.bottom_layout = QHBoxLayout(self.bottom)

        self.topright = QFrame()
        self.topright.setFrameShape(QFrame.StyledPanel)
        self.topright_layout = QVBoxLayout(self.topright)

        self.bottomright = QFrame()
        self.bottomright.setFrameShape(QFrame.StyledPanel)
        self.bottom_layout_right = QVBoxLayout(self.bottomright)

        self.tabs = QTabWidget(self) 
   
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
        
   
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.splitter3)
        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
        
        statusBar = self.statusBar()
        status_widget = QWidget()
        layout = QHBoxLayout()
        
        self.spin_box=QSpinBox()
        self.spin_box.setFixedWidth(100)
        self.spin_box.valueChanged.connect(self.spin_box_changed)
        
        self.status=QLabel("status: ")
        self.status.setFixedWidth(50)
        self.status_value=QLabel()
        self.status_value.setFixedWidth(30)
      
        cross_button =QPushButton('✖️')
        cross_button.setFixedSize(20,20)
        cross_button.clicked.connect(self.cross_button_clicked)
        #cross_button.clicked.connect(self.cross_button_clicked)
        
        validate_button = QPushButton('✓')
        validate_button.setFixedSize(20,20)
        validate_button.clicked.connect(self.validate_button_clicked)
        
        self.grey_cells_label=QLabel("Select the minimum number of days the cell must be present :")
        self.grey_cells_value=QLineEdit()
        self.grey_cells_value.setFixedWidth(50)
        self.grey_cells_value.returnPressed.connect(self.underline_cell_according_manually_curation)
        
        reset=QPushButton('Reset')
        reset.setFixedSize(50,20)
        reset.clicked.connect(self.init_plot_cell)
        
        #save_t2p_parameter=QPushButton('Save curation')
        #save_t2p_parameter.clicked.connect(self.save_t2p_parameter)
        spacer = QSpacerItem(1200, 20, QSizePolicy.Expanding, QSizePolicy.Fixed)


        layout.addWidget(self.spin_box)
        layout.addWidget(self.status)
        layout.addWidget(self.status_value)
        layout.addWidget(cross_button)
        layout.addWidget(validate_button)
        layout.addItem(spacer)
        layout.addWidget(self.grey_cells_label)
        layout.addWidget(self.grey_cells_value)
        layout.addWidget(reset)
        
        #layout.addWidget(save_t2p_parameter)
        
        status_widget.setLayout(layout)
        statusBar.addWidget(status_widget)
      

        QApplication.setStyle('Cleanlooks')
        self.setWindowTitle("track2p GUI")
        self.show()
        
    def save_t2p_parameter(self):
        track_ops_dict = np.load(os.path.join(self.t2p_folder_path, "track2p", "track_ops.npy"), allow_pickle=True).item() #load track2p dict
        track_ops_dict['vector_curation']=self.vector_curation_t2p #update and save track2p.vector_curation for cells that were curated manually 
        track_ops_dict['curated_cells']=self.curated_cells #update and save track2p.curated_cells for cells that were curated manually
        np.save(os.path.join(self.t2p_folder_path, "track2p", "track_ops.npy"), track_ops_dict) #save track2p dict 
        
        status_suite2p = [f'{value} / {len(self.t2p_match_mat_allday[1])}' for value in self.num_ones.values()]
        data = {'cell_number': list(self.vector_curation_t2p.keys()), 'status_t2p': list(self.vector_curation_t2p.values()), 'status_s2p': status_suite2p}
        self.df = pd.DataFrame(data)

        nb_cells= f'number of cells present on all days : {len(self.t2p_match_mat_allday)}'  
        is_cell_prob=f'probability used in track2p algorithm : {self.iscell_thr}'
        num_zeros_t2p = f'number of cells deleted in track2p : {len([value for value in self.vector_curation_t2p.values() if value == 0])}'
        
        info_string = ""
        for day in range(len(self.all_iscell_t2p) + 1):
            num_values_equal_to_day = len([value for value in self.num_ones.values() if value == day])
            info_string += f"Number of cells present {day} day out of {len(self.all_iscell_t2p)}: {num_values_equal_to_day}\n"
            keys_for_day = [key for key, value in self.num_ones.items() if value == day]
            info_string += f'Indexes: {keys_for_day}\n\n'
    

        with open(os.path.join(self.t2p_folder_path, "track2p",'info.txt'), 'w') as f:
            f.write(nb_cells + "\n" + is_cell_prob + "\n\n" +info_string +"\n\n" + num_zeros_t2p +"\n\n" + self.df.to_string(index=False) + "\n")
        

    def spin_box_changed(self):
        current_value = self.spin_box.value() #selected ROI 
        value=self.vector_curation_t2p[current_value] #status of ROI 
        self.status_value.setText(f"{value}") # display the status 
        self.update_selection(current_value) #update 
    
    def cross_button_clicked(self):
        if self.vector_curation_t2p[self.spin_box.value()] ==1:
            self.vector_curation_t2p[self.spin_box.value()]= 0
            self.colors[self.spin_box.value()] =(0.78, 0.78, 0.78)
        self.curated_cells.append(self.spin_box.value()) #add the cells to curated cells list
        for i in range(self.tabs.count()): 
            tab_widget = self.tabs.widget(i)
            cell_object = tab_widget.findChild(CellPlotWidget)
            cell_object.colors= self.colors
            cell_object.plot_cells()
        self.save_t2p_parameter()
        self.update_selection(self.spin_box.value())
    
    def validate_button_clicked(self):
        if self.vector_curation_t2p[self.spin_box.value()] ==0:
            self.vector_curation_t2p[self.spin_box.value()]= 1
            self.colors[self.spin_box.value()] =self.colors_copy[self.spin_box.value()]
        self.curated_cells.append(self.spin_box.value())
        for i in range(self.tabs.count()): 
            tab_widget = self.tabs.widget(i)
            cell_object = tab_widget.findChild(CellPlotWidget)
            cell_object.colors= self.colors
            cell_object.plot_cells()
        self.save_t2p_parameter()
        self.update_selection(self.spin_box.value())
        
    def update_remix(self,index):
        #update and save the changes for track2p (new_colors is used for track2p.colors in save_t2p_parameter)
        self.status_value.setText(f"{self.vector_curation_t2p[index]}") 
        current_tab_index = self.tabs.currentIndex()
        current_tab_widget = self.tabs.widget(current_tab_index)
        cell_plot = current_tab_widget.findChild(CellPlotWidget)         
        if cell_plot:
            cell_plot.underline_cell(index)
            
               
    def init_cell(self,index):
        """it displays the first cell of the t2p_match_mat_allday and its fluorescence and zooms across days. It is called when the application is opened.
        An instance of FluorescencePlotWidget and an instance of ZoomPlotWidget are created and added to attributes of the MainWindow class. """
        tab_widget = self.tabs.widget(0)
        cell_object = tab_widget.findChild(CellPlotWidget) #It finds the instance of the CellPlotWidget class in the first tab of the QTabWidget
        cell_object.underline_cell(index)
        cell_object.draw()
        if self.fluorescence_plot is None:
            self.fluorescence_plot = FluorescencePlotWidget(all_f_t2p=self.all_f_t2p,
                                                           all_ops=self.all_ops,
                                                           colors=self.colors, all_stat_t2p=self.all_stat_t2p)
            self.bottom_layout_right.addWidget(self.fluorescence_plot)
        if self.roi_plot is None:
            self.roi_plot = ZoomPlotWidget(all_ops=self.all_ops,
                                            all_stat_t2p=self.all_stat_t2p,
                                            colors=self.colors,
                                            all_iscell_t2p=self.all_iscell_t2p,
                                            t2p_match_mat_allday=self.t2p_match_mat_allday,track_ops=self.track_ops)
            self.bottom_layout.addWidget(self.roi_plot)
        self.fluorescence_plot.display_all_f_t2p(index)
        self.roi_plot.display_zooms(index)
        self.status_value.setText(f"{self.vector_curation_t2p[self.spin_box.value()]}") #once files are loaded 

    
    def loadFiles(self, t2p_folder_path, plane):
        self.t2p_folder_path = t2p_folder_path
        if self.fluorescence_plot is not None:
            self.clearData()
        # load track2p outputs           
        t2p_match_mat = np.load(os.path.join(self.t2p_folder_path,"track2p" ,f"plane{plane}_match_mat.npy"), allow_pickle=True)
        self.t2p_match_mat_allday = t2p_match_mat[~np.any(t2p_match_mat == None, axis=1), :]
        track_ops_dict = np.load(os.path.join(self.t2p_folder_path, "track2p", "track_ops.npy"), allow_pickle=True).item()
        track_ops = SimpleNamespace(**track_ops_dict)
        self.track_ops = track_ops
        self.iscell_thr=track_ops.iscell_thr
        
        
        
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
            self.all_iscell_t2p.append(iscell)
                        
        # initializes or retrieve track2p dictionary parameters
        
        if track_ops.curated_cells is None:
            self.curated_cells=[] #initialize the list of curated cells
        else:
            self.curated_cells=track_ops.curated_cells 
            
        if track_ops.vector_curation is None:
            self.vector_curation_keys=np.arange(self.t2p_match_mat_allday.shape[0]) #number of cells (rows in matrix)
            self.vector_curation_values = np.ones_like(self.vector_curation_keys)
            self.vector_curation_t2p = dict(zip(self.vector_curation_keys, self.vector_curation_values))

        else:
            self.vector_curation_t2p=track_ops.vector_curation

                    
        if track_ops.colors is None:
            self.colors=self.generate_vibrant_colors(len(self.all_stat_t2p[0]))
            track_ops_dict['colors'] = self.colors
            np.save(os.path.join(self.t2p_folder_path, "track2p", "track_ops.npy"), track_ops_dict) 
            self.track_ops = track_ops
            
        else:
            self.colors= track_ops.colors #affected by the choice of the user (grey cells) 
            self.colors_copy=track_ops.colors.copy()#not affected by the choice of the user (grey cells)
            

                
        self.spin_box.setSuffix(f'/{len(self.t2p_match_mat_allday)-1}')
        self.spin_box.setMinimum(0)
        self.spin_box.setMaximum(len(self.t2p_match_mat_allday)-1) 
        
        self.num_ones = {}  # Initialize as dictionary
        
        for i, line in enumerate(self.t2p_match_mat_allday): #i= number of cells 
        
                all_iscell_value=[]
                
                for j,index_match in enumerate(line): #j=number of days 
    
                    if track_ops.iscell_thr is None: #Manually curated 
                        iscell=self.all_iscell_t2p[j] # retrieve the iscell of day j 
                        indices_lignes_1 = np.where(iscell[:,0]==1)[0] # take the indices where the ROIs were considered as cells in suite2p
                        true_index=indices_lignes_1[index_match] # take the "true index" 
                        iscell_value=iscell[true_index,0] 
                        all_iscell_value.append(iscell_value)
                    else: #CHECK THIS PART
                        iscell=self.all_iscell_t2p[j]
                        indices_lignes_1= np.where(iscell[:,1]>track_ops.iscell_thr)[0] # take the indices where the ROIs have a probability greater than trackops.is_cell_thr
                        true_index=indices_lignes_1[index_match] # take the "true index" 
                        iscell_value=iscell[true_index,0] 
                        all_iscell_value.append(iscell_value)
                        
                self.num_ones[i] = all_iscell_value.count(1)
   
        self.save_t2p_parameter()
        for i, line in enumerate(self.t2p_match_mat_allday): #i= number of cells 
            if self.df.iloc[i, 1]==0:
                self.colors[i] =(0.78, 0.78, 0.78)
        self.meanimage()
        self.init_cell(0)
        
  
        
    def init_plot_cell(self):
        self.colors= self.colors_copy.copy()
        for i, line in enumerate(self.t2p_match_mat_allday): #i= number of cells 
            if self.df.iloc[i, 1]==0:
                self.colors[i] =(0.78, 0.78, 0.78)
        for i in range(self.tabs.count()): 
            tab_widget = self.tabs.widget(i)
            cell_object = tab_widget.findChild(CellPlotWidget)
            cell_object.colors= self.colors
            cell_object.plot_cells()
            
        
    def underline_cell_according_manually_curation(self):
        match_mal_all_day_copie=self.t2p_match_mat_allday.copy()
        all_keys=[]
        for key,value in self.num_ones.items():
            if value < int(self.grey_cells_value.text()):
                match_mal_all_day_copie[key, :]=np.nan
                all_keys.append(key)
        match_mal_all_day_copie = match_mal_all_day_copie.astype(float)
        # Now you can count the number of rows with at least one np.nan
        num_rows_with_nan = np.any(np.isnan(match_mal_all_day_copie), axis=1).sum()
        for i in range(self.tabs.count()): 
            tab_widget = self.tabs.widget(i)
            cell_object = tab_widget.findChild(CellPlotWidget)
            cell_object.colors= self.colors
            cell_object.plot_cells_remix(keys=all_keys)
            
            

    def clearData(self):
        self.all_f_t2p= []
        self.all_ops = []
        self.all_stat_t2p = []
        self.all_iscell_t2p = []
        self.colors = None
        self.t2p_match_mat_allday = None
        if self.fluorescence_plot:
            self.bottom_layout_right.removeWidget(self.fluorescence_plot)
            self.fluorescence_plot.deleteLater()
            self.fluorescence_plot = None
        if self.roi_plot:
            self.bottom_layout.removeWidget(self.roi_plot)
            self.roi_plot.deleteLater()
            self.roi_plot = None
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
        for i, (ops, stat_t2p) in enumerate(zip(self.all_ops, self.all_stat_t2p)):
            tab = QWidget()  
            cell_plot = CellPlotWidget(tab, ops=ops, stat_t2p=stat_t2p, f_t2p=self.all_f_t2p[i],
                                       colors=self.colors, update_selection_callback=self.update_selection,
                                       all_f_t2p=self.all_f_t2p, all_ops=self.all_ops,initial_colors=self.init_colors)
            layout = QVBoxLayout(tab)
            layout.addWidget(cell_plot)
            tab.setLayout(layout)
            self.tabs.addTab(tab, f"Day {i + 1}")
            cell_plot.cell_selected.connect(self.update_selection)
        
    def update_selection(self, selected_cell_index):
        self.selected_cell_index = selected_cell_index
        self.spin_box.setValue(selected_cell_index) 
        self.status_value.setText(f"{self.vector_curation_t2p[selected_cell_index]}")        
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
        if self.fluorescence_plot is None:
            self.fluorescence_plot = FluorescencePlotWidget(all_f_t2p=self.all_f_t2p,
                                                           all_ops=self.all_ops,
                                                          colors=self.colors)
            self.bottom_layout_right.addWidget(self.fluorescence_plot)
        if self.roi_plot is None:
            self.roi_plot = ZoomPlotWidget(all_ops=self.all_ops,
                                            all_stat_t2p=self.all_stat_t2p,
                                            colors=self.colors,
                                            all_iscell_t2p=self.all_iscell_t2p,
                                            t2p_match_mat_allday=self.t2p_match_mat_allday,track_ops=self.track_ops)
            self.bottom_layout.addWidget(self.roi_plot)
        self.fluorescence_plot.display_all_f_t2p(selected_cell_index)
        self.roi_plot.display_zooms(selected_cell_index)
            
    
    def generate_vibrant_colors(self, num_colors):
        vibrant_colors = []
        for _ in range(num_colors):
            l = np.random.uniform(0.55, 0.80) #luminosity
            color = mcolors.hsv_to_rgb((random.random(), 1, l)) #saturarion is set to 1 and the hue is random
            vibrant_colors.append(color)

        return vibrant_colors
    

         