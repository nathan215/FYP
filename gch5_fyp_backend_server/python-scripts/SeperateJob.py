# This is the main file to call the functions in the other files
from Data_handle.DataGenerate import start_generating_data
from Data_handle.RealTimeDataCombine import start_combining_data
from Data_handle.Simul_get_rssi import background_drone_add_rssi
from Process.Real_Time_tag_predict import predict_point
from Process.Algorithm_run import run_algorithm
from shared_state import drone_data, station_data, combined_data, initial_location

def testing():
    # Start data generation and processing
    start_generating_data()
    start_combining_data()
    # Your coordination logic here

def main():
    background_drone_add_rssi()
    predict_point()
    run_algorithm()

    
if __name__ == "__main__":
    main()
