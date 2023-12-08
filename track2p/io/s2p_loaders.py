import os
import numpy as np

def check_nplanes(track_ops):
    all_nplanes = []

    for ds_path in track_ops.all_ds_path:
        # check how many subfolders starting with plane* in suite2p folder
        n_planes = len([name for name in os.listdir(ds_path + '/suite2p') if name.startswith('plane')])
        print(f'Found {n_planes} planes in {ds_path}')
        all_nplanes.append(n_planes)
    track_ops.all_nplanes = all_nplanes
    # if all elements in all_n_planes are the same, then save it in track_ops.n_planes
    if all_nplanes.count(all_nplanes[0]) == len(all_nplanes):
        track_ops.nplanes = all_nplanes[0]
        print(f'Found {track_ops.nplanes} planes in all datasets')
    else:
        print('Found different number of planes in different datasets')
        print('Please check your dataset paths')
        print('Exiting...')
        exit()


# loads mean images
def load_all_imgs(track_ops):
    all_ds_avg_ch1 = []
    all_ds_avg_ch2 = []
    all_ds_nchannels = []

    for ds_path in track_ops.all_ds_path:
        ds_nchannels = []
        ds_avg_ch1 = []
        ds_avg_ch2 = []

        for i in range(track_ops.nplanes):
            ops = np.load(ds_path + '/suite2p/plane' + str(i) + '/ops.npy', allow_pickle=True).item()
            nchannels = ops['nchannels']
            print('nchannels: ' + str(nchannels) + ' for plane ' + str(i) + ' in dataset ' + ds_path)
            ds_avg_ch1.append(ops['meanImg'])
            ds_avg_ch2.append(ops['meanImg_chan2']) if nchannels==2 else ds_avg_ch2.append(None)
            ds_nchannels.append(nchannels)

        all_ds_avg_ch1.append(ds_avg_ch1)
        all_ds_avg_ch2.append(ds_avg_ch2)
        all_ds_nchannels.append(ds_nchannels)

    track_ops.all_ds_avg_ch1 = all_ds_avg_ch1
    track_ops.all_ds_avg_ch2 = all_ds_avg_ch2
    track_ops.all_ds_nchannels = all_ds_nchannels

    # if all elements in all_ds_nchannels are the same, then print its fine otherwise exit
    if all_ds_nchannels.count(all_ds_nchannels[0]) == len(all_ds_nchannels):
        track_ops.nchannels = all_ds_nchannels[0][0]
        print(f'Found {track_ops.nchannels} channels in all datasets')
    else:    
        print('Found different number of channels in different datasets')
        print('Please check your dataset paths')
        print('Exiting...')
        exit()

    return all_ds_avg_ch1, all_ds_avg_ch2