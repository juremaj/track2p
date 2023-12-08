import numpy as np

def load_track_ops(track_ops_path):
    track_ops = np.load(track_ops_path + 'track_ops_postreg.npy', allow_pickle=True).item()
    return track_ops