# make dummy track_ops object (would be input from command line or gui)

from track2p.io.utils import make_dir

class DefaultTrackOps:
    def __init__(self):
        # input list of dataset paths (each contains a 'suite2p' folder)
        # self.all_ds_path = [
        #     'data/ac/ac444118/2022-09-14_a',
        #     'data/ac/ac444118/2022-09-15_a',
        #     'data/ac/ac444118/2022-09-16_a'
        # ]
        self.all_ds_path = [
            'data/jm/jm032/2023-10-18_a/',
            'data/jm/jm032/2023-10-19_a/',
            'data/jm/jm032/2023-10-20_a/',
            'data/jm/jm032/2023-10-21_a/',
            'data/jm/jm032/2023-10-22_a/',
            'data/jm/jm032/2023-10-23_a/'
            ]
        # self.save_path = 'data/ac/ac444118/track2p/'
        self.save_path = 'data/jm/jm032/track2p/'
        self.reg_chan = 1 # channel to use for registration (0=functional, 1=anatomical) (1 is not always available)
        self.transform_type = 'affine' # 'affine' or 'nonrigid'
        self.sat_perc = 99 # percentile to saturate image at (only affects visualisation not the registration/matching)
        self.iscell_thr = 0.50 # threshold for iscell.npy (only keep ROIs with iscell > iscell_thr) (here lowering this can be good and non-detrimental -> artefacts are unlikely to be present in all datasets)
        # do not change these
        self.save_path_fig = self.save_path + 'figures/'
        self.show_roi_reg_output = False # this is slow because plt.contour is slow and also very memory intensive(it can easily crash)
        self.matching_method='cent_int-filt' # 'cent_int-filt' or 'cent_int'  (TODO: implement iou method from original algo)

        # make the output directories when initialising the object
        make_dir(self.save_path)
        make_dir(self.save_path_fig)
