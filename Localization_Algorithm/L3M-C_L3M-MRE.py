import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime
import itertools

def calculate_distance(x, xi, y, yi, z, zi):
    return np.sqrt((x - xi)**2 + (y - yi)**2 + (z - zi)**2)

class Localization:
    def __init__(self, test_id, stimulate, start_time):
        self.test_id = test_id
        self.stimulate = stimulate
        self.start_time = start_time
        self.rssi_records = []
    
    def l3m_3d_localization(self, anchors, Z, Z0, alpha):
        N = anchors.shape[0]
        A = np.zeros((N, 4))
        b = np.zeros(N)

        for i in range(N):
            xi, yi, zi = anchors[i]
            Ri = xi**2 + yi**2 + zi**2

            A[i] = [-2*xi, -2*yi, -2*zi, 1]
            b[i] = 10/(2*alpha) * (Z0 - Z[i]) - Ri

        # Solve the system of linear equations
        AtA_inv_At = np.linalg.pinv(A)  # Moore-Penrose pseudo-inverse
        theta_hat = 0.5 * np.dot(AtA_inv_At, b)

        # Extract and return the estimated [x, y, z] coordinates
        return theta_hat[:3]



class L3MCLocalization(Localization):
    def __init__(self, anchors, Z, Z0, alpha, R, K):
        self.anchors = anchors
        self.Z = Z
        self.Z0 = Z0
        self.alpha = alpha
        self.R = R
        self.K = K
    
    def l3m_3d_localization(self, anchors, Z):
        N = anchors.shape[0]
        A = np.zeros((N, 4))
        b = np.zeros(N)
        for i in range(N):
            xi, yi, zi = anchors[i]
            Ri = xi**2 + yi**2 + zi**2
            A[i] = [-2*xi, -2*yi, -2*zi, 1]
            b[i] = 10/(2*self.alpha) * (self.Z0 - Z[i]) - Ri
        AtA_inv_At = np.linalg.pinv(A)
        theta_hat = 0.5 * np.dot(AtA_inv_At, b)
        return theta_hat[:3]

    def estimate_preliminary_locations(self):
        estimated_locations = []
        N = self.anchors.shape[0]
        for subset_anchors in self.select_subsets_of_anchors(N, self.R):
            subset_Z = self.Z[subset_anchors]
            est_loc = self.l3m_3d_localization(self.anchors[subset_anchors], subset_Z)
            estimated_locations.append(est_loc)
        return np.array(estimated_locations)

    def select_subsets_of_anchors(self, N, R):

        return list(itertools.combinations(range(N), R))
    
    def find_optimal_cluster_and_unreliable_node(self, estimated_locations):
        kmeans = KMeans(n_clusters=self.K).fit(estimated_locations)
        labels = kmeans.labels_
        cluster_centers = kmeans.cluster_centers_
        best_cluster_index = -1
        best_cluster_metric = float('inf')
    
        # Evaluating clusters
        for k in range(self.K):
            current_cluster_points = estimated_locations[labels == k]
            Z_hat_k = self.calculate_Z_hat(current_cluster_points)  # Define this function based on your method
            z_k_metric = self.calculate_cluster_metric(current_cluster_points, Z_hat_k, k)  # Define this function
            
            if z_k_metric < best_cluster_metric:
                best_cluster_metric = z_k_metric
                best_cluster_index = k
        
        # Identifying unreliable nodes
        unreliable_node_index = self.identify_unreliable_node(best_cluster_index, labels, cluster_centers)
        
        return cluster_centers[best_cluster_index], unreliable_node_index

import json
with open('dataset_1.json', 'r') as file:
    data = json.load(file)
# random choose 50 points which x,y,z<200
data_choose = []
import random
# random data['rssi_records']
random.shuffle(data['rssi_records'])

for i in range(len(data['rssi_records'])):
    if data['rssi_records'][i]['x'] < 200 and data['rssi_records'][i]['y'] < 200 and data['rssi_records'][i]['z'] < 200:
        data_choose.append(data['rssi_records'][i])
    if len(data_choose) == 50:
        break

localizer = Localization(test_id=1, stimulate=True, start_time=0)

# Extracting anchor locations and RSSI values
anchors = np.array([[int(r['x']), int(r['y']), int(r['z'])] for r in data_choose])
Z = np.array([r['rssi'] for r in data_choose])

# Example parameters
Z0 = -50  # Sample value, please adjust according to your case.
alpha = 2.0  # Sample value, please adjust according to your case.

# Getting estimated location
estimated_location = localizer.l3m_3d_localization(anchors, Z, Z0, alpha)
print(f"Estimated location: {estimated_location}")