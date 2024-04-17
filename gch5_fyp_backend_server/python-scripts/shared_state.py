# THIS FILE IS USED TO STORE SHARED STATE VARIABLES
drone_data = []
station_data = []
device_id = []
find_combined_data = []
fix_combined_data = []
find_device_id = []
fix_device_id = []
find_initial_location = [114.268, 22.337]  # (lon,lat) coordinates
fix_initial_location = [114.268, 22.337]  # (lon,lat) coordinates
simulation_start_x_y = [100,100]
current_drone_location = [100,100]
algorithm_list = ['nelder_mead','nelder_mead_global','l3m']
algorithm_use = []
data_path = 'simulated_rssi_dataset.csv'
Z0 = -64
alpha = 1.5
