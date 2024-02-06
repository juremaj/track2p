import numpy as np
import os

from track2p.io.utils import make_dir

def save_track_ops(track_ops):
    # remove attributes taking a lot of memory (e.g. rois etc.)
    del track_ops.all_ds_all_roi_array_mov
    del track_ops.all_ds_all_roi_array_ref
    del track_ops.all_ds_all_roi_array_reg

    track_ops_dict = track_ops.to_dict() # convert to dictionary for compatibility
    
    np.save(os.path.join(track_ops.save_path, 'track_ops.npy'), track_ops_dict, allow_pickle=True)
    print('Saved track_ops.npy in ' + track_ops.save_path)

def save_all_pl_match_mat(all_pl_match_mat, track_ops):
    for (i, all_pl_match_mat) in enumerate(all_pl_match_mat):
        np.save(os.path.join(track_ops.save_path, f'plane{i}_match_mat.npy'), all_pl_match_mat, allow_pickle=True)