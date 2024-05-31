### --- UNDER CONSTRUCTION ---

## Setting up `run_track2p.py`

- `track_ops.all_ds_path`: list of paths to datasets containing a `suite2p` folder 
- `track_ops.save_path`: where the outputs will be saved (a `track2p` folder will be generated here)
- `track_ops.reg_chan` : channel to use for registration (0=functional, 1=anatomical) 

## supplementary track.ops parameters (GUI)

-  `track_ops.colors`: It's a color vector assigning a specific color to each cell. When the user opens a track2Pp dataset, each cell retains the same color at each opening.
A vector is created per plane `colors_plane_x`
- `track_ops.save_in_s2p_format` :  allows to generate the suite2p files containing only the cells present on every day 
- `track_ops.vector_curation` : It is a vector of the length of the number of cells found every day by our algorithm. It represents the state of each cell, varying between 0 and 1, where 0 means that it is considered "not cell" by the user, and 1 means that it is recognized as a "cell". It is appallingly updated by the user’s choice. 
A vector is created per plane `vector_curation_plane_x`

(for basic documentation see comments in `track2p/ops/default.py`, more documentation will be added soon).

