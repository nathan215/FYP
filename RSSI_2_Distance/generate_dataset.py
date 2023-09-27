import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

def sql_store(df):
    # MySQL connection information
    username = 'root'
    password = '0000'
    host = 'localhost'  # or the IP address of your MySQL server
    database_name = 'Virtual_Test'

    # Create the SQLAlchemy engine
    engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{database_name}')

    # Save the dataframe to the MySQL database
    df.to_sql('rssi_data', con=engine, index=False, if_exists='replace')

def generate_rssi(horizen_distance, z, n, C):
    mean_noise = 10 + 0.001 * horizen_distance - z * 0.01
    noise = np.random.normal(mean_noise, 5)  # mean and standard deviation
    rssi = C - 10 * n * np.log10(np.sqrt(horizen_distance**2 + z**2)) + noise
    return rssi

def generate_dataset():
    data = []
    n = 2.0
    C = -40
    
    for x in list(range(1, 10, 1)) + list (range(11, 101, 10)) + list(range(150, 1001, 50)):
        for y in list(range(1, 10, 1)) + list(range(11, 101, 10)) + list(range(150, 1001, 50)):
            for z in range(2, 101, 2):
                horizen_distance = np.sqrt(x**2 + y**2)
                distance = np.sqrt(x**2 + y**2 + z**2)
                rssi = generate_rssi(horizen_distance, z, n, C)
                timestamp = datetime.now()
                data.append((rssi, x, y, z, timestamp, distance, horizen_distance, 1))
                
    return pd.DataFrame(data, columns=['RSSI', 'X', 'Y', 'Z', 'Timestamp', 'Distance', 'Horizen_Distance', 'Virtual_Test'])

df = generate_dataset()
print(df)
sql_store(df)
 
# import matplotlib.pyplot as plt

# plt.figure(figsize=(10, 5))

# # Scatter Plot of Original Data
# plt.scatter(df["Distance"], df["RSSI"], c='red', label='Original Data')

# # Linear Regression on Log-scaled Distances
# log_distances = np.log10(df["Distance"])
# slope, intercept = np.polyfit(log_distances, df["RSSI"], 1)

# # Generate Fitted Line
# fitted_line_x = np.array([1, 10, 100, 1000])
# fitted_line_y = intercept + slope * np.log10(fitted_line_x)
# plt.plot(fitted_line_x, fitted_line_y, 'b-', label='Fitted Line')

# # Configure Plot
# plt.xscale('log')
# plt.xticks(ticks=[1, 10, 100, 1000], labels=[1, 10, 100, 1000])  # Manually set the ticks on x-axis
# plt.xlabel('Distance (m) [Log Scale]')
# plt.ylabel('RSSI (dBm)')
# plt.legend()
# plt.grid(True)
# plt.show()

