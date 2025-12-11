# Troubleshooting Guide: Low Cell Counts and Tracking Failures in Track2p

This guide provides practical steps for diagnosing and resolving common issues encountered when running Track2p, especially when tracking neurons across multiple days. It covers:

- Low numbers of tracked cells  
- Potential tracking and registration failures  
- Recommended parameter adjustments  
- Handling potentially problematic sessions  

Whenever you encounter unexpected results, it is strongly recommended to inspect the **Track2p output figures** (see documentation: *Outputs & Visualisations*) and, if possible, view your raw or Suite2p-processed data side-by-side across days.

In the ideal world the solution is to track a subset of cells manually (see the paper for one way of doing this), and use that as a 'validation set' to help you choose the right parameters for tracking. Generating the ground truth dataset will also give you an insight into how many cells you would be expecting to be successfully tracked across all days in your experimental setting.

---

## 1. Low Numbers of Tracked Cells Across Days

Low cell counts across days can arise from issues in **cell detection** (relating to **cell activity**, **FOV consistency** etc.), or **tracking quality**. Track2p only reports cells that can be matched across *all* selected days, so variability in detection or registration can significantly reduce the final cell set.

### 1.1 Issues with cell detection ('segmentation')

#### Important points
- **Suite2p** only detects ROIs that are "active" on that session and considered as “good” (based on the outputs of a classifier)
- **Track2p** only includes cells that appear on *every* selected day.  
  If a cell is missing on any day (due to low activity or detection thresholds), it will not be included in the tracked set.

#### Common causes
1. **Different active cells across days**  
   Some neurons may be active only on some days, making them undetectable in others.

2. **Conservative Suite2p parameters**  
   High thresholds can reduce the number of detected ROIs, especially those with low activity or considered below the threshold of the classifier.

3. **Changes or drift in the recording**  
   These can cause ROI detection inconsistencies:
   - z-shift  
   - moving blood vessels  
   - debris or accumulated tissue along FOV edges  
   - subtle optical changes across sessions  

### 1.2 Recommended Solutions

#### 1. Inspect Track2p output figures
See the *Outputs & Visualisations* documentation.  
These plots help identify whether failures are due to cell detection or during registration, matching, or thresholding.

#### 2. Inspect Suite2p outputs across days
Open two or more Suite2p GUIs side-by-side and check:
- Are the same ROIs detected across days?  
- Do obvious cells appear on one day but not another?

(Optional but ideal): manually track a small set of neurons to generate “ground truth” and verify Track2p performance.

#### 3. Adjust Suite2p parameters to detect more cells
If detection seems too strict, reduce conservativeness by tuning Suite2p parameters (see Suite2p documentation).
This should increases cell count but also probably at the expense of increasing the number of false positives.  
False ROIs can be removed manually before or after Track2p processing (using either the Suite2p or Track2p curation capabilities).

#### 4. Include more borderline ROIs in Track2p
Lowering the Track2p parameter `iscell_thr` allows inclusion of ROIs rejected by the Suite2p classifier.

- Suite2p default: **0.5**  
- Recommended more permissive option: **0.25**

This would have a similar effect as above, so also make sure to remove any additional false positives that might occur as a result of this.

---

## 2. Issues with cell tracking ('linking')

Track2p’s tracking pipeline involves three stages:

1. **Registration** of consecutive FOVs  
2. **Matching** ROIs based on spatial overlap  
3. **Automatic thresholding** of IoU values to filter reliable matches

A problem in any stage can reduce the number of tracked cells.

### 2.1 Common Causes of Tracking Failure

#### 1. Registration failure
Check `reg_img_output.png`.  
The bottom row overlays red/green images across sessions. They should align well.  
If they do not, all subsequent steps will fail!

#### 2. Poor matching quality
If registration is poor or ROIs do not overlap sufficiently, spatial matching breaks down.
Matching can also have issues even if the registration is successful, but this would only expected to be the case for samples with extremely dense somata and thick optical sectioning (leading to 'overlapping' ROIs).

#### 3. Thresholding failure
If registration/matching fail, the IoU histogram (`thr_met_hist.png`) may:
- be unimodal, for example looking like it is decaying 'exponentially' from 0  
- lack a visible separation between matched/unmatched populations (the two usual modes)

This causes automatic thresholds to be placed arbitrarily, leading to most matches being discarded or accepted, without any statistical justification.

### 2.2 Recommended Solutions

#### 1. Examine diagnostic figures
- **Registration** → `reg_img_output.png`  
- **Matching & thresholding** → `thr_met_hist.png`  

These files usually reveal the underlying issue.

Registration: check the last row of `reg_img_output.png` should show good overlap between red and green images, if not it means the registration did not work properly. It could also be the case that it only works in a part of the field of view and not homogenously! If you see the algorithm has failed make sure to check the FOV images and see if they resemble each other (e. g. could they be aligned manually).

Matching & thresholding: check that `thr_met_hist.png` shows a bimodal histogram for all pairs of consecutive sessions. Also check that the statistical threshold that is marked as a vertical line 'makes sense' statistically (e. g. it should separate the two assumed distributions corresponding to the two modes).

#### 2. Try alternate registration methods
Track2p supports:
- `'affine'` (default)  
- `'rigid'`  

Rigid has fewer degrees of freedom so it is easier to find a good alignment in theory. However it can not account for expansion or shearing across sessions, so in the case of early development `'affine'` would be prefered (based on results from the eLife paper, might depend on the particular preparation). We have not tested this in adults, but it might be that `'rigid'` would work better - we encourage users to try both :)

#### 3. Switch thresholding method
If your IoU histograms are bimodal, but you think that the threshold does not appropriately separate the two distributions, you can try a different threshold, currently the options are:
- `'otsu'`
- `'min'`  

Depending on histogram shape, one or the other may be more appropriate.

#### 4. Remove problematic recording days
If a single session is very different (e.g., z-shift, optical debris, abnormal brightness), it may disrupt registration between the surrounding sessions.  
Removing the problematic day often restores normal tracking across the remaining days, but it of course leads to missing values, which might be an issue in downsream analysis.

#### 5. Consider shorter intervals
For some scientific questions it might be sufficient to only track across two (or a few) neighbouring days. If this is the case, the user can also perform shorter tracks that are expected to yield more accurately tracked neurons.

---

## 4. Summary of Recommended Workflow for Troubleshooting

1. **Inspect Track2p output figures** to locate the stage causing failure.  
2. **Check Suite2p results side-by-side** across days for ROI consistency.  
3. **Adjust Suite2p thresholds** or Track2p’s `iscell_thr` to increase detected ROI overlap across days.  
4. **Try different registration methods** and thresholding strategies.  
5. **Identify and remove problematic sessions** (e.g., z-shift or debris).  
6. **Prefer shorter, overlapping blocks** if long-span tracking is inconsistent and if it does not interfere with your scientific goals :)

This  approach usually resolves the most common problems involving low tracked cell counts and tracking failures.
