import numpy as np
import os

from track2p.io.utils import make_dir

def save_track_ops(track_ops):
    np.save(os.path.join(track_ops.save_path, 'track_ops_postreg.npy'), track_ops, allow_pickle=True)
    print('Saved track_ops_postreg.npy in ' + track_ops.save_path)

def save_all_pl_match_mat(all_pl_match_mat, track_ops):
    for (i, all_pl_match_mat) in enumerate(all_pl_match_mat):
        np.save(os.path.join(track_ops.save_path, f'plane{i}_match_mat.npy'), all_pl_match_mat, allow_pickle=True)