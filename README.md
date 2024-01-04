# track2p
Cell tracking for longitudinal calcium imaging recordings.

# Installation

Set up conda environment with python 3.9

```
conda create --name track2p python=3.9
conda activate track2p
```

Install dependencies:
```
conda install -c conda-forge matplotlib
conda install -c conda-forge numpy
conda install -c conda-forge scikit-image
pip install itk-elastix
```

(TODO: make pip-installable)

Then clone the repo:
```
git clone https://github.com/juremaj/track2p
```

cd to the directory:
```
cd track2p
```

And install the local package (all modules within the track2p subfolder):
```
pip install -e .
```