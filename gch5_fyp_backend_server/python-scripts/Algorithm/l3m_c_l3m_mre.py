import os
os.environ['OMP_NUM_THREADS'] = '1'
from itertools import combinations as itertools_combinations
from scipy.interpolate import griddata
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from itertools import combinations
from scipy.spatial.distance import euclidean

def l3m(df, Z0, alpha):
    rssi_values = df['rssi'].values
    anchors = df[['x', 'y']].values
    distances = 10**((Z0 - rssi_values) / (10 * alpha))

    N = anchors.shape[0]
    A = np.zeros((N, 2))
    b = np.zeros(N)

    for i in range(N):
        xi, yi = anchors[i]
        Ri = distances[i]**2 - xi**2 - yi**2
        A[i] = [-2*xi, -2*yi]
        b[i] = Ri

    position = np.linalg.pinv(A).dot(b)
    return position[:2]

def l3m_c(df, Z0, alpha, R, K=3):
    N = df.shape[0]
    # Use a different name to avoid conflict with the 'combinations' from itertools
    anchor_combinations = list(itertools_combinations(range(N), R))

    estimated_positions = []
    for comb in anchor_combinations:
        selected_anchors = df.iloc[list(comb)]
        estimated_pos = l3m(selected_anchors, Z0, alpha)
        estimated_positions.append(estimated_pos)

    estimated_positions = np.array(estimated_positions)

    # Ensure there are enough samples for clustering
    if len(estimated_positions) >= K:
        kmeans = KMeans(n_clusters=K, n_init=10).fit(estimated_positions)
        cluster_centers = kmeans.cluster_centers_
        labels = kmeans.labels_

        rssi_errors = []
        for k in range(K):
            indices = np.where(labels == k)[0]
            cluster_positions = estimated_positions[indices]
            rssi_error = np.mean(np.linalg.norm(cluster_positions - cluster_centers[k], axis=1))
            rssi_errors.append(rssi_error)

        best_cluster_index = np.argmin(rssi_errors)
        anchor_counts = np.zeros(N)
        for i, comb in enumerate(anchor_combinations):
            if labels[i] != best_cluster_index:
                for anchor_index in comb:
                    anchor_counts[anchor_index] += 1

        worst_anchor = np.argmax(anchor_counts)
        df = df.drop(df.index[worst_anchor])
        estimated_pos = l3m(df, Z0, alpha)
    else:
        print("Not enough samples for clustering. Adjusting strategy...")
        estimated_pos = np.mean(estimated_positions, axis=0)  # Example fallback

    return estimated_pos[:2]

def l3m_mre(df, Z0,alpha, R):
    
    N = df.shape[0]
    # Get all combinations of R out of N anchor nodes
    anchor_combinations = list(combinations(range(N), R))
    
    estimated_locations = []
    estimated_errors = []

    for comb in anchor_combinations:
        selected_df = df.iloc[list(comb)]
        estimated_pos = l3m(selected_df, Z0, alpha)
        estimated_locations.append(estimated_pos)

        errors = []
        for i, row in selected_df.iterrows():
            anchor = row[['x', 'y', 'z']].values
            d = euclidean(anchor, estimated_pos)  # Using all x, y, and z values for distance
            estimated_rssi = Z0 - 10 * alpha * np.log10(d)  # Including the path loss exponent 'alpha'
            error = row['rssi'] - estimated_rssi
            errors.append(error)

        Z_m = np.mean(np.abs(errors))
        estimated_errors.append(Z_m)

    # Find the position with the minimum RSSI error
    best_index = np.argmin(estimated_errors)
    best_estimated_location = estimated_locations[best_index]

    return best_estimated_location
