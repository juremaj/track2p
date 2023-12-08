# make dummy track_ops object (would be input from command line or gui)
class DefaultTrackOps:
    def __init__(self):
        # input list of dataset paths (each contains a 'suite2p' folder)
        self.all_ds_path = [
            'data/jm/jm032/2023-10-19_a/',
            'data/jm/jm032/2023-10-20_a/',
            'data/jm/jm032/2023-10-21_a/'
        ]
        self.save_path = 'data/jm/jm032/tracking/'
        self.reg_chan = 1 # channel to use for registration (0=functional, 1=anatomical) (1 is not always available)
        self.transform_type = 'affine' # 'affine' or 'nonrigid'
        self.sat_perc = 99 # percentile to saturate image at (only affects visualisation not the registration/matching)
