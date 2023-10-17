import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def l3m(anchors, rssi_values, Z0, alpha):
    # Convert RSSI values to distance using the inverse of the path-loss model
    Z = 10 * np.log10(rssi_values)
    distances = 10**((Z0 - Z) / (10 * alpha))

    # Use trilateration (or multilateration) to get position estimate
    N = anchors.shape[0]
    A = np.zeros((N, 3))
    b = np.zeros(N)

    for i in range(N):
        xi, yi, zi = anchors[i]
        Ri = distances[i] ** 2 - xi ** 2 - yi ** 2 - zi ** 2

        A[i] = [-2*xi, -2*yi, -2*zi]
        b[i] = Ri

    position = np.linalg.pinv(A).dot(b)
    return position[:3]

def l3m_c(anchors, rssi, Z0, alpha, R, K=3):
    N = anchors.shape[0]

    # Combinations of R anchors out of N
    from itertools import combinations
    combinations = list(combinations(range(N), R))
    
    # Each combination provides an estimated position
    estimated_positions = []
    for comb in combinations:
        selected_anchors = anchors[list(comb)]
        selected_rssi = rssi[list(comb)]
        estimated_pos = l3m(selected_anchors, selected_rssi, Z0, alpha)
        estimated_positions.append(estimated_pos)
    
    estimated_positions = np.array(estimated_positions)
    
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=K).fit(estimated_positions)
    cluster_centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    # Compute RSSI error for each cluster
    rssi_errors = []
    for k in range(K):
        indices = np.where(labels == k)[0]
        cluster_positions = estimated_positions[indices]
        rssi_error = np.mean(np.linalg.norm(cluster_positions - cluster_centers[k], axis=1))
        rssi_errors.append(rssi_error)
    
    best_cluster_index = np.argmin(rssi_errors)
    
    # Count occurrences of each anchor in all clusters except the best one
    anchor_counts = np.zeros(N)
    for i, comb in enumerate(combinations):
        if labels[i] != best_cluster_index:
            for anchor_index in comb:
                anchor_counts[anchor_index] += 1

    # Identify the worst anchor to be removed
    worst_anchor = np.argmax(anchor_counts)
    
    # Remove the worst anchor and re-estimate the position
    selected_anchors = np.delete(anchors, worst_anchor, axis=0)
    selected_rssi = np.delete(rssi, worst_anchor)
    estimated_pos = l3m(selected_anchors, selected_rssi, Z0, alpha)
    return estimated_pos[:3]
