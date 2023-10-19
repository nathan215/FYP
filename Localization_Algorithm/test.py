import psycopg2
import random

import numpy as np
import pandas as pd
from l3m_c_l3m_mre import l3m, l3m_c, l3m_mre
def l3m_w(df, Z0, alpha, estimated_locations):
    
    N = df.shape[0]  
    def compute_rssi_error(a, b,c):
        errors = []     
        for i, row in df.iterrows():
            xi, yi, zi = row['x'], row['y'], row['z']
            d = np.sqrt((xi - a)**2 + (yi - b)**2+(zi - c)**2)  # Euclidean distance
            estimated_rssi = Z0 - 10 * alpha * np.log10(d)
            error = row['rssi'] - estimated_rssi
            errors.append(error)
            
        Z_hat = np.mean(np.abs(errors))
        return Z_hat

    errors = [compute_rssi_error(a, b,c) for a, b,c in estimated_locations]
    min_error_index = np.argmin(errors)  
    return estimated_locations[min_error_index]

def get_random_data(limit=50, x_range=None, y_range=None, z_range=None, distance_range=None):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database="FYP", user="postgres", password="0000", host="localhost", port="5433")
    cur = conn.cursor()
    
    query = "SELECT x, y, z, rssi FROM test_records WHERE 1=1 AND record_id=2"
    if x_range:
        query += f" AND x BETWEEN {x_range[0]} AND {x_range[1]}"
    if y_range:
        query += f" AND y BETWEEN {y_range[0]} AND {y_range[1]}"
    if z_range:
        query += f" AND z BETWEEN {z_range[0]} AND {z_range[1]}"
    if distance_range:
        query += f" AND distance BETWEEN {distance_range[0]} AND {distance_range[1]}"
    query += f" ORDER BY RANDOM() LIMIT {limit}"
    
    # Execute the query
    cur.execute(query)
    data = cur.fetchall()
    
    # Close the connection
    cur.close()
    conn.close()
    
    return np.array(data)

def main():
    # Get random data
    data = get_random_data(limit=10, x_range=(10,200), y_range=(10,200), z_range=(0,50))
    
    
    # Convert to DataFrame for compatibility with l3m and l3m_c
    df = pd.DataFrame(data, columns=['x', 'y', 'z', 'rssi'])
    # Predict locations using l3m and l3m_c
    print("predicting location using l3m...")
    location_l3m = l3m(df,-40 ,2)
    print("Predicted Location using L3M:", location_l3m)
    print("predicting location using l3m_c...")
    location_l3m_c = l3m_c(df ,-40,2,5,3)
    print("Predicted Location using L3M-C:", location_l3m_c)
    print("predicting location using l3m_mre...")
    location_l3m_mre = l3m_mre(df,-40 ,2,5)
    print("Predicted Location using L3M-MRE:", location_l3m_mre)
    print("predicting location using l3m_w...")
    location_l3m_w = l3m_w(df,-40 ,2,[location_l3m,location_l3m_c,location_l3m_mre])
    print("Predicted Location using L3M-W:", location_l3m_w)
    return location_l3m, location_l3m_c, location_l3m_mre, location_l3m_w
if __name__ == '__main__':
    predict = []
    for i in range(10):
        print(f"Test {i+1}")
        k = main()
        predict.append(k)

    # the actual location is ( 0,0,0), so we calculate the error
    error_l3m = []
    error_l3m_c = []
    error_l3m_mre = []
    error_l3m_w = []
    for i in range(10):
        error_l3m.append(np.sqrt((predict[i][0][0])**2+(predict[i][0][1])**2+(predict[i][0][2])**2))
        error_l3m_c.append(np.sqrt((predict[i][1][0])**2+(predict[i][1][1])**2+(predict[i][1][2])**2))
        error_l3m_mre.append(np.sqrt((predict[i][2][0])**2+(predict[i][2][1])**2+(predict[i][2][2])**2))
        error_l3m_w.append(np.sqrt((predict[i][3][0])**2+(predict[i][3][1])**2+(predict[i][3][2])**2))
    print("Error of L3M:",error_l3m, "Average Error of L3M:",np.mean(error_l3m))
    print("Error of L3M-C:",error_l3m_c, "Average Error of L3M-C:",np.mean(error_l3m_c))
    print("Error of L3M-MRE:",error_l3m_mre, "Average Error of L3M-MRE:",np.mean(error_l3m_mre))
    print("Error of L3M-W:",error_l3m_w, "Average Error of L3M-W:",np.mean(error_l3m_w))

