### --- UNDER CONSTRUCTION ---



## Matches

There are two types of output from track2p:

- A matrix (`plane#_match_mat.npy`) containing the indices of matched neurons across the session for a given plane (`#` is the index of the plane). Since matching is done from first day to last, some neurons will not be sucessfully tracked after one or a few days. In this case the matrix contains `None` values. To get neurons tracked across all days only take the rows of the matrices containing no `None` values. 

- A `track_ops.npy` object that contains the parameters used for the algorithm and some intermediate results that can be used for visualisations (e. g. registered images and ROIs etc.)
