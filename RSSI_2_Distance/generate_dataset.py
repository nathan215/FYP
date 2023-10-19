import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

def store_into_database(test_record_data):
    username = 'postgres'
    password = '0000'
    host = 'localhost'
    port = '5433'
    database_name = 'FYP'
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}')

    recording_data = {
        'id' : 2,
        'simulate_or_not': test_record_data['stimulate'],
        'latitude': None,
        'longitude': None,
        'start_time': datetime.now(),
        'description': f"C: {test_record_data['C']}, n: {test_record_data['n']}, Noise: 3+0.002dist"
    }
    recording_df = pd.DataFrame([recording_data])
    

    for record in test_record_data['rssi_records']:
        record['record_id'] = 2

    test_records_df = pd.DataFrame(test_record_data['rssi_records'])

    try:
        recording_df.to_sql('recording', con=engine, index=False, if_exists='append', method='multi')
        test_records_df.to_sql('test_records', con=engine, index=False, if_exists='append', method='multi')
    except Exception as e:
        print(e)
    


def generate_dataset(stimulate, n, C):
    test_record = {
        'stimulate': stimulate,
        'C': C,
        'n': n,
        'rssi_records': []
    }

    for x in list(range(1, 10, 1)) + list(range(20, 100, 10)) + list(range(150, 1000, 50)):
        for y in list(range(1, 10, 1)) + list(range(20, 100, 10)) + list(range(150, 1000, 50)):
            for z in range(2, 100, 2):
                horizen_distance = np.sqrt(x**2 + y**2)
                rssi = generate_rssi(horizen_distance, z, n, C)
                record = {
                    'test_record_id': len(test_record['rssi_records']) + 1,
                    'x': x,
                    'y': y,
                    'z': z,
                    'rssi': rssi,
                    'time': datetime.now()
                }
                test_record['rssi_records'].append(record)
    
    store_into_database(test_record)
    
def generate_rssi(horizen_distance, z, n, C):
    mean_noise = 3 + 0.002 * np.sqrt(horizen_distance**2 + z **2)
    noise = np.random.normal(0, mean_noise)
    rssi = C - 10 * n * np.log10(np.sqrt(horizen_distance**2 + z**2)) + noise
    return rssi


generate_dataset(True, 2, -40)




