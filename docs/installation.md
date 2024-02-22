# Installation
### --- UNDER CONSTRUCTION ---

### Issues with ITK library installation
In some cases updating anaconda helped (the procedure in the readme was written based on version 23.11.0).


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