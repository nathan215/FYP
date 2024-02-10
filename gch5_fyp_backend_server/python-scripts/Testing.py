import sys
import random
import time
from datetime import datetime
import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'FYP', # Database name
    'user': 'postgres',  
    'password': '0000', 
    'host': 'localhost',
    'port': '5433' 
}

# Function to generate random data
def generate_data(execution_id):
    current_time = datetime.utcnow()
    lat = round(random.uniform(-90, 90), 6)  # Generate random latitude
    lon = round(random.uniform(-180, 180), 6)  # Generate random longitude
    rssi_signal = random.randint(-100, 0)  # Generate random RSSI signal strength
    
    data = (current_time, lat, lon, rssi_signal, execution_id)
    
    return data

def main(execution_id):
    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    
    # Ensure your SQL table and columns match the data structure
    insert_query = """INSERT INTO RealTimeData (time, lat, lon, rssi_signal, execution_id) 
                      VALUES (%s, %s, %s, %s, %s);"""
    
    while True:
        data = generate_data(execution_id)
        cur.execute(insert_query, data)
        conn.commit()  # Commit the transaction
        print(f"Inserted data: {data}")
        time.sleep(1)  # Wait for 1 second before generating next data point

    # Close the database connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Testing.py <executionId>")
        sys.exit(1)
    
    execution_id = sys.argv[1]
    main(execution_id)