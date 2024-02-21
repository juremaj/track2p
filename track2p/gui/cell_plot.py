from qtpy.QtCore import Signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import time 
import skimage

class CellPlotWidget(FigureCanvas):
    '''This class is used to view and interact with the mean image of each recording (day). There is one instance of this class per recording. The instance of this class is created in the MainWindow class.
    It also allows to select a cell and display its fluorescence and zooms across days. The cell selected signal is emitted when a cell is selected.'''
    cell_selected = Signal(int)

    def __init__(self, tab=None, ops=None, stat_t2p=None, f_t2p=None, colors=None, update_selection_callback=None,
                 all_fluorescence=None, all_stat_t2p=None, all_ops=None):
        """It initializes the class attributes and connects certain events to their respective handlers. It also creates the figure and the axes to display the mean image of the recording."""
        self.fig, self.ax_image = plt.subplots(1, 1) 
        self.fig.set_facecolor('black')
        super().__init__(self.fig)
        self.ops = ops
        self.stat_t2p = stat_t2p
        self.f_t2p = f_t2p
        self.all_fluorescence = all_fluorescence
        self.all_stat_t2p=all_stat_t2p
        self.all_ops=all_ops
        self.colors = colors
        self.selected_cell_index = None
        self.mpl_connect('button_press_event', self.on_mouse_press)
        self.update_selection_callback = update_selection_callback
        self.nb_cells= len(self.stat_t2p)
        self.plot_cells()
        self.initialize_interactions()
        
    def plot_cells(self):
        """It plots the mean image of the recording and the contours of the cells. It also sets the axis to be invisible and the title of the plot. It uses the colors attribute to color the contours of the cells. 
        the match_histograms function of the skimage library is used to match the histograms of the mean image of the recording and the last mean image of the recordings. . This is done to make the mean images of the recordings more comparable."""
        self.ax_image.clear()
        start = time.time()
        l_mean_img=self.all_ops[-1]['meanImg']
        match_mean_img=skimage.exposure.match_histograms(self.ops['meanImg'], l_mean_img, channel_axis=None)
        self.ax_image.imshow(match_mean_img, cmap='gray')
        
        for cell in range(self.nb_cells):
            bin_mask = np.zeros_like(self.ops['meanImg']) #create a binary mask with the same shape as the mean image of the recording
            bin_mask[self.stat_t2p[cell]['ypix'], self.stat_t2p[cell]['xpix']] = 1
            color_cell=self.colors[cell]
            self.ax_image.contour(bin_mask, levels=[0.5], colors=[color_cell], linewidths=1) 
        self.ax_image.axis('off')
        print(f'time for plotting cells on mean image for recording : {time.time()-start}')
        self.draw()


           
    def underline_cell(self,selected_cell_index):
        """It underlines the selected cell by increasing the linewidth of the contour of the cell"""
        for cell in range(self.nb_cells):
            if cell == selected_cell_index:
                bin_mask = np.zeros_like(self.ops['meanImg']) 
                bin_mask[self.stat_t2p[cell]['ypix'], self.stat_t2p[cell]['xpix']] = 1 
                color_cell=self.colors[cell]
                self.ax_image.contour(bin_mask, levels=[0.5], colors=[color_cell], linewidths=3)
        self.draw() 
    
    def remove_previous_underline(self):
        """It removes the underline of the previously selected cell by decreasing the linewidth of the contour of the cell."""
        for collection in self.ax_image.collections:
            collection.set_linewidth(1)   
        self.draw() # important, don't forget it ! (update the plot)
                
    
    def initialize_interactions(self):
        """This method is used to initialize user interactions with the mean image. It connects the scroll event to the on_scroll method and records the initial xlim and ylim of the mean image."""
        self.cid_scroll = self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.initial_xlim = self.ax_image.get_xlim()
        self.initial_ylim = self.ax_image.get_ylim()

    def on_scroll(self, event):
        """it allows to zoom in and out of the mean image of the recording. It is called when the mouse wheel is scrolled. It uses the base_scale to zoom in and out of the mean image of the recording. """
        if event.inaxes == self.ax_image:
            current_xlim = self.ax_image.get_xlim()
            current_ylim = self.ax_image.get_ylim()
            base_scale = 0.9
            scale_factor = base_scale if event.button == 'up' else 1/base_scale
            # Get the coordinates of the mouse cursor in data coordinates
            x_data, y_data = event.xdata, event.ydata
            # Compute the new limits centered on the mouse cursor
            new_xlim = [x_data - (x_data - x) * scale_factor for x in current_xlim]
            new_ylim = [y_data - (y_data - y) * scale_factor for y in current_ylim]            
            # Ensure the zoom doesn't exceed the initial image boundaries
            new_xlim = [max(self.initial_xlim[0], min(self.initial_xlim[1], x)) for x in new_xlim]
            new_ylim = [max(self.initial_ylim[1], min(self.initial_ylim[0], y)) for y in new_ylim]

            self.ax_image.set_xlim(new_xlim)
            self.ax_image.set_ylim(new_ylim)
            self.fig.canvas.draw_idle()

    def on_mouse_press(self, event):
        """It allows to select a cell by clicking on it. It is called when the mouse is clicked. It uses the x and y coordinates of the mouse cursor to determine if a cell is clicked. If a cell is clicked, the selected_cell_index attribute is updated and the cell_selected signal is emitted.
        The update_selection method of the MainWindow class is called and used to update the fluorescence and zoom plots with the selected cell. """
        start = time.time()
        if event.inaxes == self.ax_image:
            x, y = event.xdata, event.ydata
            for j, cell_info in enumerate(self.stat_t2p):
                ypix = cell_info['ypix'] #ypix are the y coordinates of the pixels of the cell
                xpix = cell_info['xpix'] #xpix are the x coordinates of the pixels of the cell
                if np.any((xpix == int(x)) & (ypix == int(y))):
                    self.selected_cell_index = j
                    self.update_selection_callback(j)
                    print(f"Cell selected: {j + 1}", flush=True)
                    break
        print(f'time taken for updating: {time.time()-start}')
        
