import os
import numpy as np

def load_alldays_f1_values(base_path, animals, conditions):

    f1_values = {animal: [] for animal in animals}

    for animal in animals:
        for condition in conditions:
            metrics = np.load(os.path.join(base_path, animal, condition,'metrics_t2p_all_days.npy'), allow_pickle=True)
            f1_value = metrics[np.where(metrics[:, 0] == 'F1')[0][0], 1]
            f1_values[animal].append(f1_value)

    return f1_values


def load_pairwise_f1_values(base_path, animals, condition):

    f1_values = {animal: [] for animal in animals}

    for animal in animals:
        if condition == 'pw_reg':
            file_path = os.path.join(base_path, animal, 'metrics_table_pw_registration.npy')
        else:
            file_path = os.path.join(base_path, animal, condition, 'metrics_table_pairs.npy')
        metrics = np.load(file_path, allow_pickle=True)

        f1_scores = metrics[7, 1:].astype(float)
        f1_values[animal] = f1_scores

    return f1_values