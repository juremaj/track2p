# track2p
Cell tracking for longitudinal calcium imaging recordings.

# Installation

## Installing via pip (recommended)

First make sure that you have an updated version of conda installed (the procedure below is based on conda 23.11.0).

Next, set up conda environment with python 3.9:

```
conda create --name track2p python=3.9
conda activate track2p
```

Install the tack2p package using pip:

```
pip install track2p
```

And thats it, track2p should be succesfully installed :)

(for instructions on how to run the algorithm, see the 'Usage' section)

Note: 
Additionally it can be useful to install jupyter for example for using the demo on how to use track2p outputs for downstream analysis (`demo_t2p_outputs.ipynb`). Jupyter can be installed by for example:

```
conda install conda-forge::jupyterlab
```

## Installing via Github (discouraged)

Alternatively track2p can also be installed directly from the Github repository (this is currently discouraged, since the repo is under active development).
To install via Github run:

```
conda create --name track2p python=3.9
conda activate track2p
git clone https://github.com/juremaj/track2p
cd track2p
pip install -e .
```

# Usage

The current version (0.2.1) is not extremely user friendly, but this will be improved soon. It is recommended to run through `run_track2p.py`, which should be modified manually (see below). After correctly configuring, simply run:

```
conda activate track2p
python -m run_track2p
```

This should start printing out the progress and will tell you once the algorithm is finished :)

## Setting up `run_track2p.py`

`run_track2p.py` script in the root of the directory and specifies:

- `track_ops.all_ds_path`: list of paths to datasets containing a `suite2p` folder
- `track_ops.save_path`: where the outputs will be saved (a `track2p` folder will be generated here)
- `track_ops.---`: `---` being different parameter names overwriting the defaults (for basic documentation see comments in `track2p/ops/default.py`, more documentation will be added soon).


## Changing algorithm parameters

TODO: add documentation of algorithm parameters (for now use the defaults saved at `track2p/ops/default.py`, they should work well). If some parameters should be overwritten its recommended to do so in the `run_track2p.py` script (see section above).

# Outputs

All the outputs of the script will be saved in a `track2p` folder created within the `track_ops.save_path` directory specified by the user when running the algorithm. For an introduction on how to use the outputs for further downstream analysis we provide a useful demo notebook `demo_t2p_outlput.ipynb` in the root of this repository.

## Matches

There are two types of output from track2p:

- A matrix (`plane#_match_mat.npy`) containing the indices of matched neurons across the session for a given plane (`#` is the index of the plane). Since matching is done from first day to last, some neurons will not be sucessfully tracked after one or a few days. In this case the matrix contains `None` values. To get neurons tracked across all days only take the rows of the matrices containing no `None` values. 

- A `track_ops.npy` object that contains the parameters used for the algorithm and some intermediate results that can be used for visualisations (e. g. registered images and ROIs etc.)


## Visualisations

There are several visualisations that can be used to evaluate the registration and cell matching quality (these figures are generated automatically when running the algorithm). These will all be saved in the path defined by `track_ops.save_path` under `track2p/fig`

The figures are the following (in the order of importance):

- `reg_img_output.png` image visualising the quality of image registration across the two days. Each pair of recordings is visualised as red/green overlay of the mean images on the two days before (above) and after (below) registration. If the bottom images don't show good alignment the output of the algorithm would be completely useless (if this happen make sure everyhting is correct with the data)

![ex_reg_img_output.png](docs/media/readme/ex_reg_img_output.png)

- `thr_met_hist.png` visualises the IOU of the matched ROIs. TODO: document how the algorithm works, this will make it clearer. For now refer to other examples for explanation e. g. https://www.cell.com/cell-reports/pdf/S2211-1247(17)31430-4.pdf

![ex_thr_met_hist.png](docs/media/readme/ex_thr_met_hist.png)

- `roi_match_plane#_idx###-###.png` visualises a window of the mean gcamp image around an example match for all days. If there is more than 100 matches, they are split to separate figures. The dot in the middle shows the centroid of the ROI (whole ROI is not drawn to not bias the estimation of match).

![ex_roi_match.png](docs/media/readme/ex_roi_match.png)

- `all_roi_match.png` visualises all matches across the FOV for all days. Here the full ROIs are drawn and the color is maintained across days.

![ex_all_roi_match.png](docs/media/readme/ex_all_roi_match.png)


