
def get_all_ds_img_for_reg(all_ds_avg_ch1, all_ds_avg_ch2, track_ops): # chooses which channel to use for registration and returns all_ref_img and all_mov_img (shifted by one day to always register to previous day)
    if track_ops.reg_chan==0:
        all_ds_avg = all_ds_avg_ch1
    elif track_ops.reg_chan==1:
        all_ds_avg = all_ds_avg_ch2

    all_ds_ref_img = []
    all_ds_mov_img = []

    for i in range(len(track_ops.all_ds_path)-1):
        ds_ref_img = []
        ds_mov_img = []
        
        for j in range(track_ops.nplanes):
            ds_ref_img.append(all_ds_avg[i][j])
            ds_mov_img.append(all_ds_avg[i+1][j])

        all_ds_ref_img.append(ds_ref_img)
        all_ds_mov_img.append(ds_mov_img)

    track_ops.all_ds_ref_img = all_ds_ref_img
    track_ops.all_ds_mov_img = all_ds_mov_img

    return all_ds_ref_img, all_ds_mov_img