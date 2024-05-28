# Run track2p through gui 

After activating the GUI through `python -m track2p` the user should navigate to the 'Run' tab on the top left of the window and select 'Run track2p algorithm' from the dropdown menu. This will open a pop-up window that will allow the user to set the paths to suite2p datasets and to set the algorithm parameters.

## Suite2p dataset organization

Suite2p datasets must be structured in a specific way to be compatible with our algorithm. You need to create a folder for each day a mouse is registered. Within this folder, a folder named 'suite2p' must be present, containing one sub-folder per plane. Then, Suite2p outputs for each plane should be placed in the respective subfolder. **Please note, when you give the suite2p datasets to the algorithm, you have to give them from the first day of recording to the last day**. In this way, the first day of registration will correspond to day 1 in the interface. 

Below is an example of a mouse imagined over 7 days on two different planes. 

IMAGE

## Run track2p

The algorithm launch window is structured like a form and instructions are provided next to each parameter to be entered.

IMAGE

You can choose between 'manually curated' and 'iscell threshold'. Choosing 'manually curated' means that manual adjustments made by the user in the Suite2p interface will be taken into account. As a reminder, Suite2p detects regions of interest (ROIs) on the average image generated from a series of microscopy images. After this automatic detection, users can annotate each ROI by manually classifying them as “cell” or “not cell”. By selecting the 'manually curated' option, our algorithm will only test ROIs classified as “cell” for matching with other days of recordings. When selecting 'iscell_thr', the user must define a threshold. Only regions of interest (ROIs) detected in Suite2p with a threshold greater than this will be retained for tracking by our algorithm. As a reminder, in Suite2p, users can set a threshold for detecting regions of interest (ROIs). This threshold controls the sensitivity of detection relative to the image background.

You can tick the option 'Save the outputs in suite2p format (containing cells tracked on all days)'. In this case, it will produce a version of the Suite2p datasets (stat.npy, iscell.npy, F.npy..) containing only the cells tracked on all days. Consequently, if you open the stats.npy files for different days in Suite2p and examine cell 0 for each day, you'll see that this cell corresponds to the same neural entity detected as being the same on these different days by our algorithm. 


#IN PROGRESS



# Load track2p processed data through gui

Here we assume that each of the recording is **same length**, **imaging frequency**, **number of planes** and **number of channels** (otherwise might not work, or we cant guarantee). Moreover, for now the gui processes and displays only visualizations relating to `plane0`. 

The GUI supports both visualisation after algorithm run (as described above), as well as visualising previously processed data. The latter can be done by navigating to File -> Load processed data on the top left of the GUI. The user must import the directory containing the track2p subfolder with outputs of the algorithm (see example below).

***Warning : to avoid an error, don't remove or rename suite2p data after track2p run. Indeed, the gui uses the paths of suite2p data that have been saved in `track_ops.npy`.***

![ex_t2p_processed_data.png](media/plots/ex_t2p_processed_data.png) 


# Visualisations

The gui is divided into 3 parts: 

- In the top left-hand corner, the mean image for each recording is displayed in a tab named according to the recording day number (day1, day2 ...). The user can navigate through these tabs by clicking on them. Each mean image is interactive, so that the use can zoom in on ROIs and zoom out, once in the desired ROI the user can click on a cell which be highlighted.

![ex_meanimg_Gui](media/plots/ex_meanimg_Gui.png) 

Once the cell is clicked: 

- In the top right-hand corner a zoom (window of 40 pixels around the cell) from each mean image is displayed.

![ex_roi_gui.png](media/plots/ex_roi_gui.png) 
  
- At the bottom, the cell's fluorescence trace for each recording (per time bin) are displayed. The fluorescence trace at the top of the plot corresponds to the first day of registration and so on. The user can zoom in by drawing a rectangle *from the bottom left corner to the top right corner* as many times as desired. Once the rectangle has been drawn, the user must issue the following command: `enter` to zoom in and `r` to zoom out.

![ex_fluo_gui.png](media/plots/ex_fluo_gui.png)

