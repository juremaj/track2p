# Installation
### --- UNDER CONSTRUCTION ---

### Issues with ITK elastix installation
In some cases updating anaconda helped (the procedure in the readme was written based on version 23.11.0).

Otherwise manually building the environment could be an option.

We make the environment as usual:
```
conda create --name track2p python=3.9
conda activate track2p
```

In the next step we need to specify that we will not install dependencies automatically from pip:
```
pip install track2p --no-deps
```

Then we manually install the dependencies (see `setup.py` in root of `track2p`). For version `track2p=0.5.0` we can manually install the dependecies using:
```
pip install numpy==1.23.5 &&
pip install matplotlib==3.5.3 &&
pip install scikit-image==0.20.0 &&
pip install itk-elastix==0.19.1 &&
pip install PyQt5==5.15.10 &&
pip install qtpy==2.4.1 &&
pip install tqdm==4.66.2 &&
pip install scikit-learn==1.4.0 &&
pip install openTSNE==1.0.1
```
Note: usually saving ITK errors can be solved by changing the itk-elastix version, for example from `pip install itk-elastix==0.19.1` to `pip install itk-elastix==0.19.0` or vice versa.

If this is successful you can just run the algorithm as usual:
```
python -m track2p
```

### Platform specific installation issues/requirements:
**MacOS**: You might need to have xcode enabled during installation. If you run into `xcrun: error: invalid active developer path .../.../... , missing xcrun at .../.../... ` then enable xcode by running: `xcode-select --install`

**Linux Ubuntu**: Everything works well.

**Windows**: (not tested yet)


### Installation via GitHub (discouraged)

Alternatively track2p can also be installed directly from the Github repository (this is currently discouraged, since the repo is under active development).
To install via Github run:

```
conda create --name track2p python=3.9
conda activate track2p
git clone https://github.com/juremaj/track2p
cd track2p
pip install -e .
```