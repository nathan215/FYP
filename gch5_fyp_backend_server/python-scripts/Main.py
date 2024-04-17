# This is the main file to call the functions in the other files
import threading
from Data_transmission.MQTT_Station import setup_station_mqtt
from Data_transmission.MQTT_Drone import (
    setup_drone_mqtt,
)  # TODO: Implement this function
from Data_transmission.websocket_server import WebSocketServer
from Data_handle.DataGenerate import start_generating_data
from Data_handle.RealTimeDataCombine import start_combining_data
from Data_handle.Simul_get_rssi import background_drone_add_rssi
from Process.Algorithm_run import run_algorithm
from Process.trace_setting import trace_setting
from shared_state import (
    drone_data,
    current_drone_location,
    simulation_start_x_y,
    station_data,
    find_combined_data,
    fix_combined_data,
    device_id,
    algorithm_use,
    find_device_id,
)
import time

# setting
mqtt_station = True
mqtt_drone = False


def testing():
    print("Testing")
    websocket_server = WebSocketServer()
    ws_thread = threading.Thread(target=websocket_server.start_server)
    ws_thread.start()
    print("WebSocket server started")

    start_generating_data()
    thread = threading.Thread(target=start_combining_data(websocket_server))
    thread.start()


def main():
    # Initialize WebSocket server
    websocket_server = WebSocketServer()

    # Start WebSocket server in a separate thread
    ws_thread = threading.Thread(target=websocket_server.start_server)
    ws_thread.start()
    # change line and print statement
    print("")
    print("WebSocket server started")
    
    if mqtt_station:
        station_thread = threading.Thread(target=setup_station_mqtt)
        station_thread.start()
    if mqtt_drone:
        drone_thread = threading.Thread(target=setup_drone_mqtt)
        drone_thread.start()

    while True:
        # ask for user input to do data collection or testing
        user_input = input(
            "Do you want to do data collection, testing, or simulation test? (data/testing/simulation): "
        )

        # Start data collection
        if user_input == "data":
            if not device_id or not drone_data:
                print("No device data received yet, please wait for a moment.")
                continue
            combine_thread = threading.Thread(target=start_combining_data)
        # Start testing
        elif user_input == "simulation":
            print("Enter the starting point for the drone(x,y):")
            x = float(input("x: "))
            y = float(input("y: "))
            current_drone_location[0] = x
            current_drone_location[1] = y
            simulation_start_x_y = [x, y]
            background_drone_add_rssi_thread = threading.Thread(
                target=background_drone_add_rssi, args=(websocket_server,)
            )
            background_drone_add_rssi_thread.start()
            trace_setting()
            time.sleep(3)
            run_algorithm(websocket_server)
        elif user_input == "testing":
            background_drone_add_rssi_thread = threading.Thread(
                target=background_drone_add_rssi, args=(websocket_server,)
            )
            background_drone_add_rssi_thread.start()
            run_algorithm(websocket_server)

        else:
            print("Invalid input, please try again.")
            continue


if __name__ == "__main__":
    main()
    while True:
        pass
