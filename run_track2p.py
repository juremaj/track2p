from track2p.t2p import run_t2p
from track2p.ops.default import DefaultTrackOps


if __name__ == '__main__':

    # Get default parameters
    track_ops = DefaultTrackOps()

    # TODO Manon: add gui integration here
    # track_ops = get_track_ops_from_gui() # for example

    # for now parameters are defined manually:
    track_ops.all_ds_path = [
                '/Users/manonmantez/el017/2023-02-21_a',
                '/Users/manonmantez/el017/2023-02-22_a',
            ]

    track_ops.save_path = '/Users/manonmantez/el017/' # path where to save the outputs of algorithm (a 'track2p' folder will be created where figures for visualisation and matrices of matches would be saved)
    track_ops.reg_chan = 0 # channel to use for registration (0=functional, 1=anatomical) (use 0 if only recording gcamp!)
    track_ops.iscell_thr = 0.25

    # Run the algorithm
    run_t2p(track_ops)

    # TODO Manon: add gui integration here? To display results once done computing

