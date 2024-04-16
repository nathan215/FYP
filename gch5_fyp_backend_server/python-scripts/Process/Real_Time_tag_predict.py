# This file is used to Calling the algorithm to predict the next location of the drone
import pandas as pd
import threading
import time
import json
import sys
from shared_state import fix_combined_data, find_initial_location, algorithm_use
from Algorithm.l3m_c_l3m_mre import l3m
from Algorithm.nelder_mead import my_nelder_mead as nmg
from Data_handle.Coordinate_transfer import xy2ll


# This function is used to calculate the predict location of the drone
def caculate_predict(websocket_server):
    # leave last four data points for prediction
    global combined_data
    combined_data = combined_data[:-4]
    while True:
        time.sleep(2)
        combined_data_df = pd.DataFrame(combined_data)
        if algorithm_use == "l3m":
            predict_point = l3m(combined_data_df)
        elif algorithm_use == "nelder_mead":
            predict_point = nmg(combined_data_df)
            # result, all_points = nmg.my_nelder_mead(lambda x: objective_function(x, data), x_start, step=100, max_iter=100)
        lon, lat = xy2ll(
            predict_point[0], predict_point[1], initial_location[0], initial_location[1]
        )
        predict_json = json.dumps(
            {"type": "predict_location", "data": {"lon": lon, "lat": lat}}
        )
        websocket_server.send_message(predict_json)  # Send prediction through WebSocket


# This function is used to start the predict location in a new thread
def predict_point(websocket_server):
    thread = threading.Thread(target=caculate_predict, args=(websocket_server))
    thread.start()
