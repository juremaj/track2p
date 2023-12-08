# contains code for generating plots based on track_ops object after the pipeline is run (this will be saved as an npy file)
# here all functions just take the track_ops object as input

import numpy as np
import matplotlib.pyplot as plt

from skimage.exposure import match_histograms
from track2p.plot.utils import make_rgb_img, saturate_perc

def plot_reg_output(track_ops):
    # make a plot where on the top its all the images and the bottom is the overlays before and after registration
    nplanes = track_ops.nplanes
    n_row = nplanes + 2*nplanes # number of plays + 2 overlays per plane
    n_col = len(track_ops.all_ds_path) # number of datasets
    fig, axs = plt.subplots(n_row, n_col, figsize=(10, 10))

    # first populate first (n_planes) rows with images
    for i in range(nplanes):
        axs[i, 0].set_ylabel(f'plane{i}', rotation=0, size='large', ha='right', va='center', labelpad=20)
        for j in range(len(track_ops.all_ds_path)):
            img = track_ops.all_ds_avg_ch1[j][i]
            axs[i, j].imshow(img, cmap='gray', vmin=0, vmax=np.percentile(img, 99))


    for i in range(len(track_ops.all_ds_path)-1): # last one won't have overlay
        for j in range(nplanes):
            # get subplot indices
            row_nonreg = nplanes + 2*j # first shift for number of initial rows, then shift by 2 for each plane (before and after registration)
            row_reg = nplanes + 2*j + 1 # the row after the nonreg

            # get images
            ref_img = track_ops.all_ds_ref_img[i][j] # get ref image for this pair
            mov_img = track_ops.all_ds_mov_img[i][j] # get mov image for this pair
            mov_img_ref = track_ops.all_ds_mov_img_reg[i][j] # get mov image after registration for this pair

            # match histograms to reference
            mov_img = match_histograms(mov_img, ref_img)
            mov_img_ref = match_histograms(mov_img_ref, ref_img)

            # assemble and saturate the overlays
            img_rgb = make_rgb_img(ref_img, mov_img)
            img_rgb_reg = make_rgb_img(ref_img, mov_img_ref)
            img_rgb = saturate_perc(img_rgb, sat_perc=track_ops.sat_perc)
            img_rgb_reg = saturate_perc(img_rgb_reg, sat_perc=track_ops.sat_perc)

            # plot the overlays
            axs[row_nonreg, i].imshow(img_rgb)
            axs[row_reg, i].imshow(img_rgb_reg)
            
            # get pre and post-registration images form ops
        if i == 0:
            axs[row_nonreg,i].set_ylabel(f'plane{j} \n non-reg', rotation=0, size='large', ha='right', va='center', labelpad=20)
            axs[row_reg,i].set_ylabel(f'plane{j} \n reg', rotation=0, size='large', ha='right', va='center', labelpad=20)

            # loop through all subplots and remove ticks and labels and spines

    for ax in axs.flat:
        ax.set(xticks=[], yticks=[])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    # add arrows and dashed lines etc.

    axs[2*nplanes, 0].annotate('', xy=(0, 1.1), xytext=(3.5, 1.1), 
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(arrowstyle='-', linestyle='dashed', color='grey'), 
                annotation_clip=False)

    for i in range(len(track_ops.all_ds_path)-1):
        axs[nplanes-1,i].annotate('', xy=(0.5, -0.17), xytext=(0.5, -0.02), 
                        xycoords='axes fraction', textcoords='axes fraction',
                        arrowprops=dict(facecolor=(1,0,0), edgecolor=(1,0,0), shrink=0.05), 
                        annotation_clip=False)
        axs[nplanes-1,i+1].annotate('', xy=(-0.6, -0.17), xytext=(0.5, -0.02), 
                        xycoords='axes fraction', textcoords='axes fraction',
                        arrowprops=dict(facecolor=(0,1,0), edgecolor=(0,1,0), shrink=0.05), 
                        annotation_clip=False)