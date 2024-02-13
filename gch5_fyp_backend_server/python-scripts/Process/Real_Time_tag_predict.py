import pandas as pd
import threading
import time
import json
import sys
from shared_state import combined_data, initial_location  
from Algorithm.l3m_c_l3m_mre import l3m
from Data_handle.Coordinate_transfer import xy2ll

def caculate_predict():
    while True:
        time.sleep(5)
        global combined_data
        combined_data_df = pd.DataFrame(combined_data)
        predict_point = l3m(combined_data_df,-60,1.7)
        lon, lat = xy2ll(predict_point[0],predict_point[1],initial_location[0],initial_location[1])
        predict_json = json.dumps({"type": "predict_location","data":{'lon': lon, 'lat':lat}})
        print(predict_json)
        sys.stdout.flush()
     

def predict_point():
    thread = threading.Thread(target=caculate_predict)
    thread.start()
