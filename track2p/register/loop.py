# for now the only algorithm is elastix, TODO: add other algorithms and run them in the same way within this loop

from track2p.register.elastix import reg_img_elastix

def run_reg_loop(all_ds_ref_img, all_ds_mov_img, track_ops):
    all_ds_mov_img_reg = []
    all_ds_reg_params = []

    for (i, ds_ref_img) in enumerate(all_ds_ref_img):
        ds_mov_img = all_ds_mov_img[i]
        ds_mov_img_reg = []
        ds_reg_params = []

        for j in range(track_ops.nplanes):
            ref_img = ds_ref_img[j]
            mov_img = ds_mov_img[j]
            mov_img_reg,reg_params = reg_img_elastix(ref_img, mov_img, track_ops)
            ds_mov_img_reg.append(mov_img_reg)
            ds_reg_params.append(reg_params)

        all_ds_mov_img_reg.append(ds_mov_img_reg)
        all_ds_reg_params.append(ds_reg_params)
        
    track_ops.all_ds_mov_img_reg = all_ds_mov_img_reg
    # track_ops.all_ds_reg_params = all_ds_reg_params # for now not saving elastix transform object (TODO: transforme it to serializable to be able to pickle (for example by saving params to a dictionary))
    
    return all_ds_mov_img_reg, all_ds_reg_params