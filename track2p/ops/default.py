# make dummy track_ops object (would be input from command line or gui)
import os
from track2p.io.utils import make_dir

class DefaultTrackOps:
    def __init__(self):
        # input list of dataset paths (each contains a 'suite2p' folder)
        self.all_ds_path = [
            'data/ac/ac444118/2022-09-14_a',
            'data/ac/ac444118/2022-09-15_a',
            'data/ac/ac444118/2022-09-16_a'
        ]
        # self.all_ds_path = [
        #     # 'data/jm/jm032/2023-10-18_a/',
        #     'data/jm/jm032/2023-10-19_a/',
        #     'data/jm/jm032/2023-10-20_a/',
        #     'data/jm/jm032/2023-10-21_a/',
        #     'data/jm/jm032/2023-10-22_a/',
        #     'data/jm/jm032/2023-10-23_a/'
        #     ]
        
        self.save_path = 'data/ac/ac444118/track2p/'
        # self.save_path = 'data/jm/jm032/track2p/'
        self.reg_chan = 0 # channel to use for registration (0=functional, 1=anatomical) (1 is not always available)
        self.transform_type = 'affine' # 'affine' or 'nonrigid'
        self.iscell_thr = 0.50 # threshold for iscell.npy (only keep ROIs with iscell > iscell_thr) (here lowering this can be good and non-detrimental -> artefacts are unlikely to be consistently present in all datasets)

        self.matching_method='iou' # 'iou', 'cent' or 'cent_int-filt'  (iou takes longer but is more accurate, cent is faster but less accurate)
        self.iou_dist_thr = 16 # distance between centroids (in pixels) above which to skip iou computation (to save time) (this is only relevant if self.matching_method=='iou')

        self.thr_remove_zeros = False # remove zeros from thr_met before computing automatic threshold (this is useful when there are many zeros in thr_met, which can skew the thresholding)
        self.thr_method = 'min' # 'otsu' or 'min' (min is just local minimum of pdf of thr_met)

        # do not change these
        self.show_roi_reg_output = False # this is slow because plt.contour is slow and also very memory intensive(it can easily crash) but the visualisation is nice for presentations (for example by increasing self.iscell_thr)

        # plotting parameters
        self.win_size = 48 # window size for visualising matched ROIs across days (crop of mean image)
        self.sat_perc = 99.9 # percentile to saturate image at (only affects visualisation not the registration/matching)

        # make the output directories when initialising the object
        
    def init_save_paths(self):
        self.save_path = os.path.join(self.save_path, 'track2p/')
        self.save_path_fig = os.path.join(self.save_path, 'fig/')
        make_dir(self.save_path)
        make_dir(self.save_path_fig)
