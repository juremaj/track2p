from track2p.ops.default import DefaultTrackOps
from types import SimpleNamespace

from track2p.io.s2p_loaders import load_all_imgs, check_nplanes, load_all_ds_stat_iscell, load_all_ds_mean_img, load_all_ds_centroids
from track2p.io.savers import save_track_ops, save_all_pl_match_mat

from track2p.register.loop import run_reg_loop, reg_all_ds_all_roi
from track2p.register.utils import get_all_ds_img_for_reg, get_all_ref_nonref_inters

from track2p.plot.progress import plot_all_planes
from track2p.plot.output import plot_reg_img_output, plot_thr_met_hist, plot_roi_reg_output, plot_roi_match_multiplane, plot_allroi_match_multiplane

from track2p.match.loop import get_all_ds_assign, get_all_pl_match_mat 
import numpy as np
import os


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

    
    #HERE 
    
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


    # 10) save in suite2p format
    if track_ops.save_in_s2p_format:
        print('Saving in suite2p format...')
        save_in_s2p_format(track_ops)
        
    # 10) plot results
    print('Generating plots (this can take some time)...')
    all_ds_stat_iscell = load_all_ds_stat_iscell(track_ops)
    all_ds_centroids = load_all_ds_centroids(all_ds_stat_iscell, track_ops)
    all_ds_mean_img = load_all_ds_mean_img(track_ops)

    plot_roi_match_multiplane(all_ds_mean_img, all_ds_centroids, all_pl_match_mat, track_ops, win_size=track_ops.win_size) # TODO: match histogram to the first roi of first batch (not first roi of each batch)
    plot_allroi_match_multiplane(all_ds_mean_img, all_pl_match_mat, track_ops)
    
    print('\n\n\nDone!\n\n\n')
    

