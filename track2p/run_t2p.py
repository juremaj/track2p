from track2p.ops.default import DefaultTrackOps

from track2p.io.s2p_loaders import load_all_imgs, check_nplanes, load_all_ds_stat_iscell, load_all_ds_mean_img, load_all_ds_centroids
from track2p.io.savers import save_track_ops, save_all_pl_match_mat

from track2p.register.loop import run_reg_loop, reg_all_ds_all_roi
from track2p.register.utils import get_all_ds_img_for_reg, get_all_ref_nonref_inters

from track2p.plot.progress import plot_all_planes
from track2p.plot.output import plot_reg_img_output, plot_thr_met_hist, plot_roi_reg_output, plot_roi_match_multiplane, plot_allroi_match_multiplane

from track2p.match.loop import get_all_ds_assign, get_all_pl_match_mat 


def run_t2p(track_ops):

    # 1) initialise save paths for figures and matched neurons output
    track_ops.init_save_paths()

    # 2) Load data
    check_nplanes(track_ops)
    all_ds_avg_ch1, all_ds_avg_ch2 = load_all_imgs(track_ops)

    # 3) Plot available planes for registration
    plot_all_planes(all_ds_avg_ch1, track_ops)
    if track_ops.nchannels==2:
        plot_all_planes(all_ds_avg_ch2, track_ops)

    # 4) do the actual registration based on chosen channel
    all_ds_ref_img, all_ds_mov_img = get_all_ds_img_for_reg(all_ds_avg_ch1, all_ds_avg_ch2, track_ops)
    all_ds_mov_img_reg, all_ds_reg_params = run_reg_loop(all_ds_ref_img, all_ds_mov_img, track_ops) # TODO: save basic parameters for each registration as feedback (e. g. ammoung of shift, rotation, etc.) for later plotting
    plot_reg_img_output(track_ops)

    # 5) apply computed transorm to all ROIs
    all_ds_all_roi_ref, all_ds_all_roi_mov, all_ds_all_roi_reg, all_ds_roi_counter = reg_all_ds_all_roi(all_ds_reg_params, track_ops)

    # 6) optional: generate 'yellow intersection' plot (this is only needed for plotting below)
    all_ds_ref_reg_inters = get_all_ref_nonref_inters(all_ds_all_roi_ref, all_ds_all_roi_reg, track_ops)
    all_ds_ref_mov_inters = get_all_ref_nonref_inters(all_ds_all_roi_ref, all_ds_all_roi_mov, track_ops)

    track_ops.all_ds_ref_mov_inters = all_ds_ref_mov_inters
    track_ops.all_ds_ref_reg_inters = all_ds_ref_reg_inters

    # this line is very memory-intensive because of the ROIS (TODO: maybe instead of contours just plot RGB) (or somehow generate RGB image of contours (in the part before))
    if track_ops.show_roi_reg_output:
        plot_roi_reg_output(track_ops)

    # 7) get optimal assignments for all pairs of recordings (first to last)
    all_ds_assign, all_ds_assign_thr, all_ds_thr_met, all_ds_thr = get_all_ds_assign(track_ops, all_ds_all_roi_ref, all_ds_all_roi_reg)
    plot_thr_met_hist(all_ds_thr_met, all_ds_thr, track_ops)

    # 8) get match matrices for all pairs of recordings (first to last)
    all_pl_match_mat = get_all_pl_match_mat(all_ds_all_roi_ref, all_ds_assign_thr, track_ops)

    # 9) save results
    save_track_ops(track_ops)
    save_all_pl_match_mat(all_pl_match_mat, track_ops)

    # 10) plot results
    print('Generating plots (this can take some time)...')
    all_ds_stat_iscell = load_all_ds_stat_iscell(track_ops)
    all_ds_centroids = load_all_ds_centroids(all_ds_stat_iscell, track_ops)
    all_ds_mean_img = load_all_ds_mean_img(track_ops)

    plot_roi_match_multiplane(all_ds_mean_img, all_ds_centroids, all_pl_match_mat, track_ops, win_size=track_ops.win_size) # TODO: match histogram to the first roi of first batch (not first roi of each batch)
    plot_allroi_match_multiplane(all_ds_mean_img, all_pl_match_mat, track_ops)

    print('\n\n\nDone!\n\n\n')