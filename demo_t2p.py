from track2p.run_t2p import run_t2p
from track2p.ops.default import DefaultTrackOps


if __name__ == '__main__':

    # Get default parameters
    track_ops = DefaultTrackOps()

    # TODO Manon: add gui integration here
    # track_ops = get_track_ops_from_gui() # for example

    # for now parameters are defined manually:
    track_ops.all_ds_path = [
            'data_proc/jm/jm019/2023-04-05_a',
            'data_proc/jm/jm019/2023-04-06_a',
            'data_proc/jm/jm019/2023-04-07_a',
            'data_proc/jm/jm019/2023-04-08_a',
            'data_proc/jm/jm019/2023-04-10_a',
            ]

    track_ops.save_path = 'data_proc/jm/jm019/' # path where to save the outputs of algorithm (a 'track2p' folder will be created where figures for visualisation and matrices of matches would be saved)
    track_ops.reg_chan = 1 # channel to use for registration (0=functional, 1=anatomical) (use 0 if only recording gcamp!)

    # Run the algorithm
    run_t2p(track_ops)

    # TODO Manon: add gui integration here? To display results once done computing

