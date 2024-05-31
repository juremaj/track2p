### --- UNDER CONSTRUCTION ---

# Run track2p through gui 

After activating the GUI through `python -m track2p` the user should navigate to the 'Run' tab on the top left of the window and select 'Run track2p algorithm' from the dropdown menu. This will open a pop-up window that will allow the user to set the paths to suite2p datasets and to set the algorithm parameters.

## Suite2p dataset organization

_ _Warning: to avoid an error, don't delete or rename suite2p data after running track2p. This is because the interface uses the paths to the suite2p datasets saved in `track_ops.npy` (`track_ops.all_ds_path`)_ _

Suite2p datasets must be structured in a specific way to be compatible with the algorithm. You need to create a folder for each day a mouse is registered. Within this folder, a folder named 'suite2p' must be present, containing one sub-folder per plane. Then, Suite2p outputs for each plane should be placed in the respective subfolder. **Please note, when you give the suite2p datasets to the algorithm, you have to give them from the first day of recording to the last day**. In this way, the first day of recording will correspond to day 1 in the interface. 

Below is an example of a mouse imagined over 7 days one plane. 

![ex_suite2p_dataset.png](docs/media/plots/ex_suite2p_dataset.png)


## Run track2p

The algorithm launch window is structured like a form and instructions are provided next to each parameter to be entered.

IMAGE

### Options

You can choose between `manually curated` and `iscell threshold`. Choosing 'manually curated' means that manual adjustments made by the user in the Suite2p interface will be taken into account. As a reminder, Suite2p detects regions of interest (ROIs) on the average image generated from a series of microscopy images. After this automatic detection, users can annotate each ROI by manually classifying them as “cell” or “not cell”. By selecting the 'manually curated' option, the algorithm will only test ROIs classified as “cell” for matching with other days of recordings. When selecting 'iscell_thr', the user must define a threshold. Only regions of interest (ROIs) detected in Suite2p with a threshold greater than this will be retained for tracking by the algorithm. As a reminder, in Suite2p, users can set a threshold for detecting regions of interest (ROIs). This threshold controls the sensitivity of detection relative to the image background.

You can tick the option `Save the outputs in suite2p format (containing cells tracked on all days)`. In this case, it will produce a version of the Suite2p datasets (stat.npy, iscell.npy, F.npy..) containing only the cells tracked on all days. Consequently, if you open the stats.npy files for different days in Suite2p and examine cell 0 for each day, you'll see that this cell corresponds to the same neural entity detected as being the same on these different days by the algorithm. These files will be located in a  `matched_suite2p` folder inside the track2p folder, and will be organized in the same way as the originals.


