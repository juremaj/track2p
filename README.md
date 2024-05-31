# track2p
Cell tracking for longitudinal calcium imaging recordings.

[![PyPI version](https://img.shields.io/pypi/v/track2p)](https://pypi.org/project/track2p/)
[![All time downloads](https://static.pepy.tech/badge/track2p)](https://pepy.tech/project/track2p)
[![Monthly downloads](https://img.shields.io/pypi/dm/track2p)](https://pypi.org/project/track2p/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

___
Note: We are actively developing the software for the next couple of months, so we would greatly appreciate any feedback! You can raise it as an [issue](https://github.com/juremaj/track2p/issues) on GitHub or contact us directly. Thanks!
___


# Installation

## Installing via pip

First we need to set up a conda environment with python 3.9:

```
conda create --name track2p python=3.9
conda activate track2p
```

Then simply install the track2p package using pip:

```
pip install itk-elastix==0.19.1 --no-deps
pip install track2p
```

Thats it, track2p should be succesfully set up :)
You can simply run it by:

```
python -m track2p
```

This opens a GUI allowing the user to launch the algorithm and visualise the results interactively.

(For instructions on running track2p without the GUI see the 'Run via script' under the 'Usage' section)

Note: For common installation issues see [documentation](https://github.com/juremaj/track2p/blob/main/docs/installation.md).

## Reinstall

To reinstall, open anaconda and remove the environment with:

```
conda env remove -n track2p
```

Then follow the 'Installing via pip' instructions above :)


# Usage

## Run track2p through the GUI

After activating the GUI through `python -m track2p` the user should navigate to the 'Run' tab on the top left of the window and select 'Run track2p algorithm' from the dropdown menu. This will open a pop-up window that will allow the user to set the paths to suite2p datasets and to set the algorithm parameters. After configuring these settings, the user can click 'Run' to run the track2p algorithm, and the progress will be displayed in the terminal.

Then, once the algorithm completes its tasks, a subsequent pop-up window will prompt the user to decide whether they wish to visualize the results (of a specific plane) within the interface.

For more details on how to run the algorithm through the GUI see [run track2p](https://github.com/juremaj/track2p/blob/main/docs/gui.md) and for more description of parameters see documentation [parameters](https://github.com/juremaj/track2p/blob/main/docs/parameters.md).

## Using the GUI

_ _Here we assume that each of the recording is **same imaging frequency**, **number of planes** and **number of channels** (otherwise might not work, or we cant guarantee)_ _

After activating the GUI through python -m track2p the user can download the results of any previous analysis by clicking on 'File' tab on the top left of the window and select 'Load processed data' from the dropdown menu. This will open a pop-up window that will allow the user to set the path to the track2p folder (containing the results of the algorithm) and the plane he wants to open. 

Once completed, the interface showcases multiple visualizations.
In the upper left, the 'mean image' produced by suite2p for each day are displayed, showing the cells detected by track2p on every day. These images are interactive, allowing the user to click on a cell, which will display the fluorescence traces of each day at the bottom of the window (from the first day to the last). In addition, a zoom on the cell in each day is shown in the top right, with its index in the 'suite2p’ dataset of the corresponding day and the probability that it has assigned suite2p (iscell.npy). Finally, the user can browse all the cells detected by our algorithm using the bar at the bottom or enter a specific number. Finally, the user can evaluate the quality of the tracking for each cell, and annotate the results according to its correction. 

For more details on how to use the GUI see [GUI usage](https://github.com/juremaj/track2p/blob/main/docs/gui.md)

Below is an example of a mouse imagined over 7 days (P-P) on one plane (with `track_ops.iscell_thr=0.25` and `track_ops.reg_chan = 1`)

![]([media/plots/ex_all_vizualizations.png](https://github.com/juremaj/track2p/blob/main/docs/media/plots/ex_all_vizualizations.png))



## Run via script

To run via script you can use the `run_track2p.py` script in the root of this repo as a template. It is exactly the same as running thrugh the gui, only that the paths and the parameters are defined within the script (for more on parameters etc. see documentation). When running make sure you are running it within the track2p environment, for example:

```
conda activate track2p
python -m run_track2p
```

# Outputs

All the outputs of the script will be saved in a `track2p` folder created within the `track_ops.save_path` directory specified by the user when running the algorithm. For an introduction on how to use the outputs for further downstream analysis we provide a useful demo notebook `demo_t2p_output.ipynb` in the root of this repository. Note: You will need to additionally install jupyter for this to work. For example:

```
conda install conda-forge::jupyterlab
```

For more information see documentation relating to track2p [viusalisations](https://github.com/juremaj/track2p/blob/main/docs/visualisations.md) and [outputs](https://github.com/juremaj/track2p/blob/main/docs/outputs.md).

# Reference

For now if you use the algorithm please reference the Cosyne abstract:

  **Majnik, J., Zangila, S., Cossart, R. & Platel, J. C. (2024). _Emergence of state modulation in a developing cortical circuit_. COSYNE Abstract.**

  

You can also see the YouTube recording of the talk for a reference use-case in neocortical development: [Link to video (starting at 47:20)](https://youtu.be/Tr97HwgQ9ik?t=2839)
