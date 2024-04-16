import os
os.environ['OMP_NUM_THREADS'] = '1'
from itertools import combinations as itertools_combinations
from scipy.interpolate import griddata
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from itertools import combinations
from scipy.spatial.distance import euclidean
from scipy.stats import linregress

def compute_parameters_linear(fix_combined_data):
    # Extract coordinates and RSSI values from data
    x_coords = [entry['x'] for entry in fix_combined_data]
    y_coords = [entry['y'] for entry in fix_combined_data]
    rssi_values = [entry['rssi'] for entry in fix_combined_data]

    distances = np.sqrt(np.array(x_coords)**2 + np.array(y_coords)**2)
    distances = np.where(distances == 0, 1e-4, distances)

    log_distances = np.log10(distances)

    # Perform linear regression on log-distances versus RSSI values
    slope, intercept, r_value, p_value, stderr = linregress(log_distances, rssi_values)

    n = -slope / 10
    C = intercept
    return n, C, stderr   

def l3m(df, Z0, alpha):
    rssi_values = df['rssi'].values
    anchors = df[['x', 'y']].values
    
    # Compute distances vectorized
    distances = 10 ** ((Z0 - rssi_values) / (10 * alpha))

    # Compute squared distances
    squared_distances = distances ** 2
    
    squared_x = anchors[:, 0] ** 2
    squared_y = anchors[:, 1] ** 2
    
    Ri = squared_distances - squared_x - squared_y
    A = -2 * anchors
    
    position = np.linalg.lstsq(A, Ri, rcond=None)[0] 
    return position[:2]

def l3m_c(df, Z0, alpha, R=4, K=3):
    N = df.shape[0]
    if R > N:
        R = N

    anchor_combinations = list(itertools_combinations(range(N), R))
    estimated_positions = np.array([l3m(df.iloc[list(comb)], Z0, alpha) for comb in anchor_combinations])
    
    # Clustering
    if len(estimated_positions) >= K:
        kmeans = KMeans(n_clusters=K, n_init=10)  
        kmeans.fit(estimated_positions)
        cluster_centers = kmeans.cluster_centers_
        labels = kmeans.labels_
        
        rssi_errors = [np.mean(np.linalg.norm(estimated_positions[labels == k] - cluster_centers[k], axis=1)) for k in range(K)]
        best_cluster_index = np.argmin(rssi_errors)
        
        # Identify worst anchor and adjust dataset
        anchor_counts = np.sum(labels[:, None] == best_cluster_index, axis=0)
        worst_anchor = np.argmax(anchor_counts)
        df = df.drop(df.index[worst_anchor])
        
        estimated_pos = l3m(df, Z0, alpha)
    else:
        estimated_pos = np.mean(estimated_positions, axis=0)
    
    return estimated_pos[:2]

def l3m_mre(df, Z0, alpha, R=4):
    N = df.shape[0]
    if R > N:
        return l3m(df, Z0, alpha)

    anchor_combinations = list(combinations(range(N), R))
    node_errors = np.zeros(N)  # Array to hold total errors for each node
    node_counts = np.zeros(N)  # Array to count occurrences of each node in combinations

    estimated_positions = np.zeros((len(anchor_combinations), 2))
    estimated_errors = np.zeros(len(anchor_combinations))

    for idx, comb in enumerate(anchor_combinations):
        selected_df = df.iloc[list(comb)]
        estimated_pos = l3m(selected_df, Z0, alpha)
        estimated_positions[idx] = estimated_pos

        distances = np.linalg.norm(selected_df[['x', 'y']].values - estimated_pos, axis=1)
        estimated_rssi = Z0 - 10 * alpha * np.log10(distances)
        errors = np.abs(selected_df['rssi'].values - estimated_rssi)

        # Update the total errors and counts for each node in this combination
        for i, node_idx in enumerate(comb):
            node_errors[node_idx] += errors[i]
            node_counts[node_idx] += 1

        Z_m = np.mean(errors)
        estimated_errors[idx] = Z_m

    best_index = np.argmin(estimated_errors)
    best_estimated_location = estimated_positions[best_index]

    # Calculate average error for each node and identify the node with the highest error
    average_node_errors = node_errors / node_counts
    node_to_exclude = np.argmax(average_node_errors)

    return best_estimated_location, node_to_exclude

def mian():
    import time
    from numpy.linalg import norm
    # compare running time and accuacy for l3m, l3m_optimized
    df = pd.read_csv('D:\\FYP\\FYP\\gch5_fyp_backend_server\\simulated_rssi_dataset.csv')
    # Constants
    Z0 = -40
    alpha = 2

    # Experiment configuration
    sample_sizes = range(3, 16)  # From 3 to 15 points

    # Record results
    results = []
    

    for size in sample_sizes:
        error_original = 0
        error_optimized = 0
        duration_optimized = 0
        duration_original = 0
        print(size)
        for i in range(10):
            subset = df.sample(n=size)
            start_time = time.time()

            pos_original = l3m_c(subset, Z0, alpha)
            error_original += norm(pos_original)
            duration_original += time.time() - start_time
        

            start_time = time.time()
            pos_optimized = l3m(subset, Z0, alpha)
            error_optimized += norm(pos_optimized)
            duration_optimized += time.time() - start_time
        

        # Record data
        results.append({
            'sample_size': size,
            'time_original': duration_original,
            'error_original': error_original,
            'time_optimized': duration_optimized,
            'error_optimized': error_optimized
        })

    # Convert results to DataFrame for easier analysis
    results_df = pd.DataFrame(results)
    print(results_df)
    # Save results to CSV file
    results_df.to_csv('l3m_optimization_comparison.csv', index=False)

if __name__ == '__main__':
    mian()  
