# contains code for generating plots based on track_ops object after the pipeline is run (this will be saved as an npy file)
# here all functions just take the track_ops object as input

import numpy as np
import matplotlib.pyplot as plt

from skimage.exposure import match_histograms
from track2p.plot.utils import make_rgb_img, saturate_perc, get_all_wind_mean_img

def plot_reg_img_output(track_ops):
    # make a plot where on the top its all the images and the bottom is the overlays before and after registration
    nplanes = track_ops.nplanes
    n_row = nplanes + 2*nplanes # number of plays + 2 overlays per plane
    n_col = len(track_ops.all_ds_path) # number of datasets
    figsize = (10/3 * n_col, 10/3 * n_row)
    fig, axs = plt.subplots(n_row, n_col, figsize=figsize, dpi=300)

    # first populate first (n_planes) rows with images
    for i in range(nplanes):
        axs[i, 0].set_ylabel(f'plane{i}\nchan{track_ops.reg_chan}', rotation=0, size='large', ha='right', va='center', labelpad=20)
        for j in range(len(track_ops.all_ds_path)):
            img = track_ops.all_ds_avg_ch1[j][i] if track_ops.reg_chan==0 else track_ops.all_ds_avg_ch2[j][i]
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

        if i == 0:
            for k in range(nplanes):
                axs[nplanes + 2*k,i].set_ylabel(f'plane{k}\nchan{track_ops.reg_chan}\nnon-reg', rotation=0, size='large', ha='right', va='center', labelpad=20)
                axs[nplanes + 2*k+1,i].set_ylabel(f'plane{k}\nchan{track_ops.reg_chan}\nreg', rotation=0, size='large', ha='right', va='center', labelpad=20)

            # loop through all subplots and remove ticks and labels and spines

    for ax in axs.flat:
        ax.set(xticks=[], yticks=[])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    # add arrows and dashed lines etc.

    axs[2*nplanes, 0].annotate('', xy=(0, 1.1), xytext=(n_col + 0.5, 1.1), 
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
    

    # save figure into the output path
    fig.savefig(track_ops.save_path_fig + 'reg_img_output.png', bbox_inches='tight', dpi=200)


def plot_roi_reg_output(track_ops):
    # make a plot where on the top its all the images and the bottom is the overlays before and after registration
    nplanes = track_ops.nplanes
    n_row = nplanes + 2*nplanes # number of plays + 2 overlays per plane
    n_col = len(track_ops.all_ds_path) # number of datasets
    figsize = (10/3 * n_col, 10/3 * n_row)
    # figsize = (10 * n_col, 10 * n_row)

    fig, axs = plt.subplots(n_row, n_col, figsize=figsize, dpi=300)

    # first populate first (n_planes) rows with images
    for i in range(nplanes):
        axs[i, 0].set_ylabel(f'plane{i}\nchan{track_ops.reg_chan}', rotation=0, size='large', ha='right', va='center', labelpad=20)
        for j in range(len(track_ops.all_ds_path)):
            img = track_ops.all_ds_avg_ch1[j][i]
            axs[i, j].imshow(img, cmap='gray', vmin=0, vmax=np.percentile(img, 99), alpha=0.5)
            # take the rois of reference unless it is last on, then take the rois of the mov
            all_roi = track_ops.all_ds_all_roi_array_ref[j][i] if j < len(track_ops.all_ds_path)-1 else track_ops.all_ds_all_roi_array_mov[j-1][i]
            for k in range(all_roi.shape[2]):
                axs[i, j].contour(all_roi[:,:,k], colors='C0', linewidths=0.3)

    # now populate the next (n_planes) rows with the overlays before registration
    for i in range(len(track_ops.all_ds_path)-1):
        print(f'Plotting contours for dataset {i}/{len(track_ops.all_ds_path)-1}')
        for j in range(track_ops.nplanes):

            row_nonreg = nplanes + 2*j # first shift for number of initial rows, then shift by 2 for each plane (before and after registration)
            row_reg = nplanes + 2*j + 1 # the row after the nonreg

            all_roi_array_ref = track_ops.all_ds_all_roi_array_ref[i][j]

            all_roi_array_mov = track_ops.all_ds_all_roi_array_mov[i][j]
            ref_mov_inters = track_ops.all_ds_ref_mov_inters[i][j]

            axs[row_nonreg,i].imshow(ref_mov_inters)
            for k in range(all_roi_array_ref.shape[2]):
                axs[row_nonreg,i].contour(all_roi_array_ref[:,:,k], colors='r', linewidths=0.3)
            for k in range(all_roi_array_mov.shape[2]):
                axs[row_nonreg,i].contour(all_roi_array_mov[:,:,k], colors='g', linewidths=0.3)

            # TODO: for reg row
            all_roi_array_reg = track_ops.all_ds_all_roi_array_reg[i][j]
            ref_reg_inters = track_ops.all_ds_ref_reg_inters[i][j]

            axs[row_reg,i].imshow(ref_reg_inters)
            for k in range(all_roi_array_ref.shape[2]):
                axs[row_reg,i].contour(all_roi_array_ref[:,:,k], colors='r', linewidths=0.3)
            for k in range(all_roi_array_reg.shape[2]):
                axs[row_reg,i].contour(all_roi_array_reg[:,:,k], colors='g', linewidths=0.3)

        if i == 0:
            for k in range(nplanes):
                axs[nplanes + 2*k,i].set_ylabel(f'plane{k}\nnon-reg', rotation=0, size='large', ha='right', va='center', labelpad=20)
                axs[nplanes + 2*k+1,i].set_ylabel(f'plane{k}\nreg', rotation=0, size='large', ha='right', va='center', labelpad=20)


    for ax in axs.flat:
        ax.set(xticks=[], yticks=[])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)     

    # add arrows and dashed lines etc.

    axs[2*nplanes, 0].annotate('', xy=(0, 1.1), xytext=(n_col + 0.5, 1.1), 
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(arrowstyle='-', linestyle='dashed', color='grey'), 
                annotation_clip=False)

    for i in range(len(track_ops.all_ds_path)-1):
        axs[nplanes-1,i].annotate('', xy=(0.5, -0.17), xytext=(0.5, -0.02), 
                        xycoords='axes fraction', textcoords='axes fraction',
                        arrowprops=dict(facecolor='r', edgecolor='r', shrink=0.05), 
                        annotation_clip=False)
        axs[nplanes-1,i+1].annotate('', xy=(-0.6, -0.17), xytext=(0.5, -0.02), 
                        xycoords='axes fraction', textcoords='axes fraction',
                        arrowprops=dict(facecolor='g', edgecolor='g', shrink=0.05), 
                        annotation_clip=False)
    

    # save figure into the output path
    fig.savefig(track_ops.save_path_fig + 'reg_roi_output.png', bbox_inches='tight', dpi=200)     