def save_in_s2p_format(track_ops):
    


    #folderpath="/Users/manonmantez/Desktop/el"
    folderpath=track_ops.save_path
    
    t2p_match_mat = np.load(os.path.join(folderpath,"plane0_match_mat.npy"), allow_pickle=True)
    t2p_match_mat_allday = t2p_match_mat[~np.any(t2p_match_mat == None, axis=1), :]
    track_ops_dict = np.load(os.path.join(folderpath,  "track_ops.npy"), allow_pickle=True).item()
    track_ops = SimpleNamespace(**track_ops_dict)
    track_ops = track_ops
    iscell_thr = track_ops.iscell_thr

    all_f_t2p= []
    all_ops = []
    all_stat_t2p = []
    all_iscell_t2p = []
    fneu_iscell_t2p= []
    spks_iscell_t2p= []
    
    fneu_chan2_iscell_t2p = []
    f_chan2_iscell_t2p = []
    redcell_iscell_t2p = []


    for (i, ds_path) in enumerate(track_ops.all_ds_path):
                ops = np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'ops.npy'), allow_pickle=True).item()
                stat = np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'stat.npy'), allow_pickle=True)
                f = np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'F.npy'), allow_pickle=True)
                fneu= np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'Fneu.npy'), allow_pickle=True)
                spks= np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'spks.npy'), allow_pickle=True)
                #print(f.shape)
                #print(fneu.shape)
                #print(spks.shape)
                iscell = np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'iscell.npy'), allow_pickle=True)
                if track_ops.nchannels==2:
                    f_chan2=np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'F_chan2.npy'), allow_pickle=True)
                    fneu_chan2 = np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'Fneu_chan2.npy'), allow_pickle=True)
                    redcell=np.load(os.path.join(ds_path, 'suite2p', 'plane0', 'redcell.npy'), allow_pickle=True)

                if track_ops.iscell_thr==None:
                    stat_iscell = stat[iscell[:, 0] == 1]
                    f_iscell = f[iscell[:, 0] == 1, :]
                    fneu_iscell = fneu[iscell[:, 0] == 1, :]
                    spks_iscell = spks[iscell[:, 0] == 1, :]
                    is_cell = iscell[iscell[:, 0] == 1, :]
                    if track_ops.nchannels==2:
                        f_chan2_iscell = f_chan2[iscell[:, 0] == 1, :]
                        fneu_chan2_iscell = fneu_chan2[iscell[:, 0] == 1, :]
                        redcell_iscell = redcell[iscell[:, 0] == 1]
                else:
                    stat_iscell = stat[iscell[:, 1] > iscell_thr]
                    f_iscell = f[iscell[:, 1] > iscell_thr, :]
                    fneu_iscell = fneu[iscell[:, 1] > iscell_thr, :]
                    spks_iscell = spks[iscell[:, 1] > iscell_thr, :]
                    is_cell = iscell[iscell[:, 1] > iscell_thr, :]
                    if track_ops.nchannels==2:
                        f_chan2_iscell = f_chan2[iscell[:, 1] > track_ops.iscell_thr, :]
                        fneu_chan2_iscell = fneu_chan2[iscell[:, 1] > track_ops.iscell_thr, :]
                        redcell_iscell = redcell[iscell[:, 1] > track_ops.iscell_thr]
                    
                    
                
                stat_t2p = stat_iscell[t2p_match_mat_allday[:, i].astype(int)]
                f_t2p = f_iscell[t2p_match_mat_allday[:, i].astype(int), :]
                fneu_t2p = fneu_iscell[t2p_match_mat_allday[:, i].astype(int), :]
                spks_t2p = spks_iscell[t2p_match_mat_allday[:, i].astype(int), :]
                iscell_t2p = is_cell[t2p_match_mat_allday[:, i].astype(int), :]
                if track_ops.nchannels==2:
                    fneu_chan2_t2p = fneu_chan2_iscell[t2p_match_mat_allday[:, i].astype(int), :]
                    f_chan2_t2p = f_chan2_iscell[t2p_match_mat_allday[:, i].astype(int), :]
                    redcell_t2p = redcell_iscell[t2p_match_mat_allday[:, i].astype(int)]

                all_stat_t2p.append(stat_t2p)
                all_f_t2p.append(f_t2p)
                all_ops.append(ops)
                all_iscell_t2p.append(iscell_t2p)      
                fneu_iscell_t2p.append(fneu_t2p)
                spks_iscell_t2p.append(spks_t2p)  
                if track_ops.nchannels==2:
                    fneu_chan2_iscell_t2p.append(fneu_chan2_t2p)
                    f_chan2_iscell_t2p.append(f_chan2_t2p)
                    redcell_iscell_t2p.append(redcell_t2p)  
    


# Define the output folder path
    #output_folderpath = "/Users/manonmantez/Desktop/el/fake_suite2p"
    output_folderpath=os.path.join(folderpath, "fake_suite2p")
    last_elements = [os.path.basename(path) for path in track_ops.all_ds_path]
# Save each element of each list to a .npy file
    for i, (stat_t2p, f_t2p, ops, iscell_t2p, fneu_t2p, spks_t2p) in enumerate(zip(all_stat_t2p, all_f_t2p, all_ops, all_iscell_t2p, fneu_iscell_t2p, spks_iscell_t2p)):
        subfolder_path = os.path.join(output_folderpath, last_elements[i])
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
    
        np.save(os.path.join(subfolder_path, f"stat.npy"), stat_t2p)
        np.save(os.path.join(subfolder_path, f"F.npy"), f_t2p)
        np.save(os.path.join(subfolder_path, f"ops.npy"), ops)
        np.save(os.path.join(subfolder_path, f"iscell.npy"), iscell_t2p)
        np.save(os.path.join(subfolder_path, f"Fneu.npy"), fneu_t2p)
        np.save(os.path.join(subfolder_path, f"spks.npy"), spks_t2p)
        if track_ops.nchannels==2:
            for i, (redcell_t2p, f_chan2_t2p, fneu_chan2_t2p) in enumerate(zip(redcell_iscell_t2p, f_chan2_iscell_t2p, fneu_chan2_iscell_t2p)):
                np.save(os.path.join(subfolder_path, f"F_chan2.npy"), f_chan2_t2p)
                np.save(os.path.join(subfolder_path, f"Fneu_chan2.npy"), fneu_chan2_t2p)
                np.save(os.path.join(subfolder_path, f"redcell.npy"), redcell_t2p)