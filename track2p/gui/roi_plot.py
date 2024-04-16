
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
import skimage


class ZoomPlotWidget(FigureCanvas):
    """It is used to display the roi of the selected cell across days with each zoom being a different day. 
    The roi is centered on the median coordinates of the selected cell. The mean image of the recording is used to create the zooms. 
    The probability of the cell being a cell and the index of the cell in the suite2p files associated with each recording (day) are also displayed under the zooms."""
    
    def __init__(self,  all_ops=None, all_stat_t2p=None, colors=None, all_iscell_t2p=None,t2p_match_mat_allday =None,track_ops=None):
        nb_plot=len(all_iscell_t2p)
        self.fig, self.ax_zoom = plt.subplots(1, nb_plot, figsize = (10*nb_plot, nb_plot), gridspec_kw={'width_ratios': [1] * nb_plot},facecolor='black')
        super().__init__(self.fig)
        self.track_ops=track_ops
        self.all_ops = all_ops
        self.all_stat_t2p = all_stat_t2p
        self.colors = colors
        self.all_is_cell=all_iscell_t2p
        self.t2p_match_mat_allday =t2p_match_mat_allday 
        self.roi_dict={} 

    def display_zooms(self, selected_cell_index):
        """It is called when the application is opened and a cell is selected."""
        self.roi_dict={} #it is used to store the roi and the median coordinates of the selected cell for each recording (day)
        if self.all_ops is not None and self.all_stat_t2p is not None and self.all_is_cell is not None:
            for i in range(len(self.all_ops)):
                wind = 20
                mean_img = self.all_ops[i]['meanImg']
                stat_t2p = self.all_stat_t2p[i]
                median_coord = stat_t2p[selected_cell_index]['med']
                #if the median coordinates of the selected cell are close to the edges of the mean image, the roi is cropped to avoid an index out of range error
                if (int(median_coord[0]) + wind) > mean_img.shape[0] and (median_coord[1] + wind) > mean_img.shape[1]:   
                    out_x = (int(median_coord[0]) + wind) - mean_img.shape[0]
                    out_y = (int(median_coord[1]) + wind) - mean_img.shape[1]
                    new_coordinate_x = int(median_coord[0]) - out_x
                    new_coordinate_y = int(median_coord[1]) - out_y
                    roi = mean_img[new_coordinate_x-wind:new_coordinate_x+wind, new_coordinate_y-wind:new_coordinate_y+wind]
                    median_coord[1]= new_coordinate_y
                    median_coord[0]=new_coordinate_x
                    self.roi_dict[i] = (roi, median_coord)
                elif (int(median_coord[0]) + wind) > mean_img.shape[0]: 
                    out_x = (int(median_coord[0]) + wind) - mean_img.shape[0]
                    new_coordinate_x = int(median_coord[0]) - out_x
                    roi = mean_img[new_coordinate_x-wind:new_coordinate_x+wind, int(median_coord[1])-wind:int(median_coord[1])+wind]
                    median_coord[0]=new_coordinate_x
                    self.roi_dict[i] = (roi, median_coord)
                elif (int(median_coord[1]) + wind) > mean_img.shape[1]: 
                    out_y = (int(median_coord[1]) + wind) - mean_img.shape[1]
                    new_coordinate_y = int(median_coord[1]) - out_y
                    roi = mean_img[int(median_coord[0])-wind:int(median_coord[0])+wind, new_coordinate_y-wind:new_coordinate_y+wind]
                    median_coord[1]= new_coordinate_y
                    self.roi_dict[i] = (roi, median_coord)
                elif (int(median_coord[0]) + wind)  > mean_img.shape[0] and (median_coord[1] - wind) <0:   
                    out_x = (int(median_coord[0]) + wind) - mean_img.shape[0]
                    out_y= 0 - (int(median_coord[1]) - wind) 
                    new_coordinate_x= int (median_coord[0]) - out_x
                    new_coordinate_y= int (median_coord[1]) + out_y
                    roi = mean_img[new_coordinate_x-wind:new_coordinate_x+wind, new_coordinate_y-wind:new_coordinate_y+wind]
                    median_coord[1]= new_coordinate_y
                    median_coord[0]=new_coordinate_x
                    self.roi_dict[i] = (roi, median_coord)
                elif (median_coord[1] - wind) <0:   
                    out_y= 0 - (int(median_coord[1]) - wind) 
                    new_coordinate_y= int (median_coord[1]) + out_y
                    roi= mean_img[int(median_coord[0])-wind:int(median_coord[0])+wind, new_coordinate_y-wind:new_coordinate_y+wind]
                    median_coord[1]= new_coordinate_y
                    self.roi_dict[i] = (roi, median_coord)
                elif (int(median_coord[0]) - wind) <0:
                    out_x = 0 - (int(median_coord[0]) - wind)
                    new_coordinate_x= int (median_coord[0]) + out_x
                    roi= mean_img[new_coordinate_x-wind:new_coordinate_x+wind, int(median_coord[1])-wind:int(median_coord[1])+wind]
                    median_coord[0]=new_coordinate_x
                    self.roi_dict[i] = (roi, median_coord)
                elif (int(median_coord[0]) - wind) <0 and (median_coord[1] + wind) > mean_img.shape[1]:   
                    out_x = 0 - (int(median_coord[0]) - wind)
                    out_y= (int(median_coord[1]) + wind) - mean_img.shape[1]
                    new_coordinate_x= int (median_coord[0]) + out_x
                    new_coordinate_y= int (median_coord[1]) - out_y
                    roi = mean_img[new_coordinate_x-wind:new_coordinate_x+wind, new_coordinate_y-wind:new_coordinate_y+wind]
                    median_coord[0]=new_coordinate_x
                    median_coord[1]= new_coordinate_y
                    self.roi_dict[i] = (roi, median_coord)
                elif (int(median_coord[0]) - wind) <0  and (median_coord[1] - wind) <0: 
                    out_x = 0 - (int(median_coord[0]) - wind)
                    out_y= 0 - (int(median_coord[1]) - wind) 
                    new_coordinate_x= int (median_coord[0]) + out_x
                    new_coordinate_y= int (median_coord[1]) + out_y
                    roi = mean_img[new_coordinate_x-wind:new_coordinate_x+wind, new_coordinate_y-wind:new_coordinate_y+wind] 
                    median_coord[0]=new_coordinate_x
                    median_coord[1]= new_coordinate_y
                    self.roi_dict[i] = (roi, median_coord)
                else: 
                    roi = mean_img[int(median_coord[0])-wind:int(median_coord[0])+wind, int(median_coord[1])-wind:int(median_coord[1])+wind]
                    self.roi_dict[i] = (roi, median_coord)
            
            for i, (roi, median_coord) in enumerate(self.roi_dict.items()):
                iscell=self.all_is_cell[i]
                if self.track_ops.iscell_thr==None:
                    indices_lignes_1 = np.where(iscell[:,0]==1)[0]
                    match_index=self.t2p_match_mat_allday[selected_cell_index,i]
                    true_index=indices_lignes_1[match_index]
                else:
                    indices_lignes_1= np.where(iscell[:,1]>self.track_ops.iscell_thr)[0]
                    match_index=self.t2p_match_mat_allday[selected_cell_index,i]
                    true_index=indices_lignes_1[match_index]
                
                prob=round(iscell[true_index,1],2)
                stat_t2p = self.all_stat_t2p[i]
                ypix=stat_t2p[selected_cell_index]['ypix']
                xpix=stat_t2p[selected_cell_index]['xpix']
                ax = self.ax_zoom[i]
                color = self.colors[selected_cell_index]
                median_values= list(self.roi_dict.values())[i][1] #median coordinates of the selected cell
                mask=np.zeros((2*wind,2*wind))
                mask[ypix-median_values[0]+wind,xpix-median_values[1]+wind]=1
                ax.clear()
                ax.contour(mask,levels=[0.5], colors=[color],linewidths=2)
                
                l_roi=list(self.roi_dict.values())[-1][0] 
                match_roi=skimage.exposure.match_histograms(list(self.roi_dict.values())[i][0], l_roi, channel_axis=None)
                
                ax.imshow(match_roi, cmap='gray')
                ax.set_title(f'Day {i + 1}', color='white', fontsize=10)
                ax.text(0.5, -0.2, f'i: {true_index}', color='white', fontsize=10, ha='center', va='center', transform=ax.transAxes)
                ax.text(0.5, -0.4, f'p: {prob}', color='white', fontsize=10, ha='center', va='center', transform=ax.transAxes)

                ax.axis('off')
        
        self.draw()
                    