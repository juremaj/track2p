import numpy as np

from skimage.exposure import match_histograms


def match_hist_all(all_ds_avg_ch):
    ref = all_ds_avg_ch[0][0]
    all_ds_avg_ch_matched = []
    for ds_avg_ch in all_ds_avg_ch:
        ds_avg_ch_matched = []
        for i in range(len(ds_avg_ch)):
            ds_avg_ch_matched.append(match_histograms(ds_avg_ch[i], ref))
        all_ds_avg_ch_matched.append(ds_avg_ch_matched)
        
    return all_ds_avg_ch_matched

def make_rgb_img(img1, img2):
    img_rgb = np.zeros((img1.shape[0], img1.shape[1], 3))
    # normalise images to 0-1
    img1_norm = (img1 - np.min(img1)) / (np.max(img1) - np.min(img1))
    img2_norm = (img2 - np.min(img2)) / (np.max(img2) - np.min(img2))
    img_rgb[:, :, 0] = img1_norm
    img_rgb[:, :, 1] = img2_norm
    
    return img_rgb

def saturate_perc(img_rgb, sat_perc=99):
    img_rgb = np.clip(img_rgb, 0, np.percentile(img_rgb, sat_perc)) 
    img_rgb = (img_rgb / np.max(img_rgb) * 255).astype(np.uint8)
    return img_rgb