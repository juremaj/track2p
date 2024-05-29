### --- UNDER CONSTRUCTION ---

# Run track2p through gui 

After activating the GUI through `python -m track2p` the user should navigate to the 'Run' tab on the top left of the window and select 'Run track2p algorithm' from the dropdown menu. This will open a pop-up window that will allow the user to set the paths to suite2p datasets and to set the algorithm parameters.

## Suite2p dataset organization

Suite2p datasets must be structured in a specific way to be compatible with the algorithm. You need to create a folder for each day a mouse is registered. Within this folder, a folder named 'suite2p' must be present, containing one sub-folder per plane. Then, Suite2p outputs for each plane should be placed in the respective subfolder. **Please note, when you give the suite2p datasets to the algorithm, you have to give them from the first day of recording to the last day**. In this way, the first day of recording will correspond to day 1 in the interface. 

Below is an example of a mouse imagined over 7 days on two different planes. 

IMAGE

## Run track2p

The algorithm launch window is structured like a form and instructions are provided next to each parameter to be entered.

IMAGE

You can choose between `manually curated` and `iscell threshold`. Choosing 'manually curated' means that manual adjustments made by the user in the Suite2p interface will be taken into account. As a reminder, Suite2p detects regions of interest (ROIs) on the average image generated from a series of microscopy images. After this automatic detection, users can annotate each ROI by manually classifying them as “cell” or “not cell”. By selecting the 'manually curated' option, the algorithm will only test ROIs classified as “cell” for matching with other days of recordings. When selecting 'iscell_thr', the user must define a threshold. Only regions of interest (ROIs) detected in Suite2p with a threshold greater than this will be retained for tracking by the algorithm. As a reminder, in Suite2p, users can set a threshold for detecting regions of interest (ROIs). This threshold controls the sensitivity of detection relative to the image background.

You can tick the option `Save the outputs in suite2p format (containing cells tracked on all days)`. In this case, it will produce a version of the Suite2p datasets (stat.npy, iscell.npy, F.npy..) containing only the cells tracked on all days. Consequently, if you open the stats.npy files for different days in Suite2p and examine cell 0 for each day, you'll see that this cell corresponds to the same neural entity detected as being the same on these different days by the algorithm. These files will be located in a  `matched_suite2p` folder inside the track2p folder, and will be organized in the same way as the originals.

# GUI usage

## Toolbar

The user has three buttons on the toolbar:

- `Run` : launches the algorithm.
- `File` : downloads data already processed by the algorithm.
- `Visualization` : allows results to be visualized using raster plots, providing a precise graphical representation of neuronal activity over time (for more details, see section 'Raster plot' below).

## Central window

The central area of the interface presents various visualizations.

In the top left-hand corner, users can find a mean image displayed for each recording, labeled with the corresponding day number (e.g., day1, day2, etc.). They can navigate through these images by clicking on the tabs representing each day. Additionally, users have the option to zoom into specific regions of the image and click on individual cells to highlight them.

Once a cell is selected, a zoomed-in view of the surrounding area for each day (a window of 40 pixels around the cell) is displayed in the top right-hand corner.

At the bottom , users can view the fluorescence trace of the selected cell for each record. The tracks are organized chronologically, with the track at the top corresponding to the first day of recording, followed by the following days. To further analyze these traces, users can zoom in by drawing a rectangle from the bottom left corner to the top right corner of the trace. After drawing the rectangle, they can zoom in by pressing 'enter' and zoom out by pressing 'r'.


## Bottom bar

The bottom bar is divided into several parts:

- A text box with an up-down control: the user can browse all cells detected by the algorithm as present every day, and all central window information will be updated

The interface allows the user to correct the results of the algorithm's multi-day cell tracking. On initialization, all cells detected as being correctly tracked each day by our algorithm have a status of 1. This information is stored in `track_ops.vector_curation`. Each plane has its own vector.

However, the user can assess the quality of cell tracking and activity by inspecting cell outlines or by closely examining fluorescence traces. Subsequently, adjustments can be made to the status of a cell within track_ops.vector_curation through the interface.

- State of ROI : informs the user of the cell status stored in track_ops.npy
- ✅ : is used to set the cell state to 0 in track_ops.vector_curation
- ❌ : is used to set the cell state to 1 in track_ops.vector_curation
- Apply curation : is used to apply the evaluation made by the user. When the user clicks on this button, all cells with a status of 0 will be **white**, while those with a status of 1 will be **colored**. 


## Raster plot 

After activating the GUI through python -m track2p the user should navigate to the 'Visualization' tab on the top of the window and select 'Generate raster plot' from the dropdown menu. This will open a pop-up window that will allow the user to set the path to track2p folder and to set several parameters.The pop-up window is structured like a form and instructions are provided next to each parameter to be entered.

IMAGE 

The user can use `PCA`(Principal Component Analysis) and `t-SNE` (t-distributed Stochastic Neighbor Embedding) techniques to reduce data dimensionality and visualize cell clusters in a more intuitive way.  In addition, it can classify cells according to their activity for a specific day, which makes it possible to analyze variations in cell activity from day to day.

The user can also enter advanced settings:

- Averaging bin size : to smooth the plot raster data through events over defined time intervals.
- vmin and vmax parameters allow to adjust the contrast

IMAGE
  
