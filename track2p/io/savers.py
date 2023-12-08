import numpy as np

from track2p.io.utils import make_dir

def save_track_ops(track_ops):
    np.save(track_ops.save_path + '/track_ops_postreg.npy', track_ops, allow_pickle=True)
    print('Saved track_ops_postreg.npy in ' + track_ops.save_path)
