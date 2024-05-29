### --- UNDER CONSTRUCTION ---


## Changing algorithm parameters

TODO: add documentation of algorithm parameters (for now use the defaults saved at `track2p/ops/default.py`, they should work well). If some parameters should be overwritten its recommended to do so in the `run_track2p.py` script (see section above).


## Setting up `run_track2p.py`

`run_track2p.py` script in the root of the directory and specifies:

- `track_ops.all_ds_path`: list of paths to datasets containing a `suite2p` folder
- `track_ops.save_path`: where the outputs will be saved (a `track2p` folder will be generated here)
- `track_ops.save_in_s2p_format `---` being different parameter names overwriting the defaults (for basic documentation see comments in `track2p/ops/default.py`, more documentation will be added soon).

