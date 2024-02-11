from sklearn.cluster import KMeans
from numpy.linalg import svd
import numpy as np
import pandas as pd

def rssi_to_distance(rssi, Z0, alpha):
    return 10 ** ((Z0 - rssi) / (10 * alpha))

def cluster_svd(df, Z0, alpha, n_clusters):
    # Convert RSSI to distance
    df['distance'] = df['rssi'].apply(lambda rssi: rssi_to_distance(rssi, Z0, alpha))

    # Cluster the data
    kmeans = KMeans(n_clusters=n_clusters, n_init=10)
    df['cluster'] = kmeans.fit_predict(df[['distance']])

    # Solve positioning for each cluster using SVD
    positions = []
    for cluster in range(n_clusters):
        cluster_data = df[df['cluster'] == cluster][['x', 'y', 'z']]
        u, s, vh = svd(cluster_data, full_matrices=False)
        position = np.mean(cluster_data, axis=0)  # Calculate centroid
        positions.append(position)

    return positions

def read_data_from_csv(limit=50, x_range=None, y_range=None, z_value=5):
    # Read the CSV file into a DataFrame
    df = pd.read_csv("D:\FYP\PHD_Task\DroneSAR\data\esu\compiled_data.csv")

    # Apply the same filtering as your SQL WHERE conditions
    if x_range:
        df = df[(df['x'] >= x_range[0]) & (df['x'] <= x_range[1])]
    if y_range:
        df = df[(df['y'] >= y_range[0]) & (df['y'] <= y_range[1])]
    # Assuming z is a fixed value in this case and not a range
    df['z'] = z_value
    df['rssi'] = df['rssi'].astype(float)
    # Randomly sample 'limit' number of rows from the filtered DataFrame
    df = df.sample(n=limit).reset_index(drop=True)
    return df

def main():
    df = read_data_from_csv(limit=20, z_value=5)
    C = -60
    n = 1.7
    positions = cluster_svd(df, C, n, 5)
    print(positions)

if __name__ == '__main__':
    main()