def plot_thr_met_hist(all_ds_thr_met, all_ds_thr, track_ops):
    fig, axs = plt.subplots(track_ops.nplanes, len(all_ds_thr_met), figsize=(6*len(all_ds_thr_met), 6*track_ops.nplanes), sharey=True, sharex=True)
    for i in range(len(all_ds_thr_met)):
        for j in range(track_ops.nplanes):
            this_ax = axs[i] if track_ops.nplanes==1 else axs[j][i]
            n_reg_roi = len(all_ds_thr_met[i][j])
            n_abovethr_roi = np.sum(all_ds_thr_met[i][j]>all_ds_thr[i][j])
            this_ax.hist(all_ds_thr_met[i][j], bins=20)
            this_ax.axvline(all_ds_thr[i][j], color='grey', linestyle='--')
            # label the line with 'otsu threshold'
            this_ax.text(all_ds_thr[i][j]+0.02, this_ax.get_ylim()[1]*0.9, f'otsu thr.: {all_ds_thr[i][j]:.2f}')
            this_ax.set_title(f'ds_ref{i}, ds_reg:{i+1} (above_thr {n_abovethr_roi}/{n_reg_roi} rat. {n_abovethr_roi/n_reg_roi:.2f})')
            
            if i==0:
                this_ax.set_ylabel(f'ROI count (plane{j})')
    
    # remove the top and right spines
    for a in axs.flatten():
        a.spines['top'].set_visible(False)
        a.spines['right'].set_visible(False)

    
    plt.tight_layout()
    plt.show()


def plot_roi_match(all_ds_mean_img, all_ds_centroids, all_pl_match_mat, neuron_ids, track_ops, plane_idx=0, win_size=64):

    nrows = len(neuron_ids)
    ncols = len(all_ds_mean_img)
    fig, axs = plt.subplots(nrows, ncols, figsize=(2*ncols, 2*nrows), dpi=100)

    for (i, nrn_id) in enumerate(neuron_ids):
        # check if neuron is not matched (if ith row of all_pl_match_mat is all None)
        if any(all_pl_match_mat[plane_idx][nrn_id,:]==None):
            continue
        
        # get all wind_mean_img (small window around centroid)
        all_wind_mean_img = get_all_wind_mean_img(all_ds_mean_img, all_ds_centroids, all_pl_match_mat, nrn_id, plane_idx=plane_idx, win_size=win_size)
           
        for j in range(len(all_ds_mean_img)):
            wind_mean_img = all_wind_mean_img[j]
            ref_img = all_wind_mean_img[0]
            matched = match_histograms(wind_mean_img, ref_img)
            axs[i, j].imshow(matched, cmap='gray')
            # scatter middle pixel of the window
            axs[i, j].scatter(win_size/2, win_size/2, color='C0')
            if i==0:
                axs[i, j].set_title(f'ds {j} (pl {plane_idx})')
            if j==0:
                axs[i, j].set_ylabel(f'ROI {nrn_id} ({i}/{nrows})')

    # remove axes labels
    for ax in axs.flat:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.savefig(track_ops.save_path_fig + f'roi_match_plane{plane_idx}.png', dpi=100)
    plt.show()

def plot_roi_match_multiplane(all_ds_mean_img, all_ds_centroids, all_pl_match_mat, track_ops, win_size=48):

    for i in range(track_ops.nplanes):
        pl_neuron_ids = np.arange(all_pl_match_mat[i].shape[0])
        for j in range(len(track_ops.save_path)):
            neuron_ids = pl_neuron_ids[~np.any(all_pl_match_mat[i]==None, axis=1)]

        plot_roi_match(all_ds_mean_img, all_ds_centroids, all_pl_match_mat, neuron_ids, track_ops, plane_idx=i, win_size=win_size)