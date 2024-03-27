# This is the main file to call the functions in the other files
import threading
from Data_handle.MQTT_Station import setup_station_mqtt
from Data_handle.DataGenerate import start_generating_data
from Data_handle.RealTimeDataCombine import start_combining_data
from Data_handle.Simul_get_rssi import background_drone_add_rssi
from Process.Real_Time_tag_predict import predict_point
from Process.Algorithm_run import run_algorithm
from Process.trace_setting import trace_setting
from shared_state import drone_data, station_data, combined_data, initial_location, device_id

def testing():
    # Start data generation and processing
    start_generating_data()
    start_combining_data()
    # Your coordination logic here

def main():
    # Start the MQTT thread
    station_thread = threading.Thread(target=setup_station_mqtt)
    station_thread.start()
    
    drone_thread = threading.Thread(target=setup_drone_mqtt)
    drone_thread.start()

    while True:
        # ask for user input to do data collection or testing
        user_input = input("Do you want to do data collection or testing? (data/testing): ")
        if user_input == "data":
            if not device_id or not drone_data:
                print("No device data received yet, please wait for a moment.")
                continue
            combine_thread = threading.Thread(target=start_combining_data)

        elif user_input == "testing":
            trace_setting()
            combine_thread = threading.Thread(target=start_combining_data)
            combine_thread.start()                            
            predict_point()
            run_algorithm()
        else:
            print("Invalid input, please try again.")
            continue

    
if __name__ == "__main__":
    main()